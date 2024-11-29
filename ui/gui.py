import tkinter as tk
from ui.event_handlers.file_upload import upload_corrected_sheet, upload_student_sheets
from ui.event_handlers.results import extract_results
from allstudent.student import clear_students_file
from sheet_correction.db_con import PDFGenerator

def init_gui():
    root = tk.Tk()
    root.title("Exam Evaluation App")
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=v_scrollbar.set)
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')
    inner_frame.grid_rowconfigure(0, weight=1)
    inner_frame.grid_columnconfigure(0, weight=1)
    button_width = 20


    

    def reset_students_file():
      try:
          pdf_gen = PDFGenerator(database='Students')
          pdf_gen.connect()
          pdf_gen.clear_students_file()  
          pdf_gen.close()
          tk.messagebox.showinfo("Reset", "The students database has been reset.")
      except Exception as e:
          tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")




  
            
    
    def prepare_exam():
        output_folder = tk.filedialog.askdirectory(title="Select Output Folder")
        selected_pdf = tk.filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")],
            title="Select Input PDF File"
        )

        if selected_pdf and output_folder:  
            try:
                pdf_gen = PDFGenerator(database='Students')
                pdf_gen.connect()  # Connect to the database
                pdf_gen.generate_pdf(selected_pdf, output_folder)
                pdf_gen.close()  # Close the connection
                
                tk.messagebox.showinfo("Success", "Exam PDF generated successfully.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            tk.messagebox.showwarning("Warning", "No file or folder selected.")

    def add_new_student_to_db(name):
        try:
            pdf_gen = PDFGenerator(database='Students')
            pdf_gen.connect()
            pdf_gen.add_student(name)  
            pdf_gen.close()
            tk.messagebox.showinfo("Success", f"Student '{name}' added to the database.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    student_name_entry = tk.Entry(inner_frame, width=30)
    student_name_entry.grid(row=7, column=1, padx=5, pady=5)   


    btn_upload_corrected = tk.Button(
        inner_frame,
        text="Corrected Sheet",
        command=lambda: upload_corrected_sheet(root),
        width=button_width,
        padx=20,
        pady=10,
        bg="pink",
        font=("Arial", 14)
    )
    btn_upload_corrected.grid(row=2, column=1, pady=5, sticky='ew')

    btn_upload_students = tk.Button(
        inner_frame,
        text="Student Sheets",
        command=lambda: upload_student_sheets(root),
        width=button_width,
        padx=20,
        pady=10,
        bg="lightyellow",
        font=("Arial", 14)
    )
    btn_upload_students.grid(row=3, column=1, pady=5, sticky='ew')

    btn_reset_students = tk.Button(
        inner_frame,
        text="Reset Students",
        command=reset_students_file,
        width=button_width,
        padx=20,
        pady=10,
        bg="lightblue",
        font=("Arial", 14)
    )
    btn_reset_students.grid(row=4, column=1, pady=5, sticky='ew')

    btn_results = tk.Button(
        inner_frame,
        text="Results",
        command=extract_results,
        width=button_width,
        padx=20,
        pady=10,
        bg="lightgreen",
        font=("Arial", 14)
    )
    btn_results.grid(row=5, column=1, pady=5, sticky='ew')

    btn_prepare_exam = tk.Button(
        inner_frame,
        text="Prepare Exam for All",
        command=prepare_exam,  
        width=button_width,
        padx=20,
        pady=10,
        bg="lightcoral",
        font=("Arial", 14)
    )
    btn_prepare_exam.grid(row=6, column=1, pady=5, sticky='ew')  

    btn_add_student_to_db=tk.Button(
        inner_frame,
        text="Add new student by name",
        command=lambda: add_new_student_to_db(student_name_entry.get().strip()),
        width=button_width,
        padx=20,
        pady=10,
        bg="green",
        font=("Arial",14)
    )
    btn_add_student_to_db.grid(row=8 , column=1 , pady=5 , sticky='ew')



    window_width = button_width * 10 + 40
    window_height = (button_width * 3 + 20) * 4 + 100  

    margin = 20
    window_width += margin
    window_height += margin

    root.geometry(f"{window_width}x{window_height}")

    root.mainloop()
