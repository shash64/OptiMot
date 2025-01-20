#import classe Joueur et bibbliotheque pour l'aléatoire.
import random
from random import randint
from Joueur import Joueur
from random import shuffle
import requests
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
from itertools import combinations
import operator

class JeuMotPlusLong: #Classe jeu pour gérer tous les élements lié a une partie
    def __init__(self,nbLettres,nbJoueurs): #Constructeur paramétré pour creer une partie en fonction du nombre de lettres et de joueurs
        self.tabVoy = ["A"] * 9 + ["E"] * 12 + ["I"] * 8 + ["O"] * 6 + ["U"] * 6 + ["Y"] #tableau de voyelles en majuscules avec leurs occurences
        self.tabCons = ["B"] * 2 + ["C"] * 2 + ["D"] * 3 + ["F"] * 2 + ["G"] * 2 + ["H"] * 2 + ["J"] + ["K"] + ["L"] * 5 + ["M"] * 3 + ["N"] * 6 + ["P"] * 2 + ["Q"] + ["R"] * 6 + ["S"] * 6 + ["T"] * 6 + ["V"] * 2 #tableau de consonnes en majuscules avec leurs occurences
        self.tabJoueurs=[]  #attribut : tableau stockant les joueurs par des objets de la classe joueur
        self.tabMots=[] #attribut : tableau stockant les lettres tirées par les joueurs
        self.nbLettres = nbLettres #attribut : le nombre de letttre pour le mot de cette partie
        self.nbJoueurs = nbJoueurs  #attribut : le nombre de joueurs participant à cette partie
        self.infoMotLePlusLong=[] #attribut : stocker le mot le plus long, son nombre de lettre, sa nature, sa definition
        self.nbProp=0
        self.nbLettresATirer = 9
        self.nbManches = 0

    #Fonction qui crée et ajoute un objet Joueur à tabJoueurs en fonction d'un nom
    def ajoutJoueur(self,nom):  
        self.tabJoueurs.append(Joueur(nom))
          
    
    #Fonction booléene qui prend en parametre c ou v afin de tirer une consonne ou une voyelle
    def tirer(self,lettre):
        if(lettre=="c" or lettre=="C"): #Si la lettre est C
            nbAleatoire=randint(0,len(self.tabCons)-1)
            self.tabMots.append(self.tabCons[nbAleatoire])#on ajoute dans tabMots une consonne tirée aléatoirement
            return True
        elif(lettre=="v" or lettre=="V"): #Si la lettre est V
            nbAleatoire=randint(0,len(self.tabVoy)-1)
            self.tabMots.append(self.tabVoy[nbAleatoire])#on ajoute dans tabMots une voyelle tirée aléatoirement
            return True
        else:
            #Renvoie Faux et un message si la lettre n'est pas acceptée
            print("Veuillez choisir un type de lettre correcte") 
            return False

    def afficher(self): #Procédure qui tranforme le tableau des caractères en chaine de caractère pour l'afficher aux joueurs
        mot = "" 
        for lettre in self.tabMots:
            mot+=lettre
        print(mot)
    
    #Fonction prenant en parametre un joueur et un mot proposé, et verifie sa proposition avant de l'ajouter a son attribut
    def proposition(self,player,motProposefirst):
        motPropose = "".join(motProposefirst.split(",")) #Transformation de la chaine de caractere en tableau de caractère
        tabMotPropose = list(motPropose)
        copieTabMot = self.tabMots[:] #Creation d'une copie des lettre du jeu pour pouvoir les manipuler 
        print(tabMotPropose)
        print(copieTabMot)
        for lettre in tabMotPropose:    #Pour chaque lettre du mot de l'utilisateur
            print(lettre)
            if lettre in copieTabMot:   #Si elle est dans la copie des lettres
                copieTabMot.remove(lettre) #On la supprime de la copie
            else:
                #Sinon le mot n'as pas été concu avec les lettres autorisées
                print("Votre mot n'est pas conforme") 
                return False

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
                player.proposition = motPropose
                print(player.nom+" a proposé le mot : "+player.proposition)
                return True
            elif words[mid] < motPropose:
                low = mid + 1
            else:
                high = mid - 1
        #Si on sort de la boucle, le mot n'est pas dans le dictionnaire
        print("mot pas dans le dictionnaire")
        return False


    def comparaison(self):#Une fonction pour comparer les mots lequelle est plus long
        MotPlusLong=""#Une chaine vide pour stocker le mot le plus long
        NomJoueurDuMotPlusLong=[]#une chaine vide pour stocker le nom du joueur ayant le mot le plus long 
        IdJoueurDuMotPlusLong=[]#on initialise l'id a 0
        for i in range(self.nbJoueurs):#Une boucle qui va iterer sur le nombre de joueurs 
            if(len(self.tabJoueurs[i].proposition) > len(MotPlusLong)):#on compare a chaque fois la proposition du joueur selectionne avec le mot le plus long si la condition est vraie 
                IdJoueurDuMotPlusLong=[]
                IdJoueurDuMotPlusLong.append(i)
                NomJoueurDuMotPlusLong=[]
                NomJoueurDuMotPlusLong.append(self.tabJoueurs[i].nom)
                MotPlusLong=self.tabJoueurs[i].proposition#alors on stocke la proposition dans le MotPlusLong 
                #NomJoueurDuMotPlusLong=self.tabJoueurs[i].nom#on stocke aussi le nom du joueur ayant le mot le plus long 
                #IdJoueurDuMotPlusLong=self.tabJoueurs[i].id#on stocke aussi l'id de ce dernier(joueur ayant le mot le plus long)
            elif len(self.tabJoueurs[i].proposition) == len(MotPlusLong):
                IdJoueurDuMotPlusLong.append(i)
                NomJoueurDuMotPlusLong.append(self.tabJoueurs[i].nom)
        for id in IdJoueurDuMotPlusLong:
            self.tabJoueurs[id].addnbPoints(len(MotPlusLong))#Apres avoir comparé toutes les propositions de chacun des joueurs on rajoute des points au joueur ayant le mot le plus long 
            #print("Le joueur "+NomJoueurDuMotPlusLong+" à marqué "+str(len(MotPlusLong))+" points avec le mot "+MotPlusLong)#on fait l'affichage du joueur ayant le mot le plus long avec le mot tout en affichant les points qu'il a marqué
        

    #Fonction qui calcule quel mot était le plus long possible en fonction des lettres
    def motMax(self):
        motMax=""    #Initialisation du motMax 
        with open("ODS9.txt","r") as fd:
            mot="MotTestPourNePasSortirDeLaBoucleWhile"
            while(mot!=""):
                i=0
                #On lit le mot et en en fait une liste de caractères
                mot=fd.readline()
                tabMotDict = list(mot)  
                copieTabMot = self.tabMots[:]
                verif=True
                #On verifie la possibilité du mot
                while(len(tabMotDict)>1 and verif):
                    if tabMotDict[0] in copieTabMot:
                        copieTabMot.remove(tabMotDict[0])
                        tabMotDict=tabMotDict[1:]
                    else:
                        verif=False
                if verif:
                    #On regarde si notre mot testé devient le nouveau mot le plus possible
                    if len(motMax)<len(mot) and len(mot)<=9:
                            motMax=mot       
        self.infoMotLePlusLong.append(motMax[:-1]) #-1 pour enlever le \n
        motcorrige=corriger_mot_local(motMax[:-1])
        self.infoMotLePlusLong.append(str(len(motMax)-1))
        self.infoMotLePlusLong.append(obtenir_nature_grammaticale_wiki(motcorrige))
        self.infoMotLePlusLong.append(motMax[0])
        self.infoMotLePlusLong.append(obtenir_premiere_definition_wiktionary(motcorrige))
        return motMax


