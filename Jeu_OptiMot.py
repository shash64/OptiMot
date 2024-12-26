from Plateau import Plateau
from Joueur import Joueur
from random import shuffle

class Jeu_O:
    def __init__(self):
        self.pioche = ["A"] * 5 + ["E"] * 9 + ["I"] * 5 + ["O"] * 3 + ["U"] * 3 + ["Y"] + ["B"] * 1 + ["C"] * 2 + ["D"] * 2 + ["F"] * 2 + ["G"] * 1 + ["H"] * 1 + ["J"] + ["K"] + ["L"] * 3 + ["M"] * 3 + ["N"] * 3 + ["P"] * 2 + ["Q"] + ["R"] * 3 + ["S"] * 4 + ["T"] * 3 + ["V"] * 2 + ["W"] + ["X"] + ["Z"] #tableau des lettres en majuscules avec leurs occurences
        self.tabJoueurs=[] 
        self.plateau = Plateau()
        self.nbJoueursMax=6
        self.tour_actuel = 0  # Indice du joueur dont c'est le tour

    def joueur_actuel(self):
        #Retourne l'objet joueur dont c'est le tour
        return self.tabJoueurs[self.tour_actuel]

    def passer_au_joueur_suivant(self):
        #Passe au joueur suivant
        self.tour_actuel = (self.tour_actuel + 1) % len(self.tabJoueurs)


    def distribuer_cartes_joueurs(self, tabJoueurs):
        shuffle(self.pioche)
        for joueur in tabJoueurs:#on itere sur la liste des jouers.
            joueur.main.append([self.pioche.pop(0) for _ in range(10)])#on distribue 10 cartes à chaque joueur.
            joueur.main=joueur.main[0]

    def distribuer_cartes_plateau(self):
        for i in range(5): # Initialisation des 5 premières colonnes du plateau
            self.plateau.ajouter_lettre(i, self.pioche.pop())# À chaque itération de la boucle, cette ligne retire une carte de la pioche (avec self.pioche.pop()) et l'ajoute au plateau à la position spécifiée par i

    def ajoutJoueur(self,nom):  
        self.tabJoueurs.append(Joueur(nom))


    def afficher_etat(self):
        return {
        "plateau": self.plateau.afficher(),
        "joueurs": [{ "nom": joueur.nom, "main": joueur.afficher_main() } for joueur in self.joueurs]
    }

    def action_placer_mot(self, joueur, motG,motD, colonne_index):
        self.plateau.idMillieu[colonne_index] += len(motG)
        return motG+self.plateau.colonne[colonne_index]+motD


    def verification_plateau(self,colonne_index):
        if colonne_index == len(self.plateau.colonnes):
            return True 
        elif len(self.plateau.colonnes[colonne_index])==1:
            return self.verification_plateau(colonne_index+1) 
        elif len(self.plateau.colonnes[colonne_index])>1:
            motPropose = "".join(self.plateau.colonnes[colonne_index]) #Transformation de la chaine de caractere en tableau de caractère
            tabMotPropose = list(motPropose)
            
            #Ouverture du fichier dictionnaire et stockage des mots
            with open("ODS9.txt", 'r', encoding='utf-8') as file:
                words = file.readlines()
            words = [line.strip() for line in words] # Nettoyer les mots pour enlever les sauts de ligne
            low, high = 0, len(words) - 1
            #Algo dichotomique classique pour verifier avec la meilleure complexitée si le mot appartient au dictionnaire ou non
            while low <= high:
                mid = (low + high) // 2
                if words[mid] == motPropose:
                    #Si le mot est dans le dictionnaire, on l'ajoute dans l'attribut du joueur et l'aanonce aux autres joueurs
                    return self.verification_plateau(colonne_index+1) 
                elif words[mid] < motPropose: 
                    low = mid + 1
                else:
                    high = mid - 1
            #Si on sort de la boucle, le mot n'est pas dans le dictionnaire
            print("mot pas dans le dictionnaire")
            return False

    #version sans la classe Carte juste avec un tableau de lettres:
    def action_recouvrir(self, joueur, lettre, colonne_index, lettre_index):
        """Recouvre une lettre existante par une nouvelle lettre"""
        if lettre==self.plateau.colonnes[colonne_index][lettre_index]:
            print("Lettres identiques")
            return 0

        if len(joueur.main) == 0:
            print(f"{joueur.nom} n'a plus de cartes.")
            return 0
    
        # Vérifier si la lettre est dans la main du joueur
        if lettre not in joueur.main:
            print(f"{joueur.nom} n'a pas la lettre {lettre} dans sa main.")
            return 0
    
        # Retirer la lettre de la main du joueur
        joueur.retirer_carte(lettre)
    
        # Ajouter la nouvelle lettre à la colonne du plateau
        self.plateau.colonnes[colonne_index][lettre_index]=lettre
        return 1

    def ajout_plateau_milieu(self, lettre):
        #ajouter une lettre au milieu rang du plateau
        self.plateau.colonnes.append([lettre])

    def repartir_pioche(self, colonne_index):
        #colonnes du plateau repart à la pioche suite à une recouverte de lettre
        lettres=self.plateau.colonnes.pop(colonne_index)
        for lettre in lettres:
            self.pioche.append(lettre)

    def jeter_carte(self, joueur, lettre):
        #jeter une ou plusieurs cartes
        joueur.main.remove(lettre)

    def piocher(self, joueur):
        #piocher le nombre de cartes jeté +1
        joueur.main.append(self.pioche.pop())

    


    
'''
j1= Jeu_O()
j1.ajoutJoueur("wesh")
j1.distribuer_cartes(j1.tabJoueurs)
print(j1.tabJoueurs[0].main)

j1.plateau.colonnes = [["B"],["A","P"],["B","I","E","N"],["B","O","N"],["G"]]
print(j1.verification_plateau(2))
j1.action_recouvrir(j1.tabJoueurs[0],"B",3,0)
j1.ajout_plateau_milieu("C")

print(j1.plateau.colonnes)
j1.repartir_pioche(2)
print(j1.plateau.colonnes)
print(j1.tabJoueurs[0].main)
'''