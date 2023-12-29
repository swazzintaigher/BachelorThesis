import psycopg2

# Configura la connessione al tuo database PostgreSQL
conn = psycopg2.connect(
    dbname="progetto tesi",
    user="postgres",
    password="748596",
    host="localhost",  # Di solito "localhost" se in locale
    port="5432"  # Di solito 5432
)

# Crea un cursore per eseguire comandi SQL
cursor = conn.cursor()

# Leggi il contenuto del tuo file SQL
with open('crea_posts.sql', 'r') as f:
    sql_script = f.read()

# Esegui il contenuto del file SQL
cursor.execute(sql_script)

# Esegui il commit per applicare le modifiche al database
conn.commit()

# Chiudi la connessione
conn.close()