class JeuLeCompteEstBon:
    def __init__(self,nbJoueurs):
        self.nbATrouver = 0
        self.nbPossible = [1,2,3,4,5,6,7,8,9]*2+[25,50,75,100]
        self.nbDeLaPartie = []
        self.tabJoueurs = []
        self.nbJoueurs = nbJoueurs
        self.infoMotOpti = ()
        self.nbProp = 0
        self.nbManches = 0

    #Fonction qui crée et ajoute un objet Joueur à tabJoueurs en fonction d'un nom
    def ajoutJoueur(self,nom):  
        self.tabJoueurs.append(Joueur(nom))

    def calculer_nb_a_trouver(self):
        self.nbATrouver=random.randint(101, 999)

    def tirer_nb_partie(self):
        copieNbPossible = self.nbPossible[:]
        for i in range(6):
            indice = random.randint(0, len(copieNbPossible)-1)
            self.nbDeLaPartie.append(copieNbPossible.pop(indice))


    def proposition(self, joueur, premiere_proposition):
        resultat = evaluer_expression(premiere_proposition)
        if resultat is not None:
            joueur.proposition=int(resultat)
            return True
        else:
            joueur.proposition =0
            return False


    def le_compte_est_bon(self):
        """
        Trouve la solution optimale pour approcher un nombre cible
        en utilisant les entiers donnés et les opérations élémentaires (+, -, *, /).
        :param entiers: list, tableau d'entiers disponibles
        :param cible: int, valeur cible
        :return: tuple (int, str), le résultat le plus proche et l'expression correspondante
        """
        operations = ['+', '-', '*', '/']
        meilleure_diff = float('inf')
        meilleure_solution = None
        entiers = self.nbDeLaPartie
        cible = self.nbATrouver

        # Dictionnaire de mémoïsation pour stocker les résultats déjà calculés
        memo = {}

        def calcul_recursif(nums, expressions):
            nonlocal meilleure_diff, meilleure_solution

            # Vérifier si cette combinaison de nums a déjà été évaluée
            nums_tuple = tuple(sorted(nums))
            if nums_tuple in memo:
                return

            # Si on n'a plus qu'un seul nombre, on évalue la solution actuelle
            if len(nums) == 1:
                resultat = nums[0]
                diff = abs(cible - resultat)
                if diff < meilleure_diff:
                    meilleure_diff = diff
                    meilleure_solution = (resultat, expressions[0],diff)
                memo[nums_tuple] = True  # Mémoriser l'état pour ne pas refaire le même calcul
                return

            # Essaye toutes les paires de nombres et toutes les opérations possibles
            for i in range(len(nums)):
                for j in range(len(nums)):
                    if i != j:
                        for op in operations:
                            a, b = nums[i], nums[j]

                            # Crée une nouvelle liste de nombres sans les deux opérandes utilisés
                            reste = [nums[k] for k in range(len(nums)) if k != i and k != j]
                            reste_expr = [expressions[k] for k in range(len(expressions)) if k != i and k != j]

                            # Effectuer l'opération et continuer récursivement
                            try:
                                if op == '+':
                                    new_value = a + b
                                elif op == '-':
                                    new_value = a - b
                                elif op == '*':
                                    new_value = a * b
                                elif op == '/' and b != 0 and a % b == 0:
                                    new_value = a / b
                                else:
                                    continue  # Ignore les cas non valides

                                # Nouvelle expression
                                new_expr = f"({expressions[i]} {op} {expressions[j]})"

                                # Appel récursif
                                calcul_recursif(reste + [new_value], reste_expr + [new_expr])

                            except ZeroDivisionError:
                                continue

            # Mémoriser que cette combinaison a été explorée
            memo[nums_tuple] = True

        # Initialise les expressions avec les nombres donnés
        expressions = [str(n) for n in entiers]
        calcul_recursif(entiers, expressions)

        return meilleure_solution

    def ajout_info_optimales(self):
        self.infoMotOpti = self.le_compte_est_bon()

    def comparaison_proposition(self):
        meilleurDifférence = abs(self.nbATrouver-self.tabJoueurs[0].proposition)
        nbpoints = 7
        for joueur in self.tabJoueurs:
            if abs(joueur.proposition-self.nbATrouver)<meilleurDifférence:
                meilleurDifférence=abs(joueur.proposition-self.nbATrouver)
        if meilleurDifférence==self.infoMotOpti[2]:
            nbpoints=10
        for joueur in self.tabJoueurs:
            if abs(joueur.proposition-self.nbATrouver)==meilleurDifférence:
                joueur.nbPoints+=nbpoints


