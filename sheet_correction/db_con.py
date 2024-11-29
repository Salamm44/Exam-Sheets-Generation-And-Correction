import os
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import logging
import tkinter as tk


class PDFGenerator:
    def __init__(self, database='students.db'):
        self.db_path = database
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            print("Connected to SQLite database")
            self.initialize_database()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("SQLite connection closed")

    def create_table(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    stu_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stu_name TEXT NOT NULL,
                    score REAL
                )
            """)
            self.connection.commit()
            print("Table created or already exists")
        else:
            print("No database connection")



    def fetch_students(self):
        connection = sqlite3.connect("Students.db")  
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT stu_id, stu_name  FROM students") 
            students = cursor.fetchall()
            connection.commit()  
            return students


        except sqlite3.Error as e:
            logging.error(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
     

    def initialize_database(self):
        if self.connection:
            cursor = self.connection.cursor()

            # Path to the SQL file
            sql_file_path = os.path.join(os.getcwd(), "databaseStructure.sql")

            try:
                with open(sql_file_path, 'r') as sql_file:
                    sql_script = sql_file.read()

                cursor.executescript(sql_script)

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';")
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('students', 4512341);")
                else:
                    cursor.execute("UPDATE sqlite_sequence SET seq = 4512341 WHERE name = 'students';")

                self.connection.commit()
                print("Database initialized successfully")
            except Exception as e:
                print(f"Error initializing database: {e}")
            finally:
                cursor.close()
    

    def add_student(self, student_name):
        connection = sqlite3.connect("Students.db")  
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO students (stu_name) VALUES (?)", (student_name,))
            connection.commit()  
            logging.info(f"Student {student_name} added to the database.")
        except sqlite3.Error as e:
            logging.error(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()



    def add_score(self, id, score):
     connection = sqlite3.connect("Students.db")  
     cursor = connection.cursor()
     try:
        print(f"Updating score for ID: {id}, New Score: {score}")
        cursor.execute("UPDATE students SET score = ? WHERE stu_id = ?", (score, id))
        connection.commit()  
        print(f"Score '{score}' updated successfully for student ID '{id}'.")
     except sqlite3.Error as e:
        print(f"An error occurred: {str(e)}")
     finally:
        cursor.close()
        connection.close()





    def clear_students_file(self):

     connection = sqlite3.connect("Students.db")   
     cursor = connection.cursor()
     try:
            cursor.execute("DELETE FROM students")
            connection.commit()
            print("All student records have been deleted.")
     except sqlite3.Error as e:
            print(f"An error occurred: {str(e)}")
     finally:
            cursor.close()
            connection.close()

    def generate_pdf(self, template_pdf_path, output_folder):
        students = self.fetch_students()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for student_id, student_name in students:
            output_path = os.path.join(output_folder, f"{student_name}.pdf")

            reader = PdfReader(template_pdf_path)
            writer = PdfWriter()

            first_page = reader.pages[0]
            temp_canvas_path = f"{student_name}_temp.pdf"
            c = canvas.Canvas(temp_canvas_path, pagesize=A4)
            c.setFont("Helvetica", 18)
            c.drawString(417.0, 800.0, f"{student_id}")
            c.save()

            overlay_reader = PdfReader(temp_canvas_path)
            first_page.merge_page(overlay_reader.pages[0])
            writer.add_page(first_page)

            for page_num in range(1, len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)

            os.remove(temp_canvas_path)

            print(f"Generated PDF for: {student_name}")
