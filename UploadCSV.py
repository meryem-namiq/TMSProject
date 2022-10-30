from tkinter import *
from tkinter.filedialog import askopenfile 
from PIL import Image, ImageTk
from Box import Box



class UploadCSV():
    path_file = ""
    def __init__(self, window):
        self.window = window
        self.window.config(background='white')
        self.window.title("Transport Management System")
        self.window.geometry("720x480")
        self.window.minsize(480, 360)
        self.label = Label(window, text="Vous devez choisir un fichier CSV sous la forme suivante :",background='white', font=("Courrier", 16))
        self.label.pack(pady=50)
        #image
        self.frame0 = Frame(window,bg='white')
        image = Image.open("images/CSVfile.png")
        self.photo = ImageTk.PhotoImage(image)
        self.w1 = Label(self.frame0, image=self.photo, width=500, height=200,bg='white').pack(side="left",  expand=YES)
        self.frame0.pack()
        
        self.greet_button = Button(window, text="Choisir le fichier", command=self.open_file , background='#000000',
                        foreground='white', width=25,height=2)
        self.greet_button.pack(pady=15)

        
        self.frame = Frame(window)
        self.frame.pack(pady=15)


    def open_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
        if file_path is not None:
            titlee = Label(self.frame, text='Fichier téléchargé avec succès !', foreground='green',font=("Courrier", 13))
            titlee.pack()
            path_file = file_path.name
            setattr(UploadCSV, 'path_file',path_file)
            self.window.withdraw()
            toplevel = Toplevel(self.window)
            toplevel.geometry("720x480")
            app = Box(toplevel)


 


