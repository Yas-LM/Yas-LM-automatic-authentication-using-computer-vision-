import mysql.connector as MC
from tkinter import messagebox

class DatabaseHandler:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def commiter(self, cin, nom, prenom, date, adress, lien):
        try:
            conn = MC.connect(host=self.host, database=self.database, user=self.user, password=self.password)
            cursor = conn.cursor()
            req = 'INSERT INTO carte(cin, nom, prenom, date_nai, adresse, image) VALUES (%s, %s, %s, %s, %s, %s)'
            data = (cin, nom, prenom, date, adress, lien)
            cursor.execute(req, data)
            conn.commit()
            messagebox.showinfo("Information", "Les données sont enregistrées avec succès")
        except MC.Error as err:
            messagebox.showerror("Error", "Les données ne sont pas enregistrées. Veuillez vérifier la connexion avec la base de données")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()