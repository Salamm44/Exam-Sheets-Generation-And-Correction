import os
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk

class PDFGenerator:
    def __init__(self, host='localhost', port=3306, user='root', password='SSSShhhh_1000', database='Students'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def fetch_students(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT stu_id, stu_Name FROM Students")
            return cursor.fetchall()  
        
    def add_student(self, name):
     if self.connection:
         cursor = self.connection.cursor()
         try:
             cursor.execute("INSERT INTO students (stu_name) VALUES (%s)", (name,))
             self.connection.commit() 
             print(f"Student '{name}' added successfully.")
         except Exception as e:
             print(f"An error occurred: {str(e)}")
         finally:
             cursor.close()  
     else:
        print("No database connection.")


    def add_score(self, id ,score):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute("UPDATE students SET score = %s WHERE stu_id = %s", (score, id))
                self.connection.commit()
                print(f"Score '{score}' updated successfully for student ID '{id}'.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                cursor.close()
        else:
            print("No database connection!")
    
    def clear_students_file(self):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute("DELETE FROM Students")
                self.connection.commit()  
                print("All student records have been deleted.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                cursor.close()  
        else:
            print("No database connection!")

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


