import tkinter as tk

def search():
    search_query = entry.get()
    print("Søger efter:", search_query)

window = tk.Tk()

entry = tk.Entry(window)
entry.pack()

search_button = tk.Button(window, text="Søg", command=search)
search_button.pack()

window.mainloop()
