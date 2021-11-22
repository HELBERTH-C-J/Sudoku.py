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

#----CLASES----#
class Configuracion:
    #----GUI configuraciones----#
    def __init__(self,master):  
        self.ventanaConfigurar = tk.Toplevel(master)     
        self.ventanaConfigurar.geometry('500x300')      
        self.ventanaConfigurar.title('Configuración')
        self.ventanaConfigurar.resizable(False,False) 
        self.lblTitulo = tk.Label(self.ventanaConfigurar,text='Sudoku',fg='black',bg='gray',font=('System',20)).pack(fill=tk.X)

        self.nivelJuego = tk.IntVar()  
        config = open('sudoku2021configuracion.dat','rb')    
        configuracion = pickle.load(config)                     

        self.nivelJuego.set(str(configuracion[0])) 
        config.close()      

        self.lblJuego = tk.Label(self.ventanaConfigurar,text='Nivel:',font=('System',12)).place(x=10,y=45)
        self.check1 = tk.Radiobutton(self.ventanaConfigurar,text="Fácil", font=('System',12),value = 1, variable=self.nivelJuego \
                                                            , command=self.configuraciones \
                                                            ).place(x=55,y=45)

        self.check2 = tk.Radiobutton(self.ventanaConfigurar,text="Intermedio", font=('System',12),value = 2, variable=self.nivelJuego \
                                                            ,command=self.configuraciones \
                                                            ).place(x=55,y=65)

        self.check3 = tk.Radiobutton(self.ventanaConfigurar,text="Díficil",font=('System',12), value = 3, variable=self.nivelJuego \
                                                            ,command=self.configuraciones \
                                                            ).place(x=55,y=85)

        self.relojConfig = tk.IntVar()     
        config = open('sudoku2021configuracion.dat','rb')
        configuracion = pickle.load(config)
        self.relojConfig.set(str(configuracion[1]))
        config.close()

        self.lblReloj = tk.Label(self.ventanaConfigurar,text='Reloj:',font=('System',12)).place(x=10,y=115)
        self.chkConTiempo = tk.Radiobutton(self.ventanaConfigurar,text="Si", font=('System',12), value = 1, variable=self.relojConfig \
                                                    ,command=self.configuraciones\
                                                    ).place(x=55,y=115)

        self.chkSinTiempo = tk.Radiobutton(self.ventanaConfigurar,text="No", font=('System',12), value = 2, variable=self.relojConfig \
                                                    ,command=self.configuraciones\
                                                    ).place(x=55,y=135)

        self.chkTimer = tk.Radiobutton(self.ventanaConfigurar,text="Timer", font=('System',12), value = 3, variable=self.relojConfig \
                                                    ,command=self.configuraciones\
                                                    ).place(x=55,y=155)
        
        # TEMPORIZADOR VARIABLES
        self.hour= tk.StringVar()
        self.minute= tk.StringVar()
        self.second= tk.StringVar()

        #Se configura las variables en el valor default
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")
        self.hourLabel =    tk.Label(self.ventanaConfigurar,text='Horas',   width=8,font=('System',12)).place(x=285,y=110)
        self.minuteLabel =  tk.Label(self.ventanaConfigurar,text='Minutos', width=8,font=('System',12)).place(x=337,y=110)
        self.secondLabel =  tk.Label(self.ventanaConfigurar,text='Segundos',width=8,font=('System',12)).place(x=399,y=110)
        self.hourEntry=     tk.Entry(self.ventanaConfigurar,                width=3, font=("System",18,""),
                            textvariable=self.hour)
        
        self.hourEntry.place(x=300,y=135)
            
        self.minuteEntry= tk.Entry(self.ventanaConfigurar, width=3, font=("System",18,""),
                            textvariable=self.minute)
        self.minuteEntry.place(x=350,y=135)
            
        self.secondEntry= tk.Entry(self.ventanaConfigurar, width=3, font=("System",18,""),
                            textvariable=self.second)
        self.secondEntry.place(x=400,y=135)

        self.btnAceptar = tk.Button(self.ventanaConfigurar,text='Aceptar',command=self.confirmar).place(x=35,y=235)
    #----Guarda configuraciones----#
    def configuraciones(self):
        self.ventanaConfigurar.wait_window()    #espera la ventana a que se cierre

        # Se asignan variables tomando los datos de los radioButton
        nivelJuego = self.nivelJuego.get()      
        relojConfig = self.relojConfig.get()

        hora = self.hour.get()
        minuto = self.minute.get()
        segundo = self.second.get()

        self.configuracion = open('sudoku2021configuracion.dat','wb')    #se abre el archivo para guardar la configuración
        pickle.dump((nivelJuego,relojConfig,hora,minuto,segundo),self.configuracion)#se graban las variables cada vez que se ingrese a la ventana Configuración
        self.configuracion.close()
        return (nivelJuego,relojConfig,hora,minuto,segundo)     #retorna las variables
    #----Confirmar configuraciones----#
    def confirmar(self):
        self.ventanaConfigurar.destroy()
        
