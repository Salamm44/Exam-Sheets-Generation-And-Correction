import tkinter as tk
from tkinter import simpledialog, messagebox

class CorrectedSheetDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Corrected Sheet")

        tk.Label(master, text="Correction System:").grid(row=0, column=0, sticky=tk.W)
        self.correction_system_var = tk.StringVar(master)
        self.correction_system_var.set("Corrected System")
        self.correction_system_menu = tk.OptionMenu(master, self.correction_system_var, "System1")
        self.correction_system_menu.grid(row=0, column=1)

        tk.Label(master, text="Mark per Correct Answer:").grid(row=1, column=0, sticky=tk.W)
        self.answer_mark_entry = tk.Entry(master)
        self.answer_mark_entry.grid(row=1, column=1)

        return self.correction_system_menu

    def apply(self):
        self.correction_system = self.correction_system_var.get()
        self.answer_mark = int(self.answer_mark_entry.get())
        if self.correction_system == "Corrected System":
            self.corrected_system()

    def corrected_system(self):
        messagebox.showinfo("Correction System", "Marks will be deducted for incorrect answers.")