import os
import glob
import json
from dataclasses import dataclass, field, asdict
from typing import List
from sheet_correction.quadrat_processor import QuadratProcessor 
from sheet_correction.db_con import PDFGenerator
import tkinter as tk

# assets dir path
ROOT_DIR = os.path.join(".", "allstudent")
ASSETS_DIR = os.path.join(".", "assets")
PROCESSED_IMAGES_DIR = os.path.join(ASSETS_DIR, "processed_images")
STUDENTS_FILE = os.path.join(ROOT_DIR, "students.json")

@dataclass
class Student:
    student_id: str
    name: str = "Unknown"  
    score: float = 0.0
    student_answers_result: List[str] = field(default_factory=list)
    original_answered_sheet_path: str = ""
    corrected_sheet_path: str = ""

def __init__(self, student_id, name, student_answers_result=None):
    self.student_id = student_id
    self.name = name
    self.student_answers_result = student_answers_result

    def __post_init__(self):
        if not isinstance(self.student_id, str):
            raise ValueError("student_id must be a string")
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if not isinstance(self.score, (int, float)):
            raise ValueError("score must be a number")
        if not isinstance(self.student_answers_result, list):
            raise ValueError("student_answers_result must be a list")
        if not isinstance(self.original_answered_sheet_path, str):
            raise ValueError("original_answered_sheet_path must be a string")
        if not isinstance(self.corrected_sheet_path, str):
            raise ValueError("corrected_sheet_path must be a string")
        

    @classmethod
    def from_image(cls, image_path: str):
        processor = QuadratProcessor(prefix='student_sheet', student_id='unknown')
        student_name, student_id = processor.detect_student_info(image_path)
        return cls(student_id=student_id, name=student_name, original_answered_sheet_path=image_path)

def ensure_dir(directory: str):
    os.makedirs(directory, exist_ok=True)

def save_student_score(student: Student):
    try:
        addscore=PDFGenerator(database='Students')
        addscore.connect()
        addscore.add_score(student.student_id,student.score)
        addscore.close()
        tk.messagebox.showinfo("Score update",f"Score for student ID {student.student_id} has been updated to {student.score} in the database.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        students = load_students_from_file(STUDENTS_FILE)  
        students.append(student)  
        save_students_to_file(students, STUDENTS_FILE)  

    except Exception as e:
        print(f"An error occurred while saving the student's score: {str(e)}")

####json
def save_students_to_file(students: List[Student], filename: str):
    with open(filename, 'w') as f:
        json.dump([asdict(student) for student in students], f, indent=4)

def load_students_from_file(filename: str) -> List[Student]:
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                students_data = json.load(f)
                return [Student(**data) for data in students_data]
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}. Returning empty list.")
            return []
    else:
        print(f"File {filename} does not exist. Returning empty list.")
        return []

def delete_student_sheet(sheet_path: str):
    if os.path.exists(sheet_path):
        os.remove(sheet_path)
        print(f"Deleted sheet: {sheet_path}")
    else:
        print(f"Sheet {sheet_path} does not exist.")

def process_and_cleanup_student_sheets(sheet_paths: List[str]):
    for sheet_path in sheet_paths:
        print(f"Processing {sheet_path}")
        delete_student_sheet(sheet_path)

def get_all_students() -> List[Student]:
    return load_students_from_file(STUDENTS_FILE)

def clear_students_file():
    with open(STUDENTS_FILE, 'w') as file:
        json.dump([], file)

    image_files = glob.glob(os.path.join(PROCESSED_IMAGES_DIR, '*'))
    for image_file in image_files:
        try:
            os.remove(image_file)
            print(f"Deleted {image_file}")
        except Exception as e:
            print(f"Error deleting {image_file}: {e}")

ensure_dir(ASSETS_DIR)
ensure_dir(PROCESSED_IMAGES_DIR)


