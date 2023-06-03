import tkinter as tk
from puls import *


class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(600, 600)

        self.menu = Menu(self)

        self.mainloop()

class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        self.create_Button()
        self.search_Button()
        self.pulse_box()
        self.update_puls()
        self.graf()

    def create_Button(self):
        menu_Button1 = tk.Button(self, text='Tidligere målinger')
        menu_Button1.grid(row=2, column=0, sticky='nswe')

    def search_Button(self):
        def search():
            search_query = self.entry.get()
            print("Søger efter:", search_query)

        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=0, sticky='nswe', columnspan=3)

        search_button = tk.Button(self, text="Søg", command=search)
        search_button.grid(row=0, column=4, sticky='nswe')

    def pulse_box(self):
        self.label1 = tk.Label(self, text='Puls')
        self.label1.grid(row=3, column=0, sticky='nswe')

    def update_puls(self):
        value=round(puls.getVitals())
        self.label2=tk.Label(self, text=value,width=20, height=5)
        self.label2.config(text=value)
        self.after(1000, self.update_puls)
        self.label2.grid(row=4, column=0, sticky='nswe',pady=2)

    def graf(self):
        self.label_graf = tk.Label(self, text='Graf',width=20, height=5)
        self.label_graf.grid(row=3, column=2, sticky='nswe')
        self.entry = tk.Entry(self, width=5)
        self.entry.grid(row=4, column=2, sticky='nswe')


App('EKG', (1200, 600))
