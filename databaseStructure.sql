CREATE TABLE IF NOT EXISTS students (
    stu_id INTEGER PRIMARY KEY AUTOINCREMENT,  
    stu_name TEXT NOT NULL,                   
    score INTEGER DEFAULT 0                   
);


UPDATE sqlite_sequence 
SET seq = (SELECT MAX(stu_id) FROM students) 
WHERE name = 'students';


INSERT OR IGNORE INTO sqlite_sequence (name, seq) 
VALUES ('students', (SELECT MAX(stu_id) FROM students));
