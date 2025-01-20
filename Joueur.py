class Joueur: #Classe Joueur permettant de referencer un joueur par des attributs précis
    id_counter = 1 #Compteur pour un id incrémenté à 1 a chaque appel du constructeur
    
    def __init__(self, nom): #Constructeur paramétré par un nom
        self.id = Joueur.id_counter #id du joueur
        Joueur.id_counter += 1
        self.nom = nom #nom du joueur
        self.nbPoints = 0 #nombre de points du joueur
        self.proposition = "" #mot proposé par le joueur pour mot long
        self.main = [] #main du joueur pour optiMot
        self.nombreIndice = 0
        self.plateauJoueur=[]
        self.plateauJeu=[[]]

    def addnbPoints(self, nbPoints): #fonction pour ajouter des points au score total du joueur
        self.nbPoints += nbPoints

    def afficher_main(self):
        return [str(carte) for carte in self.main]

    def ajouter_carte(self, carte):
        self.main.append(carte)

    def retirer_carte(self, lettre):
        if lettre in self.main:
            return self.main.remove(lettre)
        else:
            print(f"Le joueur {self.nom} ne possède pas la lettre {lettre}.")





