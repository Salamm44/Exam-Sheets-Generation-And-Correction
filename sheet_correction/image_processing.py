import cv2
import numpy as np
from answers_manager import calculate_score

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return None, None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # morphological op
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)

    return image, binary


def detect_quadrats(image, binary):
    # ROI
    x, y, w, h = 20, 250, 1200, 1900
    roi_image = image[y:y+h, x:x+w]
    roi_binary = binary[y:y+h, x:x+w]
    contours, _ = cv2.findContours(roi_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    empty_quadrats = []
    filled_quadrats = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if 500 < area < 800:  
            mask = np.zeros_like(roi_binary)
            cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
            mean_val = cv2.mean(cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY), mask=mask)[0]

            if mean_val > 170:  
                empty_quadrats.append(contour)
            else:
                filled_quadrats.append(contour)

    return roi_image, filled_quadrats, empty_quadrats



def extract_answers(filled_quadrats, empty_quadrats):
    answers = []
    for i in range(len(filled_quadrats)):
        answers.append(1)  
    for i in range(len(empty_quadrats)):
        answers.append(0)  
    return answers



def process_image_for_scoring(image_path, correct_answers):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    processed_image, filled_quadrats, empty_quadrats = detect_quadrats(image, binary)
    student_answers = extract_answers(filled_quadrats, empty_quadrats)
    score = calculate_score(student_answers) #, correct_answers) #delete

    return processed_image, score


