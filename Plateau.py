class Plateau:
    def __init__(self):
        self.colonnes = [[] for _ in range(5)] # 5 colonnes initiales
        self.idMillieu=[0]*5

    def afficher(self):
        return [[str(carte) for carte in colonne] for colonne in self.colonnes]

    def ajouter_lettre(self, colonne_index, carte):
        self.colonnes[colonne_index].append(carte)
