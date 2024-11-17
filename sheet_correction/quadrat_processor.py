import os
import cv2
from .image_processing import detect_quadrats, preprocess_image
import pytesseract
from PIL import Image
import logging
import re
from ui.event_handlers.utils import upload_and_convert_pdf 


operationnum=1
class QuadratProcessor:
    
    pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    def __init__(self, directory='./assets/processed_images', prefix='corrected_sheet', student_id=None):
        self.directory = directory
        self.prefix = prefix
        self.student_id = student_id


   
    def detect_student_info(self, image_path):
       
        nameroi=None
        idroi=None
        try:
            image = cv2.imread(image_path)
            if image is None:
                logging.error(f"Failed to load image from path: {image_path}")
                return {}

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            list_of_info_locations=[[ 1219 , 22 ,250 , 39 ] ,[ 1120 , 65 ,530 , 60 ]]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  
            
            for i, location in enumerate(list_of_info_locations):
                if i == 0:
                    x, y, w, h = location
                    nameroi=cv2.GaussianBlur(gray[y:y+h , x:x+w], (5, 5), 0)
                elif i == 1:
                    x2, y2, w2, h2 = location
                    idroi=cv2.GaussianBlur(gray[y2:y2+h2 , x2:x2+w2 ], (5, 5), 0)


            _, binary_image1 = cv2.threshold(nameroi, 128, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            _, binary_image2 = cv2.threshold(idroi, 128, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            eroded_image1 = cv2.erode(binary_image1, kernel, iterations=1)
            dilated_image1 = cv2.dilate(eroded_image1, kernel, iterations=1)
            eroded_image2 = cv2.erode(binary_image2, kernel, iterations=1)
            dilated_image2 = cv2.dilate(eroded_image2, kernel, iterations=1)
            student_id, student_name = self.detect_and_recognize_text(dilated_image1, dilated_image2)
            return {
                'student_id': student_id,
                'student_name': student_name
            }

        except Exception as e:
            logging.error(f"An error occurred while detecting student info: {e}")
            return {}

    def detect_and_recognize_text(self, binary_image1, binary_image2):
        student_id = ""
        student_name = ""
        student_name=pytesseract.image_to_string(binary_image1 , config='--psm 8').strip()    
        student_id=pytesseract.image_to_string(binary_image2 , config='--psm 7 -c tessedit_char_whitelist=0123456789').strip()
        """for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = original_image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='--psm 7')
            if text.isdigit():
                student_id = text
            elif text.isalpha():
                student_name = text"""
        return student_id, student_name
    
    
    def extract_correct_answers_with_boxes(self, filename=None, sheet_type='corrected'):
        global operationnum
        if filename:
            image_path = os.path.join(self.directory, filename)
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"No image with filename '{filename}' found in directory '{self.directory}'")
        else:
            file_names = os.listdir(self.directory)
            print(f"Files in directory: {file_names}") 
            
            image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            image_paths = [os.path.join(self.directory, file) for file in image_files if file.lower().startswith(self.prefix.lower())]
            
            print(f"Filtered image paths: {image_paths}")
            
            if not image_paths:
                raise FileNotFoundError(f"No image with prefix '{self.prefix}' found in directory '{self.directory}'")
            
            image_path = image_paths[0]
        
        image, binary = preprocess_image(image_path)
        
        if image is None or binary is None:
            raise ValueError("Image preprocessing failed.")
        
        processed_image, filled_quadrats, empty_quadrats = detect_quadrats(image, binary)
        print(f"Detected {len(filled_quadrats)} filled quadrats and {len(empty_quadrats)} empty quadrats")
        all_quadrats = filled_quadrats + empty_quadrats
        all_quadrats = sorted(all_quadrats, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
        filled_quadrats_rects = [cv2.boundingRect(fq) for fq in filled_quadrats]
        quadrat_values = []
        
        # Draw contours 
        for quadrat in all_quadrats:
            quadrat_rect = cv2.boundingRect(quadrat)
            is_filled = quadrat_rect in filled_quadrats_rects
            quadrat_values.append(1 if is_filled else 0)
            color = (0, 255, 0) if is_filled else (0, 0, 255)  
            cv2.drawContours(processed_image, [quadrat], -1, color, 2)
            x, y, w, h = quadrat_rect
            cv2.putText(processed_image, str(1 if is_filled else 0), (x - 30, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        output_filename = f'processed_image_with_contours_and_values_{sheet_type}_page_{operationnum}'
        if self.student_id:
            output_filename += f'_ID_{self.student_id}'
        output_filename += '.jpg'
        output_path = os.path.join(self.directory, output_filename)
        cv2.imwrite(output_path, processed_image)
        print(f"Processed image saved to {output_path}")
        operationnum+=1
        
        return quadrat_values
    
    
