CREATE DATABASE IF NOT EXISTS trashtalk;

USE trashtalk;

CREATE TABLE IF NOT EXISTS users (
    guid INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(128) NOT NULL,
    lastname VARCHAR(128) NOT NULL,
    phone VARCHAR(32) NOT NULL,
    type VARCHAR(32) NOT NULL,
    company VARCHAR(128),
    password VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    type VARCHAR(128) NOT NULL,
    size VARCHAR(128) NOT NULL,
    color VARCHAR(128) NOT NULL,
    sorting VARCHAR(128) NOT NULL,
    price FLOAT NOT NULL,
    description VARCHAR(128) NOT NULL,
    quantity INT NOT NULL,
    image LONGBLOB,
    image2 LONGBLOB,
    image3 LONGBLOB
);

ALTER TABLE users ADD CONSTRAINT unq_email UNIQUE (email);
ALTER TABLE users ADD CONSTRAINT unq_phone UNIQUE (phone);