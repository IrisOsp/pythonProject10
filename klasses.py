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
        self.pack(expand=False, fill='none') # her kan der køres grid eller hvad der passer ind til vores
        self.create_Button()
        self.search_Button()
        self.pulse_box()
        self.graf()

    def create_Button(self):
        menu_Button1=tk.Button(self,text='Tidligere målinger',width=10, height=2)

        self.columnconfigure((0,1,2),weight=1,uniform='a')
        self.rowconfigure((0,1,2,3,4),weight=1, uniform='a')

        menu_Button1.grid(row=1, column=0, sticky='nswe')

    def search_Button(self):
            def search():
                search_query = self.entry.get()
                print("Søger efter:", search_query)

            self.entry = tk.Entry(self)
            self.entry.grid(row=0, column=0, sticky='nswe', columnspan=3)

            search_button = tk.Button(self, text="Søg", command=search,width=5, height=2)
            search_button.grid(row=0, column=2, sticky='nswe')
        
    def pulse_box(self):
        self.label=tk.Label(self, text='Puls',width=10, height=2)
        self.label.grid(row=2, column=0, sticky='nswe')
        self.entry = tk.Entry(self, width=5)
        self.entry.grid(row=3, column=0, sticky='nswe')


    def graf(self):
        self.label=tk.Label(self, text='Graf',width=10, height=2)
        self.label.grid(row=2, column=2, sticky='nswe')
        self.entry = tk.Entry(self, width=5)
        self.entry.grid(row=3, column=2, sticky='nswe')
        


App('EKG',(1200,600))


