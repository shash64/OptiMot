import requests
from time import sleep
from Joueur import Joueur

adresseServeur = None
URL = ""
pseudo = ""
premierePartie = False


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


def rejoindrePartie():
    global pseudo
    pseudo = input("Entrez votre pseudo: ")
    response = requests.post(f"{URL}/inscriptionLocale", json={"pseudo": pseudo})
    data = response.json()
    print(data["message"]) 
    return data["debutPartie"]


def tirer():
    lettre = input("Entrez une lettre (c/v) : ")
    response = requests.post(f"{URL}/tirerLocal", json={"lettre": lettre})
    data = response.json()
    print(data["message"])
    print(data["lettres"])
    return data.get("nbrLettreRestant") 


def proposer():
    print("Vous avez 30 secondes pour répondre... \n")
    mot = input("Veuilez proposer un mot en fonction des lettres: ")
    response = requests.post(f"{URL}/proposerLocal", json={"motPropose": mot})
    data = response.json()
    print(data["message"])


def calculerscore():
    response = requests.post(f"{URL}/terminerLocal")
    data = response.json()
    print(data["message"])
    for proposition in data["propositions"]:
        print(f"{proposition['joueur']} avec {proposition['points']} points a proposé le mot: {proposition['proposition']}")
    sleep(8)
    menu()


def afficher():
    response = requests.post(f"{URL}/affichageTerminerLocal")
    data = response.json()
    print(data["message"])
    for proposition in data["propositions"]:
        print(f"{proposition['joueur']} avec {proposition['points']} points a proposé le mot: {proposition['proposition']}")
    sleep(8)
    menu()


def jouer():
    global nbProposition, nbJoueurs, prem, premierePartie
    debutPartie = rejoindrePartie()
    prem=False
    premierePartie = True

    while not debutPartie:
        print("En attente d'un autre joueur...")
        sleep(2)
        debutPartie = etatPartie()
    nbrLettreRestant = 9
    while nbrLettreRestant > 0:
        nbrLettreRestant = tirer()

    proposer()
    etatProposition() 

    while nbProposition < nbJoueurs:
        prem = True
        print(f"Nombre de propositions : {nbProposition}/{nbJoueurs}")
        print("En attente de la proposition des autres joueurs...")
        sleep(2)
        etatProposition()  

    if prem:
        afficher()
    else:
        calculerscore()


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
        prem = True
        print(f"Nombre de propositions: {nbProposition}/{nbJoueurs}")
        print("En attente de la proposition des autres joueurs...")
        sleep(2)
        etatProposition()  

    if prem:
        afficher()
    else:
        calculerscore()

    
def menu():
   while True:
        print("\n==== Bienvenue dans le menu du jeu ====")
        print("(1) Jouer au jeu ")
        print("(2) Relancer la partie ")
        print("(3) Statistiques de la partie ")
        print("(4) Quitter le jeu \n")

        choix = input("Veuillez choisir une option: ")

        if choix == "1":
            jouer()
        elif choix == "2" and premierePartie == True:
            rejouer()
        elif choix == "3" and premierePartie == True:
            afficher()
        elif choix == "4":
            break
        else:
            print("\nOption invalide, veuillez réessayer")
   
    
def main():
    global adresseServeur, URL
    while True:
        adresseServeur = input("Veuillez entrer l'adresse IP du serveur: ")
        URL = f"http://{adresseServeur}:8888/"

        response = requests.get(f"{URL}") 
        if response.status_code == 200:
            print("Connexion au serveur réussie")
            menu()
            break
        else:
            print(f"Impossible de se connecter au serveur")

main()