import tkinter as tk
import sqlite3
from puls import *

class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(600, 600)

        self.menu = Menu(self)
        self.menu.grid(sticky='nswe')
        self.mainloop()


class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.patient_search_app = PatientSearchApp(self)
        self.pulse_box = PulseBox(self)
        self.pulse_label = PulseLabel(self.pulse_box)
        self.pulse_label.grid(row=0, column=0, sticky='nswe')
        self.pulse_label.update_puls()
        self.graf_box = GrafBox(self)

        self.patient_search_app.grid(row=0, column=0, sticky='nswe')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid(sticky='nswe')


class PatientSearchApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.search_label = tk.Label(self, text="Angiv ID:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        self.results_listbox = tk.Listbox(self, height=1)
        self.results_listbox.pack()

        self.search_button = tk.Button(self, text="Search", command=self.handle_search)
        self.search_button.pack()

        self.details_label = tk.Label(self, text="")
        self.details_label.pack()

        self.details_text = tk.Text(self, width=110, height=110)
        self.details_text.pack()

        self.results_listbox.bind("<<ListboxSelect>>", self.handle_selection)

    def handle_search(self):
        search_term = self.search_entry.get()

        conn = sqlite3.connect("EKG_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM person WHERE Person_id=?", (search_term,))
        results = cursor.fetchall()

        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, result)

        conn.close()

    def handle_selection(self, event):
        selection = self.results_listbox.get(self.results_listbox.curselection())

        self.details_label.config(text=f"Details for Patient ID {selection[0]}:")
        self.details_text.delete("1.0", tk.END)

        conn = sqlite3.connect("EKG_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM person WHERE Person_id=?", (selection[0],))
        result = cursor.fetchone()

        if result:
            self.details_text.insert(tk.END, f"Name: {result[1]}\n")

        conn.close()


class PulseBox(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Puls')
        self.grid(row=3, column=0, sticky='nswe')


class PulseLabel(tk.Label):
    def __init__(self, parent):
        super().__init__(parent, bg="white", fg="black", width=20, height=5)
        self.config(text=round(puls.getVitals()))

    def update_puls(self):
        value = round(puls.getVitals())
        self.config(text=value, font=("Helvetica", 20))
        self.after(1000, self.update_puls)


class GrafBox(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Graf', width=20, height=5)
        self.grid(row=3, column=2, sticky='nswe')
        self.entry = tk.Entry(parent, width=50)
        self.entry.grid(row=4, column=2, sticky='nswe')


App('EKG', (1200, 600))