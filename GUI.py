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

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.patient_search_app.grid(row=0, column=0, sticky='nswe')
        self.pulse_box.grid(row=1, column=0, sticky='nswe')  # Placerer PulseBox i næste række (row=1), samme kolonne (column=0)
        self.graf_box = GrafBox(self)
        self.graf_box.grid(row=1, column=1, sticky='nswe')  # Placerer GrafBox i samme række (row=1), næste kolonne (column=1)

        self.grid(sticky='nswe')


class PatientSearchApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

        self.grid_columnconfigure(0, weight=1)  # Justerer kolonne 0
        self.grid_columnconfigure(1, weight=1)  # Justerer kolonne 1
        self.grid_rowconfigure(3, weight=1)  # Justerer række 3

    def create_widgets(self):
        self.search_label = tk.Label(self, text="Angiv ID:")
        self.search_label.grid(row=0, column=0, sticky='w')  # Ændret fra pack til grid

        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, sticky='we')  # Ændret fra pack til grid

        self.results_listbox = tk.Listbox(self, height=1)
        self.results_listbox.grid(row=1, column=0, columnspan=2, sticky='nswe')  # Ændret fra pack til grid, tilføjet columnspan

        self.search_button = tk.Button(self, text="Search", command=self.handle_search)
        self.search_button.grid(row=0, column=2, sticky='e')  # Ændret fra pack til grid

        self.details_label = tk.Label(self, text="")
        self.details_label.grid(row=2, column=0, sticky='w')  # Ændret fra pack til grid

        self.details_text = tk.Text(self, width=5, height=5)
        self.details_text.grid(row=3, column=0, columnspan=3, sticky='nswe')  # Ændret fra pack til grid, tilføjet columnspan

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
        self.grid(row=1, column=1, sticky='nswe')  # Ændret fra row=3, column=2 til row=1, column=1


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
        super().__init__(parent, text='Graf', width=200, height=5)
        self.grid(row=0, column=2, rowspan=2, sticky='nswe')  # Ændret fra row=3, column=2 til row=0, column=2, tilføjet rowspan


App('EKG', (1200, 600))

