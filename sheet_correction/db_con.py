import os
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk

class PDFGenerator:
    def __init__(self, database='students.db'):
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database)
            print("Connected to SQLite database")
            self.initialize_database()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            self.connection = None

    def initialize_database(self):
        """Initialize the database using the SQL script file."""
        if self.connection:
            cursor = self.connection.cursor()

            # Path to the SQL file
            sql_file_path = os.path.join(os.getcwd(), "databaseStructure.sql")

            try:
                # Read the SQL script
                with open(sql_file_path, "r", encoding="utf-8") as sql_file:
                    sql_script = sql_file.read()

                # Execute the SQL script
                cursor.executescript(sql_script)
                print("Database initialized using 'databaseStructure.sql'")

            except FileNotFoundError:
                print(f"SQL file '{sql_file_path}' not found. Ensure the file exists in the project root.")
            except sqlite3.Error as e:
                print(f"An error occurred while executing the SQL script: {str(e)}")
            finally:
                self.connection.commit()


    def close(self):
        if self.connection:
            self.connection.close()
            print("SQLite connection closed")

    def fetch_students(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT stu_id, stu_name FROM students")
            return cursor.fetchall()

    def add_student(self, name):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute("INSERT INTO students (stu_name) VALUES (?)", (name,))
                self.connection.commit()
                print(f"Student '{name}' added successfully.")
            except sqlite3.Error as e:
                print(f"An error occurred: {str(e)}")

    def add_score(self, id, score):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute("UPDATE students SET score = ? WHERE stu_id = ?", (score, id))
                self.connection.commit()
                print(f"Score '{score}' updated successfully for student ID '{id}'.")
            except sqlite3.Error as e:
                print(f"An error occurred: {str(e)}")

    def clear_students_file(self):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute("DELETE FROM students")
                self.connection.commit()
                print("All student records have been deleted.")
            except sqlite3.Error as e:
                print(f"An error occurred: {str(e)}")

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