class sudoku(tk.Frame):                  #se crea la clase padre
    #----Método Constructor----#
    def __init__(self,master=None):
        super().__init__(master)
        self.master =  master   #esta variable almacena la ventana principal
        self.master.title('Sudoku')
        self.master.geometry('600x600')
        self.master.resizable(False,False) 

        # PARTIDAS DE JUEGO #
        partidas= open('sudoku2021partidas.dat','wb')
        #graba las partidas de juego
        pickle.dump([[
            [3, 0, 8, 0, 1, 4, 0, 0, 9],
            [0, 0, 2, 0, 6, 0, 1, 7, 4],
            [7, 1, 0, 5, 9, 0, 8, 0, 0],
            [0, 0, 0, 9, 0, 3, 4, 1, 7],
            [5, 9, 0, 2, 4, 0, 3, 0, 0],
            [4, 3, 7, 0, 0, 6, 0, 5, 0],
            [1, 0, 5, 4, 0, 0, 0, 3, 8],
            [0, 2, 0, 0, 3, 5, 7, 0, 1],
            [0, 4, 3, 6, 0, 1, 0, 9, 0]
            ],
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            [
            [0, 0, 0, 0, 0, 4, 2, 0, 0],
            [2, 0, 0, 5, 1, 0, 0, 0, 0],
            [7, 8, 0, 0, 0, 6, 4, 0, 0],
            [5, 9, 0, 0, 0, 7, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 2, 0, 0, 0, 9, 5],
            [0, 0, 7, 4, 0, 0, 0, 3, 2],
            [0, 0, 0, 0, 3, 9, 0, 0, 1],
            [0, 0, 3, 1, 0, 0, 0, 0, 0]
            ],
            [
            [0, 0, 5, 8, 0, 0, 0, 0, 2],
            [8, 0, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 9, 5, 0, 0, 0, 7, 8],
            [7, 0, 0, 3, 0, 0, 1, 0, 0],
            [0, 4, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 6, 0, 0, 8, 0, 0, 3],
            [6, 9, 0, 0, 0, 3, 7, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 9],
            [1, 0, 0, 0, 0, 7, 2, 0, 0]
            ]],partidas)
        partidas.close()

        #graba una lista con tres listas diferenciando cada una por nivel de dificultad
        top10 = open('sudoku2021top10.dat','wb')
        pickle.dump([[],[],[]],top10)
        top10.close()

        #llama al método que mantiene toda la interfaz principal del juego
        self.inicializar_gui()

        # VARIABLES DE LA CONFIGURACION POR DEFAULT #
        self.nivelJuego = tk.IntVar()
        self.nivelJuego.set('1')
        self.relojConfig = tk.IntVar()
        self.relojConfig.set('1')
        self.configuraciones = (self.nivelJuego.get(),self.relojConfig.get())    #se crea una lista que guarde la configuración por default 

        #TEMPORIZADOR VARIABLES
        self.hour=tk.StringVar()
        self.minute=tk.StringVar()
        self.second=tk.StringVar()
        #Se configura las variables en el valor default del reloj
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")

        self.configuracion = open('sudoku2021configuracion.dat','wb')
        pickle.dump(self.configuraciones,self.configuracion)    #grabo la configuración en el archivo .dat
        self.configuracion.close()
    #----GUI----# 
    def inicializar_gui(self):
        self.lblTitulo = tk.Label(self.master,text='Sudoku',fg='black',bg='gray',font=('System',25)).pack(fill=tk.X)
        # Se crea el menú de juego llamando cada uno al método correspondiente #
        self.barMenu = tk.Menu(self.master)
        self.barMenu.add_command(label='Jugar')
        self.barMenu.add_command(label='Configuracion', command=self.configurar)
        self.barMenu.add_command(label='Ayuda',         command=self.ayuda)
        self.barMenu.add_command(label='Acerca De',     command=self.acercaDe)
        self.barMenu.add_command(label='Salir',         command=self.salir)
        self.master.config(menu=self.barMenu)
    #----Configurar----#
    def configurar(self):
        configurar = Configuracion(self.master)                 #en configuración se llama a la clase hija "Configuracion" enviando la ventana principal como parámetro
        self.configuraciones = configurar.configuraciones()
    #----Ayuda----#
    def ayuda(self):
        # Esta opción la usaremos para que el usuario pueda ver el Manual de Usuario directamente en la computadora (despliega el pdf  respectivo). 
        path = 'manual_de_usuario_sudoku.pdf'
        os.system(path)
    #----Acerca de----#
    def acercaDe(self):
        self.ventanaInfo = tk.Tk()
        self.ventanaInfo.geometry('800x300')
        self.ventanaInfo.title('Información del programa')
        self.lblTitulo =    tk.Label(self.ventanaInfo,text='Sudoku',fg='black',bg='gray',       font=('System',20)).pack(fill=tk.X) 
        Autor =             tk.Label(self.ventanaInfo,text='Autor del programa:',               font=('Courier New',16,'bold')).place(x=0,y=60)
        nombreAutor =       tk.Label(self.ventanaInfo,text='Helberth Fabricio Cubillo Jarquin', font=('Courier New',16)).place(x=300,y=60)
        programa =          tk.Label(self.ventanaInfo,text='Nombre del programa:',              font=('Courier New',16,'bold')).place(x=0,y=90)
        nombrePrograma =    tk.Label(self.ventanaInfo,text='Juego sudoku',                      font=('Courier New',16)).place(x=300,y=90)
        version =           tk.Label(self.ventanaInfo,text='Versión:',                          font=("Courier New",16,'bold')).place(x=0,y=120)
        nombreVersion =     tk.Label(self.ventanaInfo,text='Python 3.9.6',                      font=('Courier New',16)).place(x=300,y=120)
        creacion =          tk.Label(self.ventanaInfo,text='Fecha de creación:',                font=('Courier New',16,'bold')).place(x=0,y=150)
        fechaCreacion =     tk.Label(self.ventanaInfo,text='18 de noviembre del 2021',          font=('Courier New',16)).place(x=300,y=150)
    #----Salir----#
    def salir(self):
        respuesta= messagebox.askyesno("Cuidado", "¿Quiere salir del programa?")
        if respuesta==True:
            self.master.destroy()

#----PROGRAMA PRINCIPAL----#
def main():
    app = tk.Tk()
    ventanaPrincipal = sudoku(app)
    app.mainloop()

if __name__ == "__main__":
    main()