def evaluer_expression(expression):
    try:
        return eval(expression)
    except Exception as e:
        return None



class JeuOptiMot:
    def __init__(self):
        self.pioche = ["A"] * 5 + ["E"] * 9 + ["I"] * 5 + ["O"] * 3 + ["U"] * 3 + ["Y"] + ["B"] * 1 + ["C"] * 2 + ["D"] * 2 + ["F"] * 2 + ["G"] * 1 + ["H"] * 1 + ["J"] + ["K"] + ["L"] * 3 + ["M"] * 3 + ["N"] * 3 + ["P"] * 2 + ["Q"] + ["R"] * 3 + ["S"] * 4 + ["T"] * 3 + ["V"] * 2 + ["W"] + ["X"] + ["Z"] #tableau des lettres en majuscules avec leurs occurences
        self.tabJoueurs=[] 
        self.plateau = []
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



class JeuBanana:
    def __init__(self):
        self.regime = (["A"] * 14 + ["B"] * 3 + ["C"] * 4 + ["D"] * 4 + ["E"] * 21 + ["F"] * 3 + ["G"] * 2 + ["H"] * 2 + ["I"] * 12 + ["J"] * 1 + ["K"] * 1 + ["L"] * 7 + ["M"] * 4 + ["N"] * 9 + ["O"] * 9 + ["P"] * 3 + ["Q"] * 1 + ["R"] * 9 + ["S"] * 9 + ["T"] * 9 + ["U"] * 9 + ["V"] * 3 + ["W"] * 1 + ["X"] * 1 + ["Y"] * 1 + ["Z"] * 2)
        random.shuffle(self.regime)
        self.plateauSolitaire = []
        self.plateauJeu = [[]] 
        self.plateauProposition = [[]]
        self.tabJoueurs=[]
        self.gagnant = None

    def ajoutJoueur(self,nom):  
        self.tabJoueurs.append(Joueur(nom))

    def piocher_lettres(self, nombre):
        lettres = []
        for _ in range(nombre):
            if self.regime:
                lettres.append(self.regime.pop())
        return lettres


    def initialiser_plateau_solitaire(self):
        self.plateauSolitaire = self.piocher_lettres(21)

    def initialiser_plateau_cafe(self):
        for joueur in self.tabJoueurs:  
            joueur.plateauJoueur = self.piocher_lettres(21) 
    
    def initialiser_plateau_chrono(self):
        plateauTirage=self.piocher_lettres(21) 
        for joueur in self.tabJoueurs:  
            joueur.plateauJoueur = plateauTirage


    def extraireMots(self, plateau):
        mots = []
        self.plateauProposition = plateau
        for ligne in plateau:
            mot = ""
            for i in range(len(ligne)):
                if ligne[i] != "":
                    mot += ligne[i]
                else:
                    if mot: 
                        mots.append(mot)
                    mot = ""  
            if mot:  
                mots.append(mot)

        for col in range(len(plateau[0])):
            mot = ""
            for ligne in plateau:
                if ligne[col] != "":
                    mot += ligne[col]  
                else:
                    if mot:  
                        mots.append(mot)
                    mot = ""  
            if mot:  
                mots.append(mot)

        mots = [mot for mot in mots if len(mot) > 1]
        return mots
        

    def comparer_avec_dictionnaire(self, mots_extraits):
        with open("ODS9.txt", 'r', encoding='utf-8') as file:
            words = file.readlines()

        # Nettoyer les mots pour enlever les sauts de ligne et convertir en majuscules
        words = [line.strip().upper() for line in words]

        # Fonction de recherche dichotomique dans le dictionnaire
        def est_dans_dictionnaire(mot):
            low, high = 0, len(words) - 1
            while low <= high:
                mid = (low + high) // 2
                if words[mid] == mot:
                    return True
                elif words[mid] < mot:
                    low = mid + 1
                else:
                    high = mid - 1
            return False

        mots_invalides= []

        for mot in mots_extraits:
            if not est_dans_dictionnaire(mot.upper()):
                mots_invalides.append(mot)

        if mots_invalides:
            return False, mots_invalides  
        
        else:
            self.plateauJeu = self.plateauProposition
            return True, []
    
    def est_Vide(grille):
        for ligne in grille:
            for cellule in ligne:
                if cellule != "":
                    return False
        return True


    def verifier_connexe(self, plateau):
        """Vérifie si toutes les lettres posées sont connexes."""
        def explorer_connexes(x, y, visite):
            """Explore toutes les cases connexes contenant des lettres."""
            if (x, y) in visite or plateau[x][y] == "":
                return
            visite.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(plateau) and 0 <= ny < len(plateau[0]):
                    explorer_connexes(nx, ny, visite)

        # Trouver une première lettre sur le plateau
        premiere_lettre = None
        for i in range(len(plateau)):
            for j in range(len(plateau[0])):
                if plateau[i][j] != "":
                    premiere_lettre = (i, j)
                    break
            if premiere_lettre:
                break

        if not premiere_lettre:  # Si le plateau est vide
            return True

        # Explorer toutes les lettres connectées à la première lettre trouvée
        lettres_visitees = set()
        explorer_connexes(premiere_lettre[0], premiere_lettre[1], lettres_visitees)

        # Vérifier si toutes les lettres posées sont dans `lettres_visitees`
        for i in range(len(plateau)):
            for j in range(len(plateau[0])):
                if plateau[i][j] != "" and (i, j) not in lettres_visitees:
                    return False

        return True

    def echanger_tuile(self, joueur, lettre):
        # Vérifie si la lettre est dans le plateau du joueur
        if lettre not in joueur.plateauJoueur:
            print(f"Erreur : la lettre '{lettre}' n'est pas présente dans le rack de {joueur.nom}.")
            return None
        # Vérifie si le sac contient au moins 3 lettres
        if len(self.regime) < 3:
            print("Erreur : il n'y a pas assez de lettres dans le sac pour échanger.")
            return None
        joueur.plateauJoueur.remove(lettre)
        self.regime.append(lettre)
        random.shuffle(self.regime)
        nouvelles_lettres = self.piocher_lettres(3)
        # Ajoute les nouvelles lettres au rack du joueur
        joueur.plateauJoueur.extend(nouvelles_lettres)
        return nouvelles_lettres



