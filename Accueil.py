from tkinter import *
from tkinter import messagebox
from UploadCSV import UploadCSV

class Accueil:
    def __init__(self, window):
        self.window = window
        self.window.config(background='white')
        self.window.title("Transport Management System")
        self.window.geometry("720x480")
        self.window.minsize(480, 360)
        frame01 = Frame(window, bg='white')

        frame01.pack(anchor="ne", pady=1)
        self.frame0 = Frame(window,bg='white')
        self.logo1 = PhotoImage(file="images/logo_TMS.png")
        self.w1 = Label(self.frame0, image=self.logo1, width=290, height=290,bg='white').pack(side="left", padx=15, expand=YES)
        self.frame0.pack(pady=10)
        self.title = Label(window, text=" Transport Management System ",
                      font=("Courrier", 17),bg='white', fg='#060D20')
        self.title.pack()  # expand=YES POUR CENTRER
        self. frame = Frame(window,bg='white')
        self.button = Button(self.frame, text="Valider", command=self.uploadCSV , border=1, font=("Courrier", 13), bg='#000000',
                        fg='white', width=25,height=2)
        self.button.pack()
        self.frame.pack(pady=20)


    def uploadCSV(self):
        self.window.withdraw()
        toplevel = Toplevel(self.window)
        toplevel.geometry("720x480")
        app = UploadCSV(toplevel)






