import tkinter as tk
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
        self.search_button = SearchButton(self)
        self.pulse_box = PulseBox(self)
        self.pulse_label = PulseLabel(self)
        self.pulse_label.grid(row=3, column=0, sticky='nswe')
        self.pulse_label.update_puls()
        self.graf_box = GrafBox(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid(sticky='nswe')


class SearchButton(tk.Button):
    def __init__(self, parent):
        super().__init__(parent, text='Søg', command=self.search)
        self.grid(row=0, column=20, sticky='nswe')

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(parent, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky='nswe', columnspan=3)
        self.entry.bind('<Return>', lambda event: self.search())

    def search(self):
        search_query = self.entry.get()
        print("Søger efter:", search_query)


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