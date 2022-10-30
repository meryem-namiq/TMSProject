from tkinter import *
from tkinter.filedialog import askopenfile 
from PIL import  ImageTk, Image
from function import *
from tkinter import messagebox
from UploadCSV import *
import time

class Box:
    def __init__(self, window):
        self.window = window
        self.window.config(background='white')
        self.window.title("Transport Management System")
        self.window.geometry("720x480")
        self.window.minsize(480, 360)
        self.label = Label(window, text="Vous devez choisir un algorithme",bg='white', font=("Courrier", 12))
        self.label.pack(pady=20)

        labelframe_tk = LabelFrame(window, text="Méthodes Rapides")
        labelframe_tk.pack(fill="both", expand="yes")
        
        btn1 = Button(labelframe_tk, text = 'clarke and wright', command=self.clarkeandWright ,border=1, font=("Courrier", 8), bg='#000000',fg='white', width=15,height=2)
        btn1.place(x = 100, y = 20)
        btn2 = Button(labelframe_tk, text = 'VNS' , border=1, command=self.methodVNS , font=("Courrier", 8), bg='#000000',fg='white', width=15,height=2)
        btn2.place(x = 240, y = 60)
        btn3 = Button(labelframe_tk, text = 'NN', border=1, command=self.methodNN ,font=("Courrier", 8), bg='#000000',fg='white', width=15,height=2)
        btn3.place(x = 380, y = 100)
        
        labelframe2_tk = LabelFrame(window, text="Méthodes Exactes")
        labelframe2_tk.pack(fill="both", expand="yes")
        
        btn4 = Button(labelframe2_tk, text = 'Branch and Bound', command=self.branchandBound ,border=1, font=("Courrier", 12), bg='#000000',fg='white', width=20,height=2)
        btn4.place(x = 240, y = 60)

    
    def clarkeandWright(self):
        from UploadCSV import UploadCSV
        tournee = clarkeAndWright(UploadCSV.path_file)
        tounee_Ville = tourneeVille(UploadCSV.path_file,tournee)
        ville=""
        for x in tounee_Ville:
            ville+= "-->" + x
        messagebox.showinfo("Tournée Clarke & Wright", ville)

    def methodVNS(self):
        from UploadCSV import UploadCSV
        aleatoire_tournee = [1, 3, 5, 4, 2]
        T_VNS = methodeVNS(UploadCSV.path_file,allPermutations(aleatoire_tournee))
        tounee_Ville_VNS = tourneeVille(UploadCSV.path_file,T_VNS)
        ville=""
        for x in tounee_Ville_VNS:
            ville+= "-->" + x
        messagebox.showinfo("Tournée Variable Neighborhood Search", ville)

    def methodNN(self):
        from UploadCSV import UploadCSV
        matrix = matriceDistance(UploadCSV.path_file)
        df = matrix[0]
        ville=""
        for x in df:
            ville+= "-->" + x
        messagebox.showinfo("Tournée Nearest Neighbor", ville)


    def branchandBound(self):
        from UploadCSV import UploadCSV
        best_solution = branchAndBound(UploadCSV.path_file)
        best_solution = [x+1 for x in best_solution]
        tounee_Ville = tourneeVille(UploadCSV.path_file,best_solution)
        ville=""
        for x in tounee_Ville:
            ville+= "-->" + x
        messagebox.showinfo("Tournée Branch & Bound", ville)
# print("Best solution:", best_solution)

    

    
