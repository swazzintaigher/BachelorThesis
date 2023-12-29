from flask import Flask, render_template, redirect, request, session, url_for, flash, abort
import psycopg2

import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.add_url_rule('/uploads/<filename>', 'uploads', build_only=True)
picFolder = os.path.join('.', 'uploads')
app.config['UPLOADED_PHOTOS_DEST'] = r'C:\Users\Gianluca\Desktop\flask_app\static\uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only immagini'),
            FileRequired('File non deve essere vuoto')
        ]
    )
    submit = SubmitField('Upload')

def connect_db():
    conn = psycopg2.connect(
        dbname="progetto tesi",
        user="postgres",
        password="748596",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica le credenziali dell'utente
        conn = connect_db()  # Assicurati di avere questa funzione
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM utenti WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Credenziali corrette, autenticazione riuscita
            session['user_id'] = user[0]
            flash('Login riuscito!', 'success')
            return redirect('/pazienti')
        else:
            # Credenziali errate, mostra un messaggio di errore
            flash('Credenziali non valide. Riprova.', 'danger')

    return render_template('login.html')

from werkzeug.security import generate_password_hash

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Verifica se l'utente esiste già
            conn = connect_db()
            cursor = conn.cursor()
            
            # Controlla se l'utente esiste già
            cursor.execute('SELECT * FROM utenti WHERE username = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Utente già registrato. Utilizza un altro nome utente.', 'danger')
            else:
                # Utilizza generate_password_hash per creare un hash sicuro della password
                hashed_password = generate_password_hash(password, method='sha256')
                
                # Procedi con l'inserimento dell'utente nel database
                cursor.execute('INSERT INTO utenti (username, password) VALUES (%s, %s)', (username, hashed_password))
                conn.commit()
                
                flash('Account creato con successo! Ora puoi effettuare il login.', 'success')
                return redirect('/')
                
        except Exception as e:
            flash(f'Errore durante la registrazione: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/pazienti')
def pazienti():
    # Connessione al database
    connection = connect_db()
    cursor = connection.cursor()

    # Eseguire la query SQL per ottenere i dati
    cursor.execute('SELECT * FROM paziente')

    # Crea la lista dei pazienti presenti nel database da passare poi al template html
    posts = cursor.fetchall()

    # Chiudere la connessione al database
    cursor.close()
    connection.close()

    # Funzione che prende la lista posts di pazienti presenti nel database, lo passo tramite il parametro posts
    return render_template('pazienti.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        eta = request.form['eta']
        mail = request.form['mail']
        via = request.form['via']
        citta = request.form['citta']
        numerotelefono = request.form['numerotelefono']

        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO paziente(nome, cognome, eta, mail, via, citta, numerotelefono) VALUES (%s, %s, %s, %s, %s, %s, %s)', (nome, cognome, eta, mail, via, citta, numerotelefono))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect('/pazienti')

    return render_template('create.html')

@app.route('/<int:idx>/cancella', methods=('POST',))
def delete(idx):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        # Prima elimina le immagini associate
        cursor.execute('DELETE FROM immagini WHERE idlesione IN (SELECT id FROM lesioni WHERE idpaziente = %s)', (idx,))

        # Poi elimina le lesioni
        cursor.execute('DELETE FROM lesioni WHERE idpaziente = %s', (idx,))

        # Infine elimina il paziente
        cursor.execute('DELETE FROM paziente WHERE id=%s', (idx,))

        # Esegue il commit delle modifiche al database
        connection.commit()

    except Exception as e:
        # In caso di errore, annulla le modifiche e restituisci un errore 500
        connection.rollback()
        abort(500, str(e))

    finally:
        cursor.close()
        connection.close()

    return redirect('/pazienti')

from flask import send_from_directory
from PIL import Image

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

def get_image_format(image_path):
    try:
        with Image.open(image_path) as img:
            return img.format
    except Exception as e:
        print(f"Error while getting image format: {e}")
        return None

@app.route('/<int:idx>/aggiungi', methods=['GET', 'POST'])
def aggiungi(idx):
    form = UploadForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            dimensione = request.form['dimensione']
            locazione = request.form['locazione']
            classificazione_automatica = request.form['classificazione_automatica']
            classificazione_medico = request.form['classificazione_medico']

            try:
                # Assicurati che la cartella esista, altrimenti creala
                user_upload_folder = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], str(idx))
                if not os.path.exists(user_upload_folder):
                    os.makedirs(user_upload_folder)

                # Salva l'immagine nella sottocartella specifica dell'utente/paziente
                filename = secure_filename(form.photo.data.filename)
                file_path = os.path.join(user_upload_folder, filename)
                form.photo.data.save(file_path)

                # Crea il percorso completo del file
                file_url = url_for('get_file', filename=os.path.join(str(idx), filename))

                # Ottieni l'idlesione più alto e incrementalo di 1
                conn = connect_db()
                cursor = conn.cursor()

                # Inserisci un nuovo record nella tabella lesioni e ottieni l'idlesione appena creato
                cursor.execute(
                    'INSERT INTO lesioni (idpaziente, dimensione, locazione, classificazione_automatica, classificazione_medico) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                    (idx, dimensione, locazione, classificazione_automatica, classificazione_medico))
                new_idlesione = cursor.fetchone()[0]

                # Inserisci un nuovo record nella tabella immagini
                formato = get_image_format(file_path)
                cursor.execute(
                    'INSERT INTO immagini (idlesione, immagine, formato,idimmagini) VALUES (%s, %s, %s, %s)',
                    (new_idlesione, file_url, formato, new_idlesione))

                conn.commit()
                cursor.close()
                conn.close()

                return render_template('aggiungi.html', form=form, file_url=file_url)

            except Exception as e:
                print(f"Error: {e}")
                flash("Si è verificato un errore durante l'aggiunta dell'immagine.", "error")

    return render_template('aggiungi.html', form=form, file_url=None)

@app.route('/<int:idx>/visualizza')
def visualizza(idx):
    paziente_folder = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], str(idx))

    if not os.path.exists(paziente_folder):
        os.makedirs(paziente_folder)

    image_list = os.listdir(paziente_folder)

    imagelist = [url_for('static', filename=os.path.join('uploads', str(idx), image).replace(os.path.sep, '/')) for image in image_list]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id_immagine, dimensione, locazione, classificazione_automatica, classificazione_medico FROM lesioni WHERE idpaziente = %s', (idx,))
    lesion_info = cursor.fetchall()

    cursor.close()
    conn.close()

    id_immagini = [str(id_img[0]) for id_img in lesion_info]

    print("Paziente Folder:", paziente_folder)
    print("Image List:", imagelist)
    print("Lesion Info:", lesion_info)

    return render_template("immagini.html", imagelist=imagelist, lesion_info=lesion_info)

if __name__ == '__main__':
    app.run(debug=True)
