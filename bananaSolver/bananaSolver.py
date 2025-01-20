import random

import itertools

import time



def bananaSolver(tirage):
    taille_grille = (30,30)
    grille=[]
    for i in range(taille_grille[0]):  #pour chaque ligne
        ligne = []
        for j in range(taille_grille[1]):  #pour chaque colonne
            ligne.append('.')  #ajouter les cases vides
        grille.append(ligne)
    #Construction de la grille
    #On initialise une grille vide de taille 8x15 et on joue le jeu dessus. Pas de grille dynamique.


    def peut_placer_mot(grille, mot, l, c, direction,connexion):
        """
        Vérifie si un mot peut être placé à une position donnée et dans une direction donnée
        La vérification des lettres adjacentes (haut, bas, gauche, droite) est effectuée
        uniquement pour la dernière lettre du mot (i == len(mot) - 1)
        """  
        direction = direction.upper()
        mot = mot.upper()
        connexe = False
        if direction == 'VERTICALE':
            if l + len(mot) > len(grille):  #Hors limites
                return False
            for i in range(len(mot)):
                if grille[l+i][c]==connexion:
                    connexe = True
                #Verification des valeurs de la grille, si elle est vide y'a de la place, s'il est égal au mot[i] alors on peut utiliser cette valeur de la grille pour la connexité
                if grille[l+i][c] not in ('.', mot[i]):
                    return False
                #verification des cases adjacentes 
                if l + i < len(grille) - 1 and grille[l + i + 1][c] not in ('.') and (i==len(mot)-1 or grille[l + i + 1][c]!=mot[i+1]):  
                    #En dessous, d'abord faut verifier si on dépasse pas la grille, ensuite si la valeur à droite est vide et, si on n'est pas arriver à la fin du mot, vérifier si la lettre suivante n'appartient au mot pour qu'on y applique pas la condition
                    return False
                if l + i > 0 and grille[l + i - 1][c] not in ('.') and (i<1 or grille[l + i - 1][c]!=mot[i-1]):  
                    #Au dessus, même condition mais au lieu de vérifier si on est à la fin du mot, on vérifie si on n'est pas au début
                    return False
                if c > 0 and grille[l + i][c - 1] != '.' and mot[i] != grille[l + i][c]:  
                    #A gauche, on vérifie si on n'est pas entrain de tester un mot qui appartient un autre mot connexe horizental
                    return False
                if c < len(grille[0]) - 1 and grille[l + i][c + 1] != '.' and grille[l+i][c]!=mot[i] and ((i==len(mot)-1 or grille[l + i][c + 1]!=mot[i+1]) and grille[l + i][c + 2]=='.'): 
                    #A droite, même condition
                    return False
            if(connexe or connexion==""): 
                #il faut qu'on trouve une connexion ou connexion=="" c'est le premier mot qui initialise la grille
                return True

        elif direction == 'HORIZENTALE':
            if c + len(mot) > len(grille[0]):  #Hors limites
                return False
            for i in range(len(mot)):
                if grille[l][c + i]==connexion:
                    connexe = True
                #Verification des conflits sur le mot
                if grille[l][c + i] not in ('.', mot[i]):
                    return False
                #verification des cases adjacentes pour la dernière lettre uniquement
                  #même démarche que la direction verticale en inversant et changeant quelques positions
                if c + i < len(grille[0]) - 1 and grille[l][c + i + 1] not in ('.') and (i==len(mot)-1 or grille[l][c + i + 1]!=mot[i+1]):  
                    #A droite
                    return False
                if c + i > 0 and grille[l][c + i - 1] not in ('.') and (i<1 or grille[l][c + i - 1]!=mot[i-1]):  
                    #A gauche
                    return False
                if l > 0 and grille[l - 1][c + i] != '.' and grille[l][c + i]!=mot[i]:  
                    #Au dessus 
                    return False
                if l < len(grille) - 1 and grille[l + 1][c + i] != '.'and grille[l][c + i]!=mot[i]:  
                    #En dessous 
                    return False
            if(connexe):
                return True
        return False


    def placer_mot(grille, mot, l, c, direction):
        """
        Place un mot sur la grille à la position et direction données
        """
        direction = direction.upper()
        for i in range(len(mot)):
            if direction == 'VERTICALE':
                grille[l + i][c] = mot[i].upper()
            elif direction == 'HORIZENTALE':
                grille[l][c + i] = mot[i].upper()


    def mot_max(grille, lettres_initialisees, lettres_utilisees):
        """
        Trouve le mot le plus long possible avec les lettres disponibles
        permet l'utilisation d'une seule lettre provenant de lettres_utilisees
        """
        taille_grille = len(grille)
        taille_colonne = len(grille[0])
        mots_lettres = {}  #ici on a besoin de stocker les mots et leur lettre de connexion car on en aura besoin dans le placement dans la grille
        lettre_utilisee = ""
        with open("ODS9.txt", "r") as fd:
            dictionnaire = [mot.strip().upper() for mot in fd.readlines()]
            #dictionnaire avec tous les mots du fichier sans espaces et en maj
        for mot in dictionnaire:
            copie_lettres = list(lettres_initialisees.upper())
            besoin_lettre_utilisee = False #boolean pour ajouter une connexion avec une seule lettre des lettres utilisées
            for lettre in mot:
                if lettre in copie_lettres:
                    copie_lettres.remove(lettre)
                elif lettre in lettres_utilisees and not besoin_lettre_utilisee:
                    lettre_utilisee = lettre
                    #si on a un mot avec une lettre dans les lettres utilisées, alors on autorise l'utilisation de cette lettre une seule fois
                    besoin_lettre_utilisee = True  
                else:
                    break
            else:
                #si toutes les lettres sont valides, on ajoute le mot à notre dict
                mots_lettres[mot]=lettre_utilisee
        if mots_lettres:
            mots_possibles=[]
            for mots, lettre in mots_lettres.items():
                mots_possibles.append(mots)
            mot_le_plus_long = max(mots_possibles, key=len) #avoir le mot max dans la liste
            if(len(mots_possibles)!=1): #sinon on va pas tester le dérnier mot dans la liste
                mots_possibles.remove(mot_le_plus_long)
            mot_place=False
            if(lettres_utilisees!=""): #pour éviter de reajouter le premier mot max
                while(mots_possibles!=[] and not mot_place):                             
                    mot_le_plus_long = max(mots_possibles, key=len)
                    lettre_utilisee=mots_lettres[mot_le_plus_long]
                    mots_possibles.remove(mot_le_plus_long)
                    mot_place = False
                    for l in range(taille_grille):
                        for c in range(taille_colonne):
                            if grille[l][c] != '.':  #trouver une lettre déjà placée
                                for index, lettre in enumerate(mot_le_plus_long): #parcours du mot avec itertools pour avoir à la fois l'index et la lettre qui y correspands
                                    #vérifier connexion verticale
                                    if (peut_placer_mot(grille, mot_le_plus_long, l - index, c, 'VERTICALE',lettre_utilisee) and 0 <= l - index < taille_grille):
                                        #placement du mot à partir de la position correspendante (l-index) en vérifiant qu'on peut mettre le mot aux limites de la grille
                                        placer_mot(grille, mot_le_plus_long, l - index, c, 'VERTICALE')
                                        mot_place = True
                                        break
                                    #vérifier connexion horizontale
                                    elif (peut_placer_mot(grille, mot_le_plus_long, l, c - index, 'HORIZENTALE',lettre_utilisee) and 0 <= c - index < taille_colonne):
                                        placer_mot(grille, mot_le_plus_long, l, c - index, 'HORIZENTALE')
                                        mot_place = True
                                        break
                            if mot_place:
                                #si le mot est placé on quitte sinon il y'aura des redondances 
                                break
                        if mot_place:
                            break                   
            return grille, mot_le_plus_long, mots_lettres[mot_le_plus_long]
        return grille, None, None


    def liste_mots_connexes(grille,tirage):
        """
        Construit une liste de mots en respectant les connexions
        """
        taille_grille = len(grille)
        taille_colonne = len(grille[0])
        lettres_utilisees = ""
        liste_mots = {}
        #trouver le premier mot et le placer horizontalement au centre pour avoir plus de chance d'y ajouter des mots connexes
        grille, motMax, lettre_utilisee = mot_max(grille,tirage, lettres_utilisees)
        debut_ligne = taille_grille // 2
        debut_colonne = (taille_colonne - len(motMax)) // 2
        placer_mot(grille,motMax,debut_ligne,debut_colonne,'HORIZENTALE') 
        while motMax:
            for lettre in motMax:
                tirage =tirage.replace(lettre,"", 1)
                if(lettre==lettre_utilisee and not mot_util): 
                    #si c'est la lettre utilisée pour faire la connexion, on peut plus l'utiliser
                    mot_util=True
                elif(lettre!=lettre_utilisee): 
                    #sinon, on l'ajoute à la liste des lettres qu'on peut désormait utiliser pour établir une connexion
                    lettres_utilisees += lettre
                elif(mot_util): 
                    #pour éviter d'exclure une lettre pas utilisée pour une connexion
                    lettres_utilisees += lettre
            lettres_utilisees=lettres_utilisees.replace(lettre_utilisee,"", 1)  #on enlève la lettre qui vient d'être utilisée pour éviter qu'on ajoute des lettres dans la grille qui existe pas dans le tirage
            # mettre à jour les lettres disponibles et utilisées
            liste_mots[motMax]=lettre_utilisee
            mot_util=False
            #chercher le mot suivant avec connexion
            grille, motMax,lettre_utilisee = mot_max(grille, tirage, lettres_utilisees)      
        return liste_mots


    liste_mots = liste_mots_connexes(grille,tirage)
    # print(liste_mots)


    def afficher_grille(grille):
        """
        Affichage de la grille basique
        """
        for ligne in grille:
            print(' '.join(ligne))


    afficher_grille(grille)   







regime = (["A"] * 14 + ["B"] * 3 + ["C"] * 4 + ["D"] * 4 + ["E"] * 21 + ["F"] * 3 + ["G"] * 2 + ["H"] * 2 + ["I"] * 12 + ["J"] * 1 + ["K"] * 1 + ["L"] * 7 + ["M"] * 4 + ["N"] * 9 + ["O"] * 9 + ["P"] * 3 + ["Q"] * 1 + ["R"] * 9 + ["S"] * 9 + ["T"] * 9 + ["U"] * 9 + ["V"] * 3 + ["W"] * 1 + ["X"] * 1 + ["Y"] * 1 + ["Z"] * 2)
random.shuffle(regime)
tirage=""
for i in range(144):
    tirage=tirage+regime[i]


start_time = time.time()
bananaSolver(tirage)
print("--- %s seconds ---" % (time.time() - start_time))