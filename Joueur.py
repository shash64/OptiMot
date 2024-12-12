class Joueur: #Classe Joueur permettant de referencer un joueur par des attributs précis
    id_counter = 1 #Compteur pour un id incrémenté à 1 a chaque appel du constructeur
    
    def __init__(self, nom): #Constructeur paramétré par un nom
        self.id = Joueur.id_counter #id du joueur
        Joueur.id_counter += 1
        self.nom = nom #nom du joueur
        self.nbPoints = 0 #nombre de points du joueur
        self.proposition = "" #mot proposé par le joueur

    def addnbPoints(self, nbPoints): #fonction pour ajouter des points au score total du joueur
        self.nbPoints += nbPoints

