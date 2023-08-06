from cmd import Cmd
import os
import random
import getpass
import tkinter as t
import time

class Pomodoro(Cmd):
    def do_pomo(self,args):
        def closewin():
            root.destroy()
        root=t.Tk()
        root.attributes("-fullscreen",True)
        root['bg']='#444444'
        root.title('Pomodoro Manager')
        var=t.StringVar()
        label = t.Label( root, textvariable=var, relief=t.RAISED, bd=0,fg='white',font=("Arial", 200),background='#444444')
    
        var.set(time.strftime("%H:%M:%S"))
        root.bind("<Button-1>",closewin())
        label.pack()
        root.mainloop()

        