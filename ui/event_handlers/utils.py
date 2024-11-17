import os
from pdf_utils import convert_pdf_to_images  
import string
import random
from tkinter import messagebox

def upload_and_convert_pdf(file_path, prefix, student_id=""):
    assets_dir = "./assets"
    processed_images_dir = "./assets/processed_images"

    for directory in [assets_dir, processed_images_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    if student_id:
        papers_folder = os.path.join(processed_images_dir, f"{student_id}")
        if not os.path.exists(papers_folder):
            os.makedirs(papers_folder)
    else:
        papers_folder=os.path.join(processed_images_dir , f"{prefix}")

    image_paths = convert_pdf_to_images(file_path, papers_folder)

    return image_paths

def generate_student_id(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

