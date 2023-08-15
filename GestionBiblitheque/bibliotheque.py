import csv
from datetime import datetime, timedelta
import os


class Document():
    def __init__(self, titre):
        self.titre = titre


class Volume(Document):
    def __init__(self, titre, auteur):
        super().__init__(titre)
        self.auteur = auteur



class Journal(Document):
    def __init__(self, titre, date_de_Publication):
        super().__init__(titre)
        self.date_de_Publication = date_de_Publication


class Dictionnaire(Volume):
    pass


class BandeDessinee(Volume):
    def __init__(self, titre, auteur, dessinateur):
        super().__init__(titre, auteur)
        self.dessinateur = dessinateur


class Livre(Volume):
    def __init__(self, titre, auteur):
        super().__init__(titre, auteur)
        self.livre_Disponible = True


class Emprunte():
    def __init__(self, adherent, livre):
        self.adherent = adherent
        self.livre = livre
        self.date_emprunt = datetime.today().date()
        self.date_retour = (datetime.today()+timedelta(days=15)).date()


class Bibliotheque():
    def __init__(self):
        self.documents = []
        self.adherents = []
        self.empruntes = []

    def ajouter_adherent(self, adherent):
        self.adherents.append(adherent)

    def enlever_adherent(self, adherent):
        self.adherents.remove(adherent)

    def afficher_adherents(self):
        for adherent in self.adherents:
            print(f"{adherent.nom} {adherent.prenom}")

    def ajouter_document(self, document):
        self.documents.append(document)

    def enlever_document(self, document):
        self.documents.remove(document)

    def afficher_documents(self):
        for document in self.documents:
            print(f"{document.titre} par {document.auteur}, Disponible: {document.est_disponible}")

    def afficher_emprunts(self):
        for emprunt in self.empruntes:
            print(
                f"{emprunt.adherent.nom} a emprunté {emprunt.document.titre} le {emprunt.date_emprunt}. Retourné: {'Oui' if emprunt.date_retour else 'Non'}")

    def emprunterLivre(self, adherent, livre):
        if isinstance(livre, Livre) and livre.livre_Disponible:
            livre.livre_Disponible = False
            livre_emprunter = Emprunte(adherent, livre)
            self.empruntes.append(livre_emprunter)
            adherent.livre_Emprunte.append(livre)

    def rendreLivre(self, adherent, livre):
        if livre in adherent.livre_Emprunte:
            livre.livre_Disponible = True
            adherent.livre_Emprunte.remove(livre)
            for livre_emprunter in self.empruntes:
                if livre_emprunter == livre and livre_emprunter.adherent == adherent and livre_emprunter.date_retour is None:
                    livre_emprunter.date_retour = datetime.today().date()

    def contenu_De_La_Bibliotheque(self):
        with open("Biblio.txt", "w", newline="") as fich:
            docs = csv.writer(fich)
            docs.writerow(["Titre", "Auteur", "Disponibilite", "Type du document"])
            for doc in self.documents:
                if isinstance(doc, Livre):
                    docs.writerow([doc.titre, doc.auteur, doc.livre_Disponible, "Livre"])
                elif isinstance(doc, Dictionnaire):
                    docs.writerow(["", "", "", "Dictionnaire"])
                elif isinstance(doc, BandeDessinee):
                    docs.writerow([doc.titre, doc.auteur, doc.dessinateur, "Bande dessinee"])
                elif isinstance(doc, Journal):
                    docs.writerow([doc.titre, "", "Journaux"])

    def ajout_des_Documents(self):
        with open("Biblio.txt", "r") as fich:
            affich = csv.reader(fich)
            next(affich)  # sauter la lecture de l'entete
            for ligne in affich:
                if ligne[3] == "Livre":
                    self.ajouter_document(Livre(ligne[0], ligne[1]))
                elif ligne[3] == "Bande dessinee":
                    self.ajouter_document(BandeDessinee(ligne[0], ligne[1], ligne[2]))
                elif ligne[3] == "Journaux":
                    self.ajouter_document(Journal(ligne[0], ligne[1]))

    def enregistrement_des_Adherents(self):
        with open("Adherents.txt", "w", newline="") as fich:
            adher = csv.writer(fich)
            adher.writerow(["Nom", "Prenom"])
            for adherent in self.adherents:
                adher.writerow([adherent.nom, adherent.prenom])

    def ajout_Adherent(self):
        with open("Adherents.txt", "r") as fich:
            affich = csv.reader(fich)
            next(affich)
            for ligne in affich:
                self.ajouter_adherent(Adherent(ligne[0], ligne[1]))

    def enregistrement_des_Livres_Empruntes(self): # Enregistre la liste des emprunts e
        with open("LivresEmpruntes.txt", "w", newline="") as fich:
            emprunts = csv.writer(fich)
            emprunts.writerow(["Nom de l'Adherent", "Prenom de l'Adherent", "Titre du Livre", "Date Emprunt", "Date Retour"])
            for emprunt in self.empruntes:
                emprunts.writerow([emprunt.adherent.nom, emprunt.adherent.prenom, emprunt.livre.titre, emprunt.date_emprunt, emprunt.date_retour])
# Afficher Emprunts
    def ajout_Empruntes(self):
        with open("LivresEmpruntes.txt", "r") as fich:
            affichEmprunts = csv.reader(fich)
            next(affichEmprunts) # sauter la premiere l<entete
            for ligne in affichEmprunts: # parcourir le fichier livreEmprunts 0(entete), 1 2
                adherent = next((adh for adh in self.adherents if adh.nom == ligne[0] and adh.prenom == ligne[1]), None)
                '''adherent = None
                for adh in self.adherents:
                    if adh.nom == ligne[0] and adh.prenom == ligne[1]:
                        adherent = adh
                        break'''



                livre = next((liv for liv in self.documents if liv.titre == ligne[2]), None)
                if adherent is not None and livre is not None:
                    self.emprunterLivre(adherent, livre)
                    self.empruntes[-1].date_emprunt = datetime.strptime(ligne[3], "%Y-%m-%d").date()
                    if ligne[4]:
                        self.empruntes[-1].date_retour = datetime.strptime(ligne[4], "%Y-%m-%d").date()

class Adherent():
    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom
        self.livre_Emprunte = []

    def EmpruntLivre(self, biblio, livre):
        biblio.emprunterLivre(self, livre)

    def rendreLivre(self, biblio, livre):
        biblio.rendreLivre(self, livre)

