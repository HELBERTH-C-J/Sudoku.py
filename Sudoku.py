#¿Que hace el programa?
#En el se un programa en el cual se ejecuta el juego sudoku mediante la gui de tkinter 
#Autor: Helberth Cubillo Jarquin - 2021110838
#Fecha de creación 18 de noviembre del 2021 a las 08:10 am
#Ultima fecha de actualizacion 30 de noviembre del 2021 a las x:xx pm
#Version de Python 3.9.6.

#----MODULOS----#
import os
import time
import pickle
import random
import tkinter as tk
from tkinter import messagebox

#----CLAESES----#





#----PROGRAMA PRINCIPAL----#
def main():
    app = tk.Tk()
    ventanaPrincipal = sudoku(app)
    app.mainloop()

if __name__ == "__main__":
    main()
