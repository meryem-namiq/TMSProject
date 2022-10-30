from tkinter import *
from Accueil import Accueil



window = Tk()
window.title("Transport Management System")
window.geometry("720x480")
window.minsize(480, 360)
window.config(background='#FCE6F9')
cls = Accueil(window)
window.mainloop()