def obtenir_premiere_definition_wiktionary(mot):
    """
    Fonction pour récupérer uniquement la première phrase de la définition d'un mot depuis Wiktionary,
    avec des espaces corrigés.
    :param mot: str, le mot à chercher
    :return: str, la première phrase de la définition ou un message d'erreur
    """
    # URL de recherche sur le site Wiktionary
    url = f"https://fr.wiktionary.org/wiki/{mot}"
    
    try:
        # Envoyer une requête HTTP
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        
        # Analyser le contenu HTML de la page
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Rechercher la section contenant les définitions (premier <ol>)
        def_section = soup.find("ol")
        
        if not def_section:
            return "Aucune définition trouvée pour le mot."
        
        # Récupérer la première définition (<li>)
        premiere_definition = def_section.find("li")
        if not premiere_definition:
            return "Aucune définition trouvée pour le mot."
        
        # Extraire le texte brut avec des espaces corrigés
        definition_complète = premiere_definition.get_text(separator=" ", strip=True)
        
        # Séparer la définition en phrases (basé sur le point final)
        premiere_phrase = definition_complète.split('.')[0] + '.'  # Récupère tout jusqu'au premier point
        
        return premiere_phrase.split(':')[0].split('du verbe')[0]
    
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion à Wiktionary : {e}"



