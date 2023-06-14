from klasser7 import *
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
        self.pulse_box.grid(row=1, column=0, sticky='nswe')
        self.graf_box = GrafBox(self)
        self.graf_box.grid(row=1, column=1, sticky='nswe')

        self.grid(sticky='nswe')


class PatientSearchApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def create_widgets(self):
        self.search_label = tk.Label(self, text="Angiv ID:")
        self.search_label.grid(row=0, column=0, sticky='w')

        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, sticky='we')

        self.results_listbox = tk.Listbox(self, height=1)
        self.results_listbox.grid(row=1, column=0, columnspan=2, sticky='nswe')

        self.search_button = tk.Button(self, text="Search", command=self.handle_search)
        self.search_button.grid(row=0, column=2, sticky='e')

        self.details_label = tk.Label(self, text="")
        self.details_label.grid(row=2, column=0, sticky='w')

        self.details_text = tk.Text(self, width=5, height=5)
        self.details_text.grid(row=3, column=0, columnspan=3, sticky='nswe')

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
        self.grid(row=1, column=1, sticky='nswe')


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
        self.grid(row=0, column=2, rowspan=2, sticky='nswe')

        self.graph_frame = MyGraph(self, b)  # Replace 'buffer' with 'b'
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        sensor_thread = Thread(target=sensor_thread_func, args=(b, self.graph_frame.que, Database()))
        sensor_thread.start()

        self.graph_frame.update_graph()

class Graph:
    def __init__(self, ax):
        self.buffer = []
        self.ax = ax

    def plot_graph(self, obs):
        self.buffer.extend(obs)
        if len(self.buffer) >= 800:
            x = list(range(len(self.buffer) - 800, len(self.buffer)))
            y = self.buffer[-800:]
            self.ax.clear()
            self.ax.plot(x, y)
            self.buffer = self.buffer[-800:]

class MyGraph(tk.Frame):
    def __init__(self, parent, buffer):
        tk.Frame.__init__(self, parent)
        self.master = parent
        self.que = que(buffer)
        self.figure = plt.figure(figsize=(5, 2))
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_visible(True)
        self.ax.yaxis.set_visible(True)
        self.ax.tick_params(axis='both', which='both', labelsize=8)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph = Graph(self.ax)

    def update_graph(self):
        data = self.que.getData()
        self.graph.plot_graph(data)
        self.canvas.draw()
        self.after(1000, self.update_graph)

App('EKG', (1200, 600))
