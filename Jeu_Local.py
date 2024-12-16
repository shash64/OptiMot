import requests
from time import sleep
from Joueur import Joueur

URL = "http://192.168.1.30:8888/"

pseudo = ""


def rejoindrePartie():
    global pseudo
    pseudo = input("Entrez votre pseudo: ")
    response = requests.post(f"{URL}/inscriptionLocale", json={"pseudo": pseudo})
    data = response.json()
    print(data["message"]) 
    return data["debutPartie"]

def etatPartie():
    response = requests.post(f"{URL}/inscriptionLocale", json={"pseudo": pseudo})
    data = response.json()
    return data["debutPartie"]

def etatProposition():
    global nbProposition, nbJoueurs
    response = requests.post(f"{URL}/etatProposition")
    data = response.json()
    nbProposition = data.get("nbProposition", 0)
    nbJoueurs = data.get("nbJoueurs", 2)  


def tirer():
    lettre = input("Entrez une lettre (c/v) : ")
    response = requests.post(f"{URL}/tirerLocal", json={"lettre": lettre})
    data = response.json()
    print(data["message"])
    print(data["lettres"])
    return data.get("nbrLettreRestant") 

def proposer():
    mot = input("Veuilez proposer un mot en fonction des lettres: ")
    response = requests.post(f"{URL}/proposerLocal", json={"motPropose": mot})
    data = response.json()
    print(data["message"])


def afficher():
    response = requests.post(f"{URL}/affichageterminerLocal")
    data = response.json()
    print(data["message"])
    for proposition in data["propositions"]:
        print(f"{proposition['joueur']} avec {proposition['points']} points a proposé le mot: {proposition['proposition']}")
    sleep(8)
    main()


def jouer():
    global nbProposition, nbJoueurs
    debutPartie = rejoindrePartie()

    while not debutPartie:
        print("En attente d'un autre joueur...")
        sleep(2)
        debutPartie = etatPartie()
    etatProposition()
    nbrLettreRestant = 9
    while nbrLettreRestant > 0:
        nbrLettreRestant = tirer()

    proposer()

    while nbProposition < nbJoueurs:
        print(f"Nombre de propositions : {nbProposition}/{nbJoueurs}")
        print("En attente de la proposition des autres joueurs...")
        sleep(2)
        etatProposition()  

    afficher()

def rejouer():
    response = requests.post(f"{URL}/relancerLocal")
    data = response.json()
    print(data["message"])
    etatProposition()
    nbrLettreRestant = 9
    while nbrLettreRestant > 0:
        nbrLettreRestant = tirer()

    proposer()

    while nbProposition < nbJoueurs:
        print(f"Nombre de propositions : {nbProposition}/{nbJoueurs}")
        print("En attente de la proposition des autres joueurs...")
        sleep(2)
        etatProposition()  

    afficher()

    

def main():
    while True:
        print("\n==== Bienvenue dans le menu du jeu ====")
        print("(1) Jouer au jeu ")
        print("(2) Relancer la partie ")
        print("(3) Quitter le jeu \n")

        choix = input("Veuillez choisir une option: ")

        if choix == "1":
            jouer()

        elif choix == "2":
            rejouer()

        elif choix == "3":
            break

        else:
            print("=== Option invalide, veuillez réessayer ===")
    
    
 
main()