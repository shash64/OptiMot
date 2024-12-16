#import classe Joueur et bibbliotheque pour l'aléatoire.
from random import randint
from Joueur import Joueur

class Jeu: #Classe jeu pour gérer tous les élements lié a une partie
    def __init__(self,nbLettres,nbJoueurs): #Constructeur paramétré pour creer une partie en fonction du nombre de lettres et de joueurs
        self.tabVoy = ["A"] * 9 + ["E"] * 12 + ["I"] * 8 + ["O"] * 6 + ["U"] * 6 + ["Y"] #tableau de voyelles en majuscules avec leurs occurences
        self.tabCons = ["B"] * 2 + ["C"] * 2 + ["D"] * 3 + ["F"] * 2 + ["G"] * 2 + ["H"] * 2 + ["J"] + ["K"] + ["L"] * 5 + ["M"] * 3 + ["N"] * 6 + ["P"] * 2 + ["Q"] + ["R"] * 6 + ["S"] * 6 + ["T"] * 6 + ["V"] * 2 #tableau de consonnes en majuscules avec leurs occurences
        self.tabJoueurs=[]  #attribut : tableau stockant les joueurs par des objets de la classe joueur
        self.tabMots=[] #attribut : tableau stockant les lettres tirées par les joueurs
        self.nbLettres = nbLettres #attribut : le nombre de letttre pour le mot de cette partie
        self.nbJoueurs = nbJoueurs  #attribut : le nombre de joueurs participant à cette partie

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
        #On affiche quel mot était le plus long
        print("Le mot le plus long était : "+motMax)
        return motMax

        
def lancerPartie(self):
    #Execution simple d'une partie
    print("Bienvenue dans le jeu: Le Mot Le Plus Long")
    nbJ = input("Combien de Joueurs ?")
    nbL = input("Combien de Lettres ?")
    Partie = Jeu(int(nbL),int(nbJ))

    for i in range(int(nbJ)):
        nom=input("Saisissez votre nom : ")
        Partie.ajoutJoueur(nom)


    print("La partie peux commencer.")
    print("Tirer chacun votre tour une consonne ou une voyelle")

    for i in range(3):
        nbLettresActuel=0
        while(nbLettresActuel<Partie.nbLettres):#on demande aux utilisateurs de choisir des lettres
            lettre=input("Joueur(e) "+Partie.tabJoueurs[nbLettresActuel % Partie.nbJoueurs].nom+", Choisissez entre une consonne ou une voyelle (c/v)")
            if Partie.tirer(lettre):
                nbLettresActuel+=1
        
        #On affiche les lettres
        print("Voici les " + nbL + " lettres de la partie")
        Partie.afficher()

        #Demande aux utilisateurs de faire une proposition de réponse
        print("Veuillez choisir un mot le plus long parmis ces " + nbL +" lettres")
        for player in Partie.tabJoueurs:
            motPropose=input("Joueur "+player.nom+", donnez votre proposition : ").upper()
            Partie.proposition(player,motPropose)

        #On compare les propositions des Joueurs
        Partie.comparaison()

        #On affiche la réponse optimale
        Partie.motMax()

        #Affichage du classement
        print("Voici le classement des Joueurs:")
        for joueur in Partie.tabJoueurs:
            print(joueur.nom + " avec " + str(joueur.nbPoints)+" points")
            
        #print("Le mot le plus long était:" + motMax())

def reset():
    self.tabMots=[]
    for joueur in self.tabJoueurs:
        joueur.nbPoints = 0
        joueur.proposition = 0





                
            
        
    

#obj1 = Jeu(9,1)
#print(obj1.nbLettres)
#obj1.ajoutJoueur()


#print(obj1.tabJoueurs)
#print(obj1.tabJoueurs[0].nom)
#print(obj1.tabJoueurs)
#print(obj1.tabJoueurs[0].nom)

#obj1.tirer()
#obj1.afficher()
#obj1.propSolution()
#
#
#lancerPartie(Jeu)
