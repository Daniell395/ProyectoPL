import tkinter as tk
from tkinter import ttk
from subprocess import Popen

class UnificadorInterfaz:
    def __init__(self, root):
        print("\n\n\t\t\tLas iteraciones del Método de Dos Fases se mostrarán por este medio")
        print("\t|-----------------------------------------------------------------------------------------------------|")
        self.root = root
        self.root.title("Inv. de Operaciones")

        # Configurar el contenedor
        container = ttk.Frame(root)
        container.pack(expand=True, fill="both")

        # Botón para ejecutar archivo1.exe (azul)
        self.boton1 = ttk.Button(container, text="Método Gráfico", style="BotonAzul.TButton", command=self.ejecutar_archivo1)
        self.boton1.pack(side="left", expand=True, fill="both")

        # Botón para ejecutar archivo2.exe (rojo)
        self.boton2 = ttk.Button(container, text="Método de Dos \n         Fases", style="BotonRojo.TButton", command=self.ejecutar_archivo2)
        self.boton2.pack(side="right", expand=True, fill="both")

        # Configurar estilos
        style = ttk.Style()
        style.configure("BotonAzul.TButton", foreground="blue", font=("TkDefaultFont", 12, "bold"))
        style.configure("BotonRojo.TButton", foreground="red", font=("TkDefaultFont", 12, "bold"))

    def ejecutar_archivo1(self):
        # Reemplaza 'archivo1.exe' con el nombre de tu primer archivo ejecutable
        Popen(['met_grafico.exe'])

    def ejecutar_archivo2(self):
        # Reemplaza 'archivo2.exe' con el nombre de tu segundo archivo ejecutable
        Popen(['Met_DosFases.exe'])

root = tk.Tk()
app = UnificadorInterfaz(root)
root.geometry("300x200")
root.resizable(False, False)
root.mainloop()
