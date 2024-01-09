import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd

class CSVViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        
        self.file_path = tk.StringVar()
        self.df = None

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Botón para cargar archivo
        load_button = tk.Button(self.root, text="Cargar archivo CSV", command=self.load_csv)
        load_button.pack(pady=10)

        # Frame para mostrar la tabla
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack()

        # Combobox para seleccionar la columna de filtro
        filter_label = tk.Label(self.root, text="Filtrar por columna:")
        filter_label.pack()

        self.filter_column = ttk.Combobox(self.root)
        self.filter_column.pack(pady=5)

        # Entry para ingresar el valor del filtro
        self.filter_value = tk.Entry(self.root)
        self.filter_value.pack(pady=5)

        # Botón para aplicar el filtro
        filter_button = tk.Button(self.root, text="Filtrar", command=self.apply_filter)
        filter_button.pack(pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("Archivos CSV", "*.csv")])

        if file_path:
            self.file_path.set(file_path)
            self.df = pd.read_csv(file_path)

            # Llenar el Combobox con los nombres de las columnas
            self.filter_column["values"] = list(self.df.columns)

            # Mostrar la tabla
            self.show_table()

    def show_table(self):
        # Limpiar el frame de la tabla
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Crear la tabla
        tree = ttk.Treeview(self.table_frame, columns=list(self.df.columns), show="headings")

        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        for index, row in self.df.iterrows():
            tree.insert("", index, values=list(row))

        # Añadir la tabla al frame
        tree.pack(fill="both", expand=True)

    def apply_filter(self):
        if self.df is None:
            return

        filter_column = self.filter_column.get()
        filter_value = self.filter_value.get()

        if filter_column and filter_value:
            try:
                # Aplicar el filtro según la columna seleccionada
                filtered_df = self.df[self.df[filter_column] == filter_value]
                self.df = filtered_df
                self.show_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo aplicar el filtro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewer(root)
    root.mainloop()
