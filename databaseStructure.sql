DROP DATABASE IF EXISTS Students;

CREATE DATABASE Students;
USE Students;

CREATE TABLE students (
    stu_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    stu_name VARCHAR(50),
    score INTEGER NOT NULL DEFAULT 0
);

INSERT INTO students (stu_name) VALUES ("Peter Nicola"), ("Salam Darwish"), ("Ahmed Mansour"), ("Rose Andrew");

ALTER TABLE students AUTO_INCREMENT = 4512343;

INSERT INTO students (stu_name) VALUES ("John Doe"), ("Jane Smith");

SELECT * FROM students;

DESCRIBE students;