def main():
    bibliotheque = Bibliotheque()

    if os.path.exists("Biblio.txt"):
        bibliotheque.ajout_des_Documents()
    if os.path.exists("Adherents.txt"):
        bibliotheque.ajout_Adherent()
    if os.path.exists("LivresEmpruntes.txt"):
        bibliotheque.ajout_Empruntes()

    while True:
        print("******************************************")
        print("* Bienvenue à votre bibliothèque         *")
        print("* Faites un choix :                      *")
        print("******************************************")
        print("* 1 Ajouter adhérent                     *")
        print("* 2 Supprimer adhérent                   *")
        print("* 3 Afficher tous les adhérents          *")
        print("* 4 Ajouter Document                     *")
        print("* 5 Supprimer Document                   *")
        print("* 6 Afficher tous les Documents          *")
        print("* 7 Ajouter Emprunt                      *")
        print("* 8 Retour d’un Emprunt                  *")
        print("* 9 Afficher tous les Emprunts           *")
        print("* Q Quitter                              *")
        print("******************************************")

        # choix = input("Choisissez une action : ").strip().upper()
        # while choix != "Q":

        choix = input("Choisissez une action : ").strip().upper()
        if choix == "1":  # Ajouter adhérent
            nom = input("Entrez le nom de l'adherent: ")
            prenom = input("Entrez le prenom de l'adherent")
            adherent = Adherent(nom, prenom)
            bibliotheque.ajouter_adherent(adherent)
            print(f"Adherent {nom} {prenom} est ajoute avec succes.")
            bibliotheque.enregistrement_des_Adherents()

        elif choix == "2":  # Supprimer adhérent
            nom = input("Entrez le nom de l'adherent que vous voulez supprimer: ")
            prenom = input("Entrez le prenom de l'adherent que vous voulez supprimer: ")
            adherent = next((adh for adh in bibliotheque.adherents if adh.nom == nom and adh.prenom == prenom), None)
            if adherent is not None:
                bibliotheque.enlever_adherent(adherent)
                print(f"L'adherent {nom} {prenom} a ete supprime avec succes.")
            else:
                print("L'adherent que vous avez saisi ne figure pas dans la liste!")
            bibliotheque.enregistrement_des_Adherents()

        elif choix == "3":  # Afficher tous les adhérents
            for adherent in bibliotheque.adherents:
                print(f"{adherent.nom} {adherent.prenom}")

            bibliotheque.afficher_adherents()

        elif choix == "4":  # Ajouter document
            typeDocument = input("Entrez le type de document (Livre, Bandedessinee, Journal): ")
            titre = input("Entrez le titre du document: ")
            auteur = input("Entrez le nom de l'auteur: ")
            doc = None
            if typeDocument == "Livre":
                doc = Livre(titre, auteur)
            elif typeDocument == "BandeDessinee":
                dessinateur = input("Entrez le nom du dessinateur: ")
                doc = BandeDessinee(titre, auteur, dessinateur)
            elif typeDocument == "Journal":
                date_de_Publication = input("Date de publication (AAAA-MM-DD): ")
                doc = Journal(titre, date_de_Publication)
            if doc:
                bibliotheque.ajouter_document(doc)
                print(f"Le document {titre} a ete  ajoute avec succes.")
            else:
                print("Type de document incorrect!")
            bibliotheque.contenu_De_La_Bibliotheque()

        elif choix == "5":  # Supprimer Document
            titre = input("Entrez le titre du document a supprimer: ")
            doc = next((d for d in bibliotheque.documents if d.titre == titre), None)
            if doc is not None:
                bibliotheque.enlever_document(doc)
                print(f"Le documment {titre} a ete supprime avec succe!")
            else:
                print("Le document ne figure pas dans la liste!")
        elif choix == "6":  # Afficher tous les Documents
            for doc in bibliotheque.documents:
                print(doc.titre)
            bibliotheque.contenu_De_La_Bibliotheque()
            bibliotheque.ajout_des_Documents()
        elif choix == "7":  # Ajouter Emprunt
            nom = input("Entrez le nom de l'adherent qui emprunte: ")
            prenom = input("Entrez le prenom: ")
            titre = input("Entrez le titre du document a emprunter: ")
            #date_emprunt = bibliotheque.empruntes[-1].date_emprunt



            adherent = next((adh for adh in bibliotheque.adherents if adh.nom == nom and adh.prenom == prenom), None)

            document = next((liv for liv in bibliotheque.documents if isinstance(liv, Livre) and liv.titre == titre), None)

            if adherent and document:
                bibliotheque.emprunterLivre(adherent, document)
                print(f"Le livre {titre} a ete prete a {nom} {prenom}.")
                print(f"Date d'emprunt: {bibliotheque.empruntes[-1].date_emprunt}. Date de retour prévue: ")
            else:
                print("Adherent ou livre non trouve!")

            bibliotheque.enregistrement_des_Livres_Empruntes()

        elif choix == "8":  # Retour d’un Emprunt
            nom = input("Entrez le nom de l'adherent: ")
            prenom = input("Entrez le prenom de l'adherent: ")
            titre = input("Entrez le titre du livre: ")
            adherent = next((adh for adh in bibliotheque.adherents if adh.nom == nom and adh.prenom == prenom), None)
            livre = next((liv for liv in bibliotheque.documents if isinstance(liv, Livre) and liv.titre == titre), None)
            if adherent and livre:
                bibliotheque.rendreLivre(adherent, livre)
                print(f"Le livre {titre} a ete retourne par {nom} {prenom}.")
            else:
                print("Adherent ou livre non trouve!")

        elif choix == "9":  # Afficher tous les Emprunts
            for emprunt in bibliotheque.empruntes:
                print(
                    f"{emprunt.adherent.nom} - {emprunt.adherent.prenom} - {emprunt.livre.titre} - {emprunt.date_emprunt} - {emprunt.date_retour} ")
            bibliotheque.ajout_Empruntes()

        elif choix == "Q":
            print("Merci, Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez reessayez!")


if __name__ == "__main__":
    main()
