from tkinter import Toplevel, Label, Entry, Button

class CorrectedSheetDialog:
    def __init__(self, root):
        self.dialog = Toplevel(root)
        self.dialog.title("Corrected Sheet Details")

        Label(self.dialog, text="Correction System:").grid(row=0, column=0, padx=10, pady=10)
        self.correction_system = Entry(self.dialog)
        self.correction_system.grid(row=0, column=1, padx=10, pady=10)

        Label(self.dialog, text="Mark per Correct Answer:").grid(row=1, column=0, padx=10, pady=10)
        self.answer_mark = Entry(self.dialog)
        self.answer_mark.grid(row=1, column=1, padx=10, pady=10)

        Button(self.dialog, text="OK", command=self.dialog.destroy).grid(row=2, columnspan=2, pady=10)
