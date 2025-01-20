# Plateforme Multi-Jeux

## Description:

Premier Jeu : "Des chiffres et des lettres" est un jeu télévisé populaire constitué de plusieures manches du :

   Premier Jeu : "Le Mot Le Plus Long" est une implémentation web du jeu classique dans lequel les joueurs tentent de former le mot le plus long à partir d'un ensemble de lettres. Le projet est écrit en Python et utilise le framework Flask pour la gestion des interfaces web. Ce projet inclut également une version locale permettant de jouer depuis le terminal, connectée à des joueurs en ligne.

   Second Jeu : "Le compte est bon" est un jeu dans lequel les joueurs ont 6 chiffres ainsi que les opérations élémentaires telles que l'addition, la soustraction , la multiplication, et la division. Les joueurs doivent en utilisant au maximum une fois chaque nombre former grace à des opérations succecives, un nombre qui se rapproche le plus possible du nombre cible.



Deuxieme Jeu :
"Opti'Mot" est un jeu de lettres interactif qui se joue en ligne et met les joueurs au défi de former des mots à partir de lettres disposées dans une colonne verticale .Le projet est écrit aussi en Python et utilise le framework Flask pour la gestion des interfaces web.
La communication en temps réel entre le serveur et les clients est gérée par Socket.IO, permettant aux joueurs d’interagir instantanément et de partager les mises à jour du jeu sans avoir à recharger la page. L'interface utilisateur est réalisée avec des pages HTML, CSS et JavaScript, offrant une expérience visuelle agréable et réactive. Le jeu utilise également un fichier de dictionnaire (ODS9.txt) pour valider les mots proposés par les joueurs. Grâce à cette architecture, OptiMot permet une expérience de jeu fluide et engageante.

Troisième Jeu :
"BananaGrams" est également un jeu de lettres qui se joue sur plateau avec 144 tuiles. 3 modes de jeu possibles :
- Banana Solitaire : À jouer seul. Vous recevez un tirage de 21 lettres et votre but est de former des mots horizontals et verticals connexes entre eux. Possibilité de piocher une lettre si vous êtes bloqués.

- Chrono Banane : Se joue a plusieurs. Celui qui fini sa grille le premier gagne.

- Banane Café : Se joue a plusieurs avec une grille commune. Le premier joueur qui arrive à poser toutes ses lettres gagne. L'échange de une tuile contre trois est possible.

## Fonctionnalités:
- **Gestion des joueurs :** Une classe `Joueur` permet de modéliser les joueurs et leurs paramètres.
- **Mécanismes du jeu :** Toutes les fonctions liées à la logique du jeu sont regroupées dans le fichier `Jeu.py` contenant les classes JeuMotPlusLong, JeuOptiMot, JeuBanana, JeuLeCompteEstBon.
- **Version web :** Le fichier `serveur.py` gère les connexions, les routes Flask, et les templates HTML.
- **Version locale :** Le fichier `Jeu_Local.py` permet à un joueur de participer au jeu depuis le terminal tout en jouant contre des joueurs connectés via l'interface web ou d'autres terminaux.

## Structure du projet:

```
.
├── Joueur.py       # Classe pour modéliser les joueurs
├── Jeu.py          # Fonctions principales du Mot Le Plus Long
├── Jeu_OptiMot.py  # Fonctions principales du Opti'Mot
├── serveur.py      # Serveur Flask gérant l'interface web et les connexions
├── Jeu_Local.py    # Interface terminal pour jouer sur le serveur depuis le terminal
├── templates/      # Fichiers HTML pour l'interface utilisateur
└── README.md       # Documentation du projet
```

## Installations requises

## Utilisation:
```bash
pip install -r requirements.txt
```

### Version Web:
1. Lancez le serveur:
   ```bash
   python serveur.py
   ```

2. Accédez au jeu depuis votre navigateur à l'adresse du serveur:
   Exemple: [http://192.168.1.43:8888/](http://192.168.1.43:8888/)


### Version Locale:
1. Lancez le serveur:
   ```bash
   python serveur.py
   ```
2. Lancez le fichier `Jeu_Local.py` dans un autre terminal:
   ```bash
   python Jeu_Local.py
   ```

3. Entrez l'adresse IP du serveur. Exemple: `192.168.1.43`

4. Suivez les instructions dans le terminal pour jouer 

## Fonctionnement

### Fichier `Joueur.py`:
Le fichier contient la classe `Joueur`, qui modélise les propriétés et comportements des joueurs, tels que leur nom, leur nombre de points, leur propositions, ...

### Fichier `Jeu.py`:
Le fichier jeu.py regroupe l'ensemble des fonctionnalités principales nécessaires au bon déroulement des différents jeux proposés. Il inclut des classes et des méthodes clés qui assurent la gestion de chaque étape du jeu, telles que la génération aléatoire des lettres à partir d’un sac de tuiles ,le tirage des lettres pour les joueurs , la recherche du mot le plus long (motMax) dans certaines variantes , la comparaison des mots soumis par les joueurs pour valider leur authenticité et leur conformité au dictionnaire , la gestion des scores, incluant l'attribution des points en fonction des performances des joueurs et la sauvegarde des propositions des joueurs, permettant un suivi des coups joués .

Ce fichier contient également la classe JeuBanane, qui centralise la logique des trois versions du jeu de Bananagrams : Banana Solitaire , Banane Café , Chrono Banane .  
Ces trois versions ont été intégrées dans une seule classe car elles reposent sur des mécanismes similaires, comme la gestion des lettres, la validation des mots, et la vérification des plateaux. Cela permet de mutualiser le code tout en conservant la spécificité de chaque variante.

### Serveur Flask `serveur.py`:
Ce fichier permet de gérer:
- La gestion des routes (ex : affichage de la page d'acceuil, affichage du plateau, gestion des boutons de tirage de lettres et affichage du classement des joueurs).
- Les appels aux différentes fonctions du fichier Jeu.py et Jeu_OptiMot.py
- Le rendu des templates HTML pour l'interface utilisateur.

À noté : le jeu Opti'Mot est un travail en progrès, le fichier inclut l'inscription pour pouvoir se connecter au jeu avec un nombre maximum de joueurs mais on peut pas y jouer encore.

### Fichier `Jeu_Local.py`:
Ce fichier permet de jouer depuis le terminal en se connectant au serveur, le joueur a la possibilité de rejoindre la même partie que les autres joueurs web. Il permet aussi la communication avec le serveur pour synchroniser les actions de jeu.

### Fichier `Jeu_OptiMot.py`:
Ce fichier regroupe quelques fonctions principales du jeu, comme la distributions des cartes aux joueurs et dans le plateau, placement des lettres dans les colonnes du plateau pour former des mots, vérification de la validité du mot écrit, recouvrement des lettres et le pouvoir de jeter et piocher une ou plusieurs cartes.


### Fichier `bananaSolver.py`:
Ce fichier contient une fonction bananaSolver(tirage) qui prend en entrée une chaîne de lettres et génère une grille sous forme de liste de listes. Chaque case de cette grille représente soit une lettre du tirage, soit une case vide (indiquée par un '.'). Le but de cette fonction est de trouver une disposition des lettres qui respecte les règles du jeu, tout en étant la plus optimale possible. Pour tester la performance de cette solution, des mesures de temps seront effectuées sur des tirages de tailles variées. Le projet est organisé de manière indépendante et contient un fichier requirements.txt qui liste les dépendances nécessaires pour l'exécution du solver. Ce code a été conçu de manière à être facilement intégré dans un environnement de test pour valider son efficacité.	

