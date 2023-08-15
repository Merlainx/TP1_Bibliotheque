import GestionBiblitheque.bibliotheque as gb
import os

def afficherMenu():
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

def lire_fichier(fichier):
    if not "." in fichier:
        print("Erreur! Fichier Invalide")
    elif fichier.split(".")[-1] == "csv":
        return fichier

def demander_fichier():
    fichier = input("Quel fichier de donnees voulez vous utiliser: ")
    while not os.path.exists(fichier):
        print("Le chemin du fichier n'est pas valide!")
        fichier = input("Quel fichier de donnees voulez vous utiliser: ")

    return fichier
if __name__ == "__main__":
    fichier = demander_fichier()
    biblio = lire_fichier(fichier)
    choix = ""
    while choix != "Q":
        afficherMenu()
        choix = input("Veuillez choisir une option: ")
        if choix == "1":
            gb.Bibliotheque.ajouter_adherent(biblio)





