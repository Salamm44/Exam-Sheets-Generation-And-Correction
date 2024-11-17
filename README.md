
# Exam Generation and Evaluation App
This application provides tools for generating and evaluating exams, including a graphical interface for managing students, generating exams, and grading based on answer sheets.

## Installation

1. Clone the repository:
   
   git clone https://github.com/Salamm44/ExamSheetsGenerationAndCorrection
   cd exam-evaluation-app
   

2. Set up a virtual environment and activate it
   

3. Install dependencies:
 
   pip install -r requirements.txt
   
## Dependencies

- **OpenCV**: Image processing tasks. Install: `pip install opencv-python`
- **NumPy**: Numerical operations for images. Install: `pip install numpy`
- **Tkinter**: GUI interface. (Included with Python)
- **Pillow**: Image processing. Install: `pip install Pillow`
- **pdf2image**: Converts PDFs to images. Install: `pip install pdf2image`
- **reportlab**: PDF creation. Install: `pip install reportlab`
- **os**: Used for interacting with the operating system, such as file and directory operations.
  Package: os (built-in with Python, no need to install separately)

- **ttk**: Part of tkinter, used for themed widgets.Package: ttk (included with tkinter)
- **React**:  Frontend library for the test generation tool 

## Available Scripts (for test generation)
### `npm install`
### `npm start`
Launches the development mode for the frontend  
Open [http://localhost:3000](http://localhost:3000) in your browser.


## Usage

1. **Run the Main Application**:
   python main.py
   - A GUI will open, allowing you to upload and process exam sheets.

2. **Step-by-Step Guide**:
   - **Add new student by name**: to store students information in the database 
   - **Generate Exams**: Click "Prepare Exam for All" to create exams for all students.You have to choose the output folder , where you want to save the results. You have also to choose the exam file as input file.
   - **Upload Answer Key**: Click **"Corrected Sheet"** to upload the correct answer sheet(the exam file with corrected answers).
   - **Upload Student Sheets**: Click **"Student Sheets"** to upload students' answers.
   - **View Results**: Click **"Results"** to see the grading results.
   - **Reset Database**: Click **"Reset Students"** to delete all student data.


## Database (query1.sql)
A simple `Students` database stores student IDs, names, and scores.



