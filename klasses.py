import tkinter as tk

class App(tk.Tk):
    def __init__(self, title, size,):
        #main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(600,600)

        #widgets
        self.menu=Menu(self)

        #run
        self.mainloop()

class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill='both') # her kan der køres grid eller hvad der passer ind til vores
        self.create_Button()
        self.search_Button()

    def create_Button(self):
        menu_Button1=tk.Button(self,text='Tidligere målinger')

        self.columnconfigure((0,1,2),weight=1,uniform='a')
        self.rowconfigure((0,1,2,3,4),weight=1, uniform='a')

        menu_Button1.grid(row=0, column=0, sticky='nswe',columnspan=2)
        #search_button.grid(row=0,column=0, sticky='nswe')

    def search_Button(self):
        search_query = entry.get()
        print("Søger efter:", search_query)

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.search_button = tk.Button(self, text="Søg", command=search)
        self.search_button.pack()

        



App('EKG',(1200,600))


