import logging
from sheet_correction.db_con import PDFGenerator
import tkinter as tk

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

correct_answers = []
answer_mark = 0

def set_correct_answers(new_correct_answers):
    global correct_answers
    correct_answers = new_correct_answers
    logging.info(f"Correct answers updated: {correct_answers}")

def get_correct_answers():
    global correct_answers
    return correct_answers

def set_answer_mark(mark):
    global answer_mark
    answer_mark = mark
    logging.info(f"Answer mark set to: {answer_mark}")

def get_answer_mark():
    global answer_mark
    return answer_mark

def calculate_score(student_answers):  
    global correct_answers, answer_mark
    if not correct_answers:
        logging.warning("Correct answers have not been set.")
        return 0

    logging.debug(f"Correct answers: {correct_answers}")
    if len(student_answers) != len(correct_answers):
        logging.warning(f"Length mismatch: {len(student_answers)} student answers vs {len(correct_answers)} correct answers.")
        return 0

    score = 0
    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer == 0 or correct_answer == 0:
            continue
        if student_answer == correct_answer:
            score += answer_mark

    logging.info(f"Calculated score: {score}")
    return score