def obtenir_nature_grammaticale_wiki(mot):
    """
    Fonction pour récupérer la nature grammaticale d'un mot depuis le site Larousse.
    :param mot: str, le mot à chercher
    :return: str, la nature grammaticale ou un message d'erreur
    """
    # URL de recherche sur le site Larousse
    url = f"https://fr.wiktionary.org/wiki/{mot}"
    
    try:
        # Envoyer une requête HTTP
        response = requests.get(url)
        response.raise_for_status()
        
        # Analyser le contenu HTML de la page
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Trouver la section contenant la nature grammaticale (élément <p> avec la classe 'CatgramDefinition')
        nature_section = soup.find("span", class_="titredef")
        
        if not nature_section:
            return "Aucune nature trouvée pour le mot."
    
        # Extraire le texte restant (nature grammaticale)
        nature = nature_section.get_text(strip=True)
        
        return nature
    
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion à Wiktionary : {e}"



def corriger_mot_local(mot_majuscule):
    """
    Corrige un mot en majuscule avec une orthographe correcte (avec accents).
    Utilise une bibliothèque locale pour la correction.
    :param mot_majuscule: str - Le mot en majuscule (ex: "EPATANT")
    :return: str - Le mot corrigé (ex: "épatant") ou None si non trouvé
    """
    spell = SpellChecker(language='fr')
    mot_minuscule = mot_majuscule.lower()
    
    # Trouver le mot corrigé
    correction = spell.correction(mot_minuscule)
    return correction

            