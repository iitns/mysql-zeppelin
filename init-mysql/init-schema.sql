SHOW TABLES;

SET sql_notes = 0;

CREATE TABLE IF NOT EXISTS registration(
    id INT NOT NULL AUTO_INCREMENT,
    registered_at TIMESTAMP NOT NULL,
    email VARCHAR(255),
    name_kr VARCHAR(64),
    name_en VARCHAR(128),
    preferred_name VARCHAR(4),
    dob DATE,
    gender TINYINT,
    phone VARCHAR(16),
    kakaotalk VARCHAR(32),
    prefer_college TINYINT,
    note TEXT,
    want_register TINYINT,
    CONSTRAINT PK_registration PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS attendance(
    id INT NOT NULL AUTO_INCREMENT,
    table_group VARCHAR(32),
    name VARCHAR(255),
    date DATE,
    prayer_request TEXT,
    CONSTRAINT PK_attendance PRIMARY KEY(id)
);

SET sql_notes = 1;
