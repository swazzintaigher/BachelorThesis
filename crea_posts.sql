CREATE TABLE IF NOT EXISTS paziente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    eta INT,
    mail VARCHAR(100),
    via VARCHAR(50),
    citta VARCHAR(50),
    numerotelefono VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS lesioni (
    id SERIAL PRIMARY KEY,
    idpaziente INT,
    dimensione DECIMAL(5,2),
    locazione VARCHAR(100),
    classificazione_automatica VARCHAR(100),
    classificazione_medico VARCHAR(100),
    id_immagine INT,
    FOREIGN KEY (idpaziente) REFERENCES paziente(id)
);

CREATE TABLE IF NOT EXISTS immagini (
    id SERIAL PRIMARY KEY,
    idlesione INT, 
    immagine VARCHAR(255), -- Memorizza il percorso del file sull'archiviazione
    formato VARCHAR(10),
    idimmagini INT,
    FOREIGN KEY (idlesione) REFERENCES lesioni(id)
);

CREATE TABLE IF NOT EXISTS utenti (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
