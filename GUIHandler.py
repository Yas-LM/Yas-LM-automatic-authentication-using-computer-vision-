import cv2
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class GUIHandler:
    def __init__(self, image_processor, database_handler):
        self.image_processor = image_processor
        self.database_handler = database_handler
        self.app = Tk()
        self.app.geometry("640x400+300+100")
        self.app.title("Scanner la carte d'identité")
        self.app.resizable(width=0, height=0)
        self.create_widgets()
        self.cin = ""
        self.nom = ""
        self.prenom = ""
        self.date = ""
        self.adress = ""
        self.lien = ""

    def create_widgets(self):
        # Setup initial images and labels
        img = ImageTk.PhotoImage(Image.open('.//images/centre.png').resize((314, 167), Image.ANTIALIAS))
        logo = Label(self.app, image=img)
        logo.img = img
        logo.place(x=0, y=0)

        img2 = ImageTk.PhotoImage(Image.open('.//images/logo.png').resize((319, 110), Image.ANTIALIAS))
        logo2 = Label(self.app, image=img2)
        logo2.img = img2
        logo2.place(x=316, y=0)

        # Setup canvases
        Canvas(self.app, bg="ivory", width='410', height="-56", bd="110", highlightthickness="5", highlightbackground="sky blue").place(x=0, y=170)
        Canvas(self.app, bg="ivory", width='0', height="164", bd="0", highlightthickness="4", highlightbackground="sky blue").place(x=461, y=170)

        # Setup labels and buttons
        Label(self.app, text="S'il vous plait vérifier les informations :", fg="#AA9988", font=("Courier", 12)).place(x=5, y=175)
        Label(self.app, text="Nom                   :", font=("Courier", 13)).place(x=6, y=200)
        Label(self.app, text="Prenom                :", font=("Courier", 13)).place(x=6, y=225)
        Label(self.app, text="CIN	              :", font=("Courier", 13)).place(x=6, y=250)
        Label(self.app, text="Date de Naissance     :", font=("Courier", 13)).place(x=6, y=275)
        Label(self.app, text="Adresse de Naissance  :", font=("Courier", 13)).place(x=6, y=300)
        Button(self.app, text="Valider", bg="green", font=("Courier,12"), width=20, height=2, command=self.commiter).place(x=442, y=346)
        Button(self.app, text="La personne suivant", bg="orange", font=("Courier,12"), width=20, height=2, command=self.open).place(x=224, y=346)
        Button(self.app, text="Quitter", bg="red", font=("Courier,12"), width=20, height=2, command=quit).place(x=6, y=346)
        Button(self.app, text="* Choisir l'image *", bg='yellow', width=20, height=3, command=self.open).place(x=318, y=114)

    def open(self):
        img2 = ImageTk.PhotoImage(Image.open('.//images/logo.png').resize((319, 166), Image.ANTIALIAS))
        logo2 = Label(self.app, image=img2)
        logo2.img = img2
        logo2.place(x=316, y=0)

        imagelien = filedialog.askopenfilename(initialdir="", title="Choisir l'image", filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*")))
        imagecv = cv2.imread(imagelien)
        image = self.image_processor.traitement_img(imagecv)
        gray = self.image_processor.grayscale(image)
        faces = self.image_processor.detection_image(gray)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.prenom = self.image_processor.tere_chaine(image, 5, 121, 115, 154)
        self.nom = self.image_processor.tere_chaine(image, 5, 175, 115, 208)
        self.date = self.image_processor.tere_chaine(image, 146, 200, 290, 240)
        self.cin = self.image_processor.tere_chaine(image, 470, 320, 600, 360)
        self.adress = self.image_processor.tere_chaine(image, 28, 250, 220, 290)

        img2 = ImageTk.PhotoImage(Image.open('.//images/logo.png').resize((316, 166), Image.ANTIALIAS))
        logo2 = Label(self.app, image=img2)
        logo2.img = img