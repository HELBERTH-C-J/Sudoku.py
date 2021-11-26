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
     
     
        
class sudoku(tk.Frame):                  
    #----Método Constructor----#
    def __init__(self,master=None):
        super().__init__(master)
        self.master =  master   #esta variable almacena la ventana principal
        self.master.title('Sudoku')
        self.master.geometry('700x700')
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
        self.barMenu.add_command(label='Jugar',         command=self.juego)
        self.barMenu.add_command(label='Configuracion', command=self.configurar)
        self.barMenu.add_command(label='Ayuda',         command=self.ayuda)
        self.barMenu.add_command(label='Acerca De',     command=self.acercaDe)
        self.barMenu.add_command(label='Salir',         command=self.salir)
        self.master.config(menu=self.barMenu)
    #----Configuraciones----#
    def configurar(self):
        configurar = Configuracion(self.master)                 #en configuración se llama a la clase hija "Configuracion" enviando la ventana principal como parámetro
        self.configuraciones = configurar.configuraciones()
    #----GUI juego----#
    def juego(self):
        # CONFIGURACION DEL NIVEL DE JUEGO #
        self.lblNivelJuego =    tk.Label(self.master,text='Nivel: Fácil',                   font=('System',16),width=50)
        self.lblNivelJuego.place(x=100,y=50)

        self.lblNombre = tk.Label(self.master,text='Nombre del jugador',                    font=('System',12))
        self.lblNombre.place(x=15,y=75)
        self.txtNombre =        tk.Entry(self.master,width=31,                              font=('System',12))
        self.txtNombre.place(x=185,y=80)
        # BOTONES DE LA INTERACCIÓN CON EL JUEGO #
        self.btnIniciarJuego =  tk.Button(self.master,text='Iniciar juego',     bg='red',   font=('System',10),command=self.inicioJuego)
        self.btnIniciarJuego.place(x=5,y=550)

        # Estos botones se mantienen inhabilitados hasta que se inicie una partida
        self.btnBorrarJugada =  tk.Button(self.master,text='Rehacer jugada',    bg='gray',  font=('System',10),state=tk.DISABLED)
        self.btnBorrarJugada.place(x=265,y=600)
        self.btnBorrarJugada =  tk.Button(self.master,text='Deshacer jugada',   bg='blue',  font=('System',10),state=tk.DISABLED)
        self.btnBorrarJugada.place(x=265,y=550)
        self.btnTerminarJuego = tk.Button(self.master,text='Terminar juego',    bg='orange',font=('System',10),state=tk.DISABLED)
        self.btnTerminarJuego.place( x=125,y=550)
        self.btnBorraJuego =    tk.Button(self.master,text=' Borrar juego ',    bg='violet',font=('System',10),state=tk.DISABLED)
        self.btnBorraJuego.place(x=405,y=550)
        self.btnTopLevel =      tk.Button(self.master,text='    Top 10    ',    bg='yellow',font=('System',10))
        self.btnTopLevel.place(x=535,y=550)
        
        self.btnGuardarJuego =  tk.Button(self.master,text='Guardar juego',     bg='purple',font=('System',10),state=tk.DISABLED)
        self.btnGuardarJuego.place(x=405,y=600)
        self.btnCargarJuego =    tk.Button(self.master,text='Cargar juego',     bg='pink',  font=('System',10),state=tk.DISABLED)
        self.btnCargarJuego.place(x=535,y=600)
        
        #-------------------------------------------------------- CUADRICULA --------------------------------------------------------#
        self.btnPos00 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos00))
        self.btnPos00.place(x=20,y=110)
        self.btnPos01 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos01))
        self.btnPos01.place(x=70,y=110)
        self.btnPos02 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos02))
        self.btnPos02.place(x=120,y=110)
        self.btnPos03 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos03))
        self.btnPos03.place(x=170,y=110)
        self.btnPos04 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos04))
        self.btnPos04.place(x=220,y=110)
        self.btnPos05 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos05))
        self.btnPos05.place(x=270,y=110)
        self.btnPos06 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos06))
        self.btnPos06.place(x=320,y=110)
        self.btnPos07 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos07))
        self.btnPos07.place(x=370,y=110)
        self.btnPos08 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos08))
        self.btnPos08.place(x=420,y=110)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos10 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos10))
        self.btnPos10.place(x=20,y=155)
        self.btnPos11 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos11))
        self.btnPos11.place(x=70,y=155)
        self.btnPos12 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos12))
        self.btnPos12.place(x=120,y=155)
        self.btnPos13 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos13))
        self.btnPos13.place(x=170,y=155)
        self.btnPos14 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos14))
        self.btnPos14.place(x=220,y=155)
        self.btnPos15 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos15))
        self.btnPos15.place(x=270,y=155)
        self.btnPos16 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos16))
        self.btnPos16.place(x=320,y=155)
        self.btnPos17 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos17))
        self.btnPos17.place(x=370,y=155)
        self.btnPos18 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos18))
        self.btnPos18.place(x=420,y=155)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos20 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos20))
        self.btnPos20.place(x=20,y=200)
        self.btnPos21 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos21))
        self.btnPos21.place(x=70,y=200)
        self.btnPos22 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos22))
        self.btnPos22.place(x=120,y=200)
        self.btnPos23 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos23))
        self.btnPos23.place(x=170,y=200)
        self.btnPos24 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos24))
        self.btnPos24.place(x=220,y=200)
        self.btnPos25 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos25))
        self.btnPos25.place(x=270,y=200)
        self.btnPos26 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos26))
        self.btnPos26.place(x=320,y=200)
        self.btnPos27 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos27))
        self.btnPos27.place(x=370,y=200)    
        self.btnPos28 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos28))
        self.btnPos28.place(x=420,y=200)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos30 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos30))
        self.btnPos30.place(x=20,y=245)
        self.btnPos31 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos31))
        self.btnPos31.place(x=70,y=245)
        self.btnPos32 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos32))
        self.btnPos32.place(x=120,y=245)
        self.btnPos33 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos33))
        self.btnPos33.place(x=170,y=245)
        self.btnPos34 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos34))
        self.btnPos34.place(x=220,y=245)
        self.btnPos35 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos35))
        self.btnPos35.place(x=270,y=245)
        self.btnPos36 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos36))
        self.btnPos36.place(x=320,y=245)
        self.btnPos37 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos37))
        self.btnPos37.place(x=370,y=245)
        self.btnPos38 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos38))
        self.btnPos38.place(x=420,y=245)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos40 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos40))
        self.btnPos40.place(x=20,y=290)
        self.btnPos41 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos41))
        self.btnPos41.place(x=70,y=290)
        self.btnPos42 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos42))
        self.btnPos42.place(x=120,y=290)
        self.btnPos43 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos43))
        self.btnPos43.place(x=170,y=290)
        self.btnPos44 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos44))
        self.btnPos44.place(x=220,y=290)
        self.btnPos45 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos45))
        self.btnPos45.place(x=270,y=290)
        self.btnPos46 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos46))
        self.btnPos46.place(x=320,y=290)
        self.btnPos47 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos47))
        self.btnPos47.place(x=370,y=290)
        self.btnPos48 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos48))
        self.btnPos48.place(x=420,y=290)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos50 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos50))
        self.btnPos50.place(x=20,y=335)
        self.btnPos51 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos51))
        self.btnPos51.place(x=70,y=335)
        self.btnPos52 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos52))
        self.btnPos52.place(x=120,y=335)
        self.btnPos53 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos53))
        self.btnPos53.place(x=170,y=335)
        self.btnPos54 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos54))
        self.btnPos54.place(x=220,y=335)
        self.btnPos55 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos55))
        self.btnPos55.place(x=270,y=335)
        self.btnPos56 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos56))
        self.btnPos56.place(x=320,y=335)
        self.btnPos57 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos57))
        self.btnPos57.place(x=370,y=335)
        self.btnPos58 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos58))
        self.btnPos58.place(x=420,y=335)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos60 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos60))
        self.btnPos60.place(x=20,y=380)
        self.btnPos61 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos61))
        self.btnPos61.place(x=70,y=380)
        self.btnPos62 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos62))
        self.btnPos62.place(x=120,y=380)
        self.btnPos63 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos63))
        self.btnPos63.place(x=170,y=380)
        self.btnPos64 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos64))
        self.btnPos64.place(x=220,y=380)
        self.btnPos65 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos65))
        self.btnPos65.place(x=270,y=380)
        self.btnPos66 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos66))
        self.btnPos66.place(x=320,y=380)    
        self.btnPos67 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos67))
        self.btnPos67.place(x=370,y=380)
        self.btnPos68 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos68))
        self.btnPos68.place(x=420,y=380)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos70 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos70))
        self.btnPos70.place(x=20,y=425)
        self.btnPos71 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos71))
        self.btnPos71.place(x=70,y=425)
        self.btnPos72 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos72))
        self.btnPos72.place(x=120,y=425)
        self.btnPos73 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos73))
        self.btnPos73.place(x=170,y=425)
        self.btnPos74 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos74))
        self.btnPos74.place(x=220,y=425)
        self.btnPos75 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos75))
        self.btnPos75.place(x=270,y=425)
        self.btnPos76 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos76))
        self.btnPos76.place(x=320,y=425)
        self.btnPos77 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos77))
        self.btnPos77.place(x=370,y=425)
        self.btnPos78 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos78))
        self.btnPos78.place(x=420,y=425)
        #------------------------------------------------------------------------------------------------------------------------------#
        self.btnPos80 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos80))
        self.btnPos80.place(x=20,y=470)
        self.btnPos81 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos81))
        self.btnPos81.place(x=70,y=470)
        self.btnPos82 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos82))
        self.btnPos82.place(x=120,y=470)
        self.btnPos83 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos83))
        self.btnPos83.place(x=170,y=470)
        self.btnPos84 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos84))
        self.btnPos84.place(x=220,y=470)
        self.btnPos85 = tk.Button(self.master,bg='gray',    font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos85))
        self.btnPos85.place(x=270,y=470)
        self.btnPos86 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos86))
        self.btnPos86.place(x=320,y=470)
        self.btnPos87 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos87))
        self.btnPos87.place(x=370,y=470)
        self.btnPos88 = tk.Button(self.master,bg='white',   font=('System'),width=5,height=2,command=lambda:self.cuadricula(self.btnPos88))
        self.btnPos88.place(x=420,y=470)
        
        #------------------------------------------------------------------------------------------------------------------------------#
        self.casillas = [(self.btnPos00,self.btnPos01,self.btnPos02,self.btnPos03,self.btnPos04,self.btnPos05,self.btnPos06,self.btnPos07,self.btnPos08,
                          self.btnPos10,self.btnPos11,self.btnPos12,self.btnPos13,self.btnPos14,self.btnPos15,self.btnPos16,self.btnPos17,self.btnPos18,
                          self.btnPos20,self.btnPos21,self.btnPos22,self.btnPos23,self.btnPos24,self.btnPos25,self.btnPos26,self.btnPos27,self.btnPos28,
                          self.btnPos30,self.btnPos31,self.btnPos32,self.btnPos33,self.btnPos34,self.btnPos35,self.btnPos36,self.btnPos37,self.btnPos38,
                          self.btnPos40,self.btnPos41,self.btnPos42,self.btnPos43,self.btnPos44,self.btnPos45,self.btnPos46,self.btnPos47,self.btnPos48,
                          self.btnPos50,self.btnPos51,self.btnPos52,self.btnPos53,self.btnPos54,self.btnPos55,self.btnPos56,self.btnPos57,self.btnPos58,
                          self.btnPos60,self.btnPos61,self.btnPos62,self.btnPos63,self.btnPos64,self.btnPos65,self.btnPos66,self.btnPos67,self.btnPos68,
                          self.btnPos70,self.btnPos71,self.btnPos72,self.btnPos73,self.btnPos74,self.btnPos75,self.btnPos76,self.btnPos77,self.btnPos78,
                          self.btnPos80,self.btnPos81,self.btnPos82,self.btnPos83,self.btnPos84,self.btnPos85,self.btnPos86,self.btnPos87,self.btnPos88,)]
        
        # CONFIGURACION DEL RELOJ #
        # EVALUA LA CONFIGURACIÓN DEL RELOJ PARA AJUSTAR EN VENTANA PRINCIPAL EL RELOJ (TIMER, CRONÓMETRO O SIN RELOJ) #
        if self.configuraciones[1] == 1:
            # CRONÓMETRO #
            self.hourLabel = tk.Label(self.master,text='Horas',width=8,font=('System',12))
            self.hourLabel.place(x=40,y=600)
            self.minuteLabel = tk.Label(self.master,text='Minutos',width=8,font=('System',12))
            self.minuteLabel.place(x=97,y=600)
            self.secondLabel = tk.Label(self.master,text='Segundos',width=8,font=('System',12))
            self.secondLabel.place(x=165,y=600)
            
            self.time = tk.Label(self.master, text= '0   :   0  :   0 ', font=('System',25,''))
            self.time.place(x=55,y=625)

        elif self.configuraciones[1] == 2:
            # SIN RELOJ #
            self.lblOcultar = tk.Label(self.master,text='',width=40,height=10)
            self.lblOcultar.place(x=40,y=600)
        else:
            # TEMPORIZADOR # 
            self.hourLabel = tk.Label(self.master,text='Horas',width=8,font=('System',12))
            self.hourLabel.place(x=40,y=600)
            self.minuteLabel = tk.Label(self.master,text='Minutos',width=8,font=('System',12))
            self.minuteLabel.place(x=97,y=600)
            self.secondLabel = tk.Label(self.master,text='Segundos',width=8,font=('System',12))
            self.secondLabel.place(x=165,y=600)
            
            # Uso deL Entry para recibir información del usuario
            self.hourEntry= tk.Entry(self.master, width=3, font=("System",18,""),
                            textvariable=self.hour)
            self.hourEntry.place(x=60,y=625)
            self.hour.set(self.configuraciones[3])      #se asignan los valores que contenga si el usuario pone el timer en la configuración
            
            self.minuteEntry= tk.Entry(self.master, width=3, font=("System",18,""),
                            textvariable=self.minute)
            self.minuteEntry.place(x=110,y=625)
            self.minute.set(self.configuraciones[4])    #se asignan los valores que contenga si el usuario pone el timer en la configuración
            
            self.secondEntry= tk.Entry(self.master, width=3, font=("System",18,""),
                            textvariable=self.second)
            self.secondEntry.place(x=160,y=625)
            self.second.set(self.configuraciones[5])

            
        self.btn1 = tk.Button(self.master,text='1',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(1),state=tk.DISABLED)
        self.btn1.place(x=500,y=120)
        self.btn2= tk.Button(self.master,text='2',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(2),state=tk.DISABLED)
        self.btn2.place(x=560,y=120)
        self.btn3 = tk.Button(self.master,text='3',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(3),state=tk.DISABLED)
        self.btn3.place(x=620,y=120)
        self.btn4 = tk.Button(self.master,text='4',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(4),state=tk.DISABLED)
        self.btn4.place(x=500,y=200)
        self.btn5 = tk.Button(self.master,text='5',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(5),state=tk.DISABLED)
        self.btn5.place(x=560,y=200)
        self.btn6 = tk.Button(self.master,text='6',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(6),state=tk.DISABLED)
        self.btn6.place(x=620,y=200)
        self.btn7 = tk.Button(self.master,text='7',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(7),state=tk.DISABLED)
        self.btn7.place(x=500,y=280)
        self.btn8 = tk.Button(self.master,text='8',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(8),state=tk.DISABLED)
        self.btn8.place(x=560,y=280)
        self.btn9 = tk.Button(self.master,text='9',font=('System',12),activebackground='green',height=2,width=4,command=lambda:self.botones(9),state=tk.DISABLED)
        self.btn9.place(x=620,y=280)

        # LISTA CON LOS BOTONES DEL JUEGO #
        self.botonesJuego = [self.btn1,self.btn2,self.btn3,self.btn4,self.btn5,self.btn6,self.btn7,self.btn8,self.btn9]
    #----Inicializar juego----#
    def inicioJuego(self):
        # Variables globales
        global proceso
        global running
        global h,m,s

        # VALIDACIONES DE BOTONES HABILITADOS y DESABILITADOS #
        self.btnIniciarJuego.configure(state=tk.DISABLED)
        self.btnGuardarJuego.configure(state=tk.NORMAL)
        self.btnCargarJuego.configure(state=tk.NORMAL)
        self.btnBorraJuego.configure(state=tk.NORMAL)
        self.btnTerminarJuego.configure(state=tk.NORMAL)
        self.btnBorrarJugada.configure(state=tk.NORMAL)

        # SE HABILITAN LOS BOTONES DE JUEGO 
        for i in self.botonesJuego:
            i.configure(state=tk.NORMAL)

        # Se evalua si el usuario escribio su nombre, de lo contrario el juego no puede iniciar 
        if self.txtNombre.get() == '':
            messagebox.showerror('Nombre del Jugador','Debe de ingresar el nombre del jugador')
            self.juego()
            return 
        else:
            configuracion = open('sudoku2021configuracion.dat','rb')
            x = pickle.load(configuracion)
            top10 = open('sudoku2021top10.dat','rb')
            tops = pickle.load(top10)
            jugadores = str(self.txtNombre.get())
            # El nombre es guardado en la lista correspondiente al nivel de juego
            if x[0] == 1:
                tops[0].append(jugadores)
            elif x[0] == 2:
                tops[1].append(jugadores)
            elif x[0] == 3:
                tops[2].append(jugadores)
            configuracion.close()

        # Evalua la configuración del reloj
        if self.configuraciones[1] == 3:
            # TEMPORIZADOR
            try:
                # Para el timer las horas pueden estar entre 0 y  2, los minutos entre 0 y 59 y los  segundos  entre  0  y  59.
                # RESTRICCIONES DE TIEMPO
                if int(self.hour.get()) > 2:
                    messagebox.showerror('Tiempo Incorrecto','Por favor ingresar un intervalo de tiempo correcto')
                    self.juego()
                    return
                if int(self.hour.get()) >= 2 and int(self.minute.get()) > 0:
                    messagebox.showerror('Tiempo Incorrecto','Por favor ingresar un intervalo de tiempo correcto')
                    self.juego()
                    return 
                if int(self.hour.get()) >= 2 and int(self.second.get()) > 0:
                    messagebox.showerror('Tiempo Incorrecto','Por favor ingresar un intervalo de tiempo correcto')
                    self.juego()
                    return 
                # la entrada proporcionada por el usuario es almacenado aquí: temp
                self.temp = int(self.hour.get())*3600 + int(self.minute.get())*60 + int(self.second.get())
            except:
                messagebox.showerror('Tiempo Incorrecto','Por Favor ingresar un tiempo correcto')
                return
            while self.temp > -1:
                # divmod(firstvalue = temp//60, secondvalue = temp%60)
                self.mins,self.secs = divmod(self.temp,60)
            
                # Conversión de la entrada ingresada en minutos o segundos a horas, minutos, segundos 
                # (input = 110 min --> 120*60 = 6600 => 1hr : 50min: 0sec)
                self.hours=0
                if self.mins > 60:
                        
                    # divmod(firstvalue = temp//60, secondvalue = temp%60)
                    self.hours, self.mins = divmod(self.mins, 60)
                
                self.hour.set(self.hours)
                self.minute.set(self.mins)
                self.second.set(self.secs)
            
                # actualizar la ventana de la GUI después de disminuir el valor del temp cada vez 
                self.master.update()
                time.sleep(1)
            
                # cuando valor de temp = 0; luego aparece un cuadro de mensaje
                # con el mensaje: "Tiempo Expirado" y consulta al usuario si desea continuar
                if (self.temp == 0):
                    respuesta= messagebox.askyesno("Tiempo Expirado", "¿Desea continuar el mismo juego?")
                    if respuesta==True:
                        # Si  responde  SI  entonces  el timer pasa a ser reloj inicializado con el tiempo que se había establecido en 
                        # el  timer.  Por  ejemplo  si  el  timer  estaba  para  1  hora  y  30  minutos,  ahora  el 
                        # reloj debe marcar que ya ha pasado 1 hora y 30 minutos y sigue contando el tiempo.
                        pass
                    else:
                        #Si responde NO el juego finaliza regresando a la opción de Jugar
                        self.juego()
                        return

                # despues de cada segundo va decreciendo uno
                self.temp -= 1
        elif self.configuraciones[1] == 1:
            s += 1
            if s >= 60:
                s = 0
                m = m + 1
                if m >= 60:
                    m = 0
                    h = h + 1
                    if h >= 24:
                        h = 0
        
            #etiqueta que muestra el cronometro en pantalla
            self.time['text'] = str(h)+"  :   "+str(m)+"   :    "+str(s)
        
            # iniciamos la cuenta progresiva de los segundos
            proceso=self.time.after(1000, self.inicioJuego)
            running = True      #varible de tipo indicadora  
    #----Almacena número----#      
    def botones(self,num):          
        self.numero = str(num)      
    #----Posciona número----#
    def cuadricula(self,posicion):                  
        self.posicion = posicion                    
        self.posicion.configure(text=self.numero) 
    #----Terminar juego----#
    def terminarJuego(self):
        #       Si responde SI termina de inmediato el juego y se vuelve a mostrar otro juego como si estuviera entrando a la opción de Jugar.  
        #       Si responde NO sigue jugando con el mismo juego.
        respuesta = messagebox.askyesno('TERMINAR JUEGO','¿ESTÁ SEGURO DE TERMINAR EL JUEGO?')
        if respuesta == True:
            self.juego()
            return
        else:
            pass
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
proceso=0  
h=0         
m=0
s=0
running = False
def main():
    app = tk.Tk()
    ventanaPrincipal = sudoku(app)
    app.mainloop()

if __name__ == "__main__":
    main()
