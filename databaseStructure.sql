-- Drop the table if it already exists
DROP TABLE IF EXISTS students;

-- Create the table with AUTOINCREMENT
CREATE TABLE students (
    stu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stu_name TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0
);

-- Insert initial records into the table
INSERT INTO students (stu_name) VALUES 
("Peter Nicola"), 
("Salam Darwish"), 
("Ahmed Mansour"), 
("Rose Andrew");

-- Set the starting value for AUTOINCREMENT
UPDATE SQLITE_SEQUENCE SET seq = 4512342 WHERE name = 'students';

-- Insert additional records
INSERT INTO students (stu_name) VALUES 
("John Doe"), 
("Jane Smith");

-- Retrieve all records
SELECT * FROM students;

-- Describe the table structure
PRAGMA table_info(students);