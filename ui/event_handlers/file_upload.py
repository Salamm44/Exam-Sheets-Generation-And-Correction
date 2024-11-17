import os
from tkinter import filedialog, messagebox
from allstudent.student import save_student_score, Student
from ..dialog import CorrectedSheetDialog
from sheet_correction.quadrat_processor import QuadratProcessor
from answers_manager import set_correct_answers, calculate_score, set_answer_mark, get_correct_answers
from .utils import upload_and_convert_pdf, generate_student_id
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def upload_corrected_sheet(root):
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            dialog = CorrectedSheetDialog(root)
            correction_system = dialog.correction_system
            answer_mark = dialog.answer_mark
            print(f"Correction System: {correction_system}")
            print(f"Mark per Correct Answer: {answer_mark}")

            set_answer_mark(float(answer_mark))

            image_paths=upload_and_convert_pdf(file_path, "corrected_sheet")
            print(image_paths)

            processor = QuadratProcessor(prefix='corrected_sheet')
            all_corrected_answers = []
            for image_path in image_paths:
                processor.directory = os.path.dirname(image_path)
                filename = os.path.basename(image_path)
                corrected_answers = processor.extract_correct_answers_with_boxes(filename=filename, sheet_type='corrected')
                all_corrected_answers.extend(corrected_answers)

            
            set_correct_answers(all_corrected_answers)

            messagebox.showinfo("Success", "Corrected sheet processed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the corrected sheet: {e}")

def upload_student_sheets(root):
    choice = messagebox.askyesno("Upload Type", "Would you like to upload multiple PDFs from a folder?")

    if choice:  
        folder_path = filedialog.askdirectory()  
        if folder_path:
            pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
            if pdf_files:
                try:
                    for file_path in pdf_files:
                        student_id, student_name, student_answers, converted_image_path = process_student_sheet(file_path)
                        validate_and_save_student_sheet(student_id, student_name, student_answers, converted_image_path)
                    messagebox.showinfo("Success", "All student sheets have been processed successfully.")
                except Exception as e:
                    logging.error(f"An error occurred while uploading the student sheets: {e}")
                    messagebox.showerror("Error", f"An error occurred while uploading the student sheets: {e}")
            else:
                messagebox.showwarning("No PDFs", "No PDF files were found in the selected folder.")
        else:
            messagebox.showwarning("No Folder", "No folder selected.")
    
    else:  #  single file
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Ask for single file
        if file_path:
            try:
                student_id, student_name, student_answers, converted_image_path = process_student_sheet(file_path)
                validate_and_save_student_sheet(student_id, student_name, student_answers, converted_image_path)
                messagebox.showinfo("Success", "Student sheet has been processed successfully.")
            except Exception as e:
                logging.error(f"An error occurred while uploading the student sheet: {e}")
                messagebox.showerror("Error", f"An error occurred while uploading the student sheet: {e}")
        else:
            messagebox.showwarning("No File", "No file selected.")


def process_student_sheet(file_path):
    processor = QuadratProcessor(prefix='student_sheet')

    image_paths_for_info = upload_and_convert_pdf(file_path, "student_sheet_for_info")
    student_info = processor.detect_student_info(image_paths_for_info[0])  # Process first page for student info
    logging.debug(f"Student info: {student_info}")
    student_id = student_info.get('student_id')
    student_name = student_info.get('student_name', 'Unknown')

    if not student_id:
        student_id = generate_student_id()
        logging.warning("Student ID could not be detected from the sheet. Generated a new Student ID.")

    image_paths = upload_and_convert_pdf(file_path, "student_sheet", student_id)
    logging.debug(f"Converted image paths: {image_paths}")

    if not image_paths or any(not os.path.exists(image_path) for image_path in image_paths):
        raise ValueError("One or more converted image paths are invalid or do not exist.")

    all_student_answers = []

    for image_path in image_paths:
        filename = os.path.basename(image_path)
        logging.debug(f"Processing filename: {filename}")
        filename_with_id = os.path.join(student_id, filename)

        student_answers = processor.extract_correct_answers_with_boxes(filename=filename_with_id, sheet_type='student')
        logging.debug(f"Student answers from page {filename}: {student_answers}")

        all_student_answers.extend(student_answers)

    return student_id, student_name, all_student_answers, image_paths

def validate_and_save_student_sheet(student_id, student_name, student_answers, image_paths):
    correct_answers = get_correct_answers()
    if not correct_answers:
        messagebox.showerror("Error", "Correct answers have not been set. Please upload the corrected sheet first.")
        return

    if not isinstance(student_answers, list):
        messagebox.showerror("Error", "Invalid data format for student answers. Expected a list.")
        return

    if len(student_answers) != len(correct_answers):
        messagebox.showerror("Error", f"Length mismatch: {len(student_answers)} student answers vs {len(correct_answers)} correct answers.")
        return

    score = calculate_score(student_answers)

    processed_images_dir = "./assets/processed_images"
    original_answered_sheet_paths = image_paths
    corrected_sheet_path = os.path.join(processed_images_dir, f"{student_id}_corrected.png")

    new_student = Student(
        student_id=student_id,
        name=student_name,
        score=score,
        student_answers_result=student_answers,
        original_answered_sheet_path=original_answered_sheet_paths[0],  
        corrected_sheet_path=corrected_sheet_path
    )

    save_student_score(new_student)

    logging.info(f"Uploaded Student Name: {new_student.name}")
    logging.info(f"Uploaded Student ID: {new_student.student_id}")

    messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")



