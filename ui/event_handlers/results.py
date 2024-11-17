import tkinter as tk
from tkinter import ttk
from sheet_correction.db_con import PDFGenerator
from allstudent.student import get_all_students

def extract_results():
    result_window = tk.Toplevel()
    result_window.title("Student Results")
    frame = tk.Frame(result_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Score"), show='headings')
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)
    y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    pdf_gen = PDFGenerator()
    pdf_gen.connect()  

    query = "SELECT stu_id, stu_name, score FROM Students"
    cursor = pdf_gen.connection.cursor()
    cursor.execute(query)
    students = cursor.fetchall()
    for student in students:
        tree.insert("", tk.END, values=(student[0], student[1], student[2]))

    cursor.close()
    pdf_gen.close()