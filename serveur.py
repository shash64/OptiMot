import uuid
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from Jeu import JeuMotPlusLong, JeuOptiMot, JeuBananaSolitaire
from Joueur import Joueur


app = Flask(__name__)
app.secret_key = 'projetGroupe2'
socketio = SocketIO(app) 


"""------------------------------"""
""" Lancement des parties """
"""------------------------------"""
Partie = JeuMotPlusLong(9,2)
PartieOpti = JeuOptiMot()
PartieBananaSolitaire = JeuBananaSolitaire()


"""------------------------------"""
""" Partie utilisateur et session """
"""------------------------------"""
joueurConnecté = []
joueurConnectéOpti = []
partiesBanana = {}


"""------------------------------"""
""" Variables globales """
"""------------------------------"""
nbProposition = 0
i = 0
debutPartie = False
nbLettreATirer = 9



"""------------------------------"""
""" Route pour la page d'accueil """
"""------------------------------"""
@app.route('/')
def home():
    return render_template('home.html')



"""----------------------------------------"""
""" Routes pour le jeu du Mot Le Plus Long """
"""----------------------------------------"""
@app.route('/index')
def index():
    session['user_id'] = ""
    return render_template('index.html')


@app.route('/inscription', methods=['POST'])
def inscription():
    global debutPartie
    if len(Partie.tabJoueurs) == Partie.nbJoueurs:
        return render_template('index.html', joueurConnecté=" - ".join(joueurConnecté), message="Partie pleine")

    nom = request.form["nomJoueur"]

    if nom in joueurConnecté:
        return render_template('index.html', joueurConnecté=" - ".join(joueurConnecté), message="Déjà connecté")

    Partie.ajoutJoueur(nom)
    session['user_id'] = nom
    joueurConnecté.append(nom)

    if len(Partie.tabJoueurs) == Partie.nbJoueurs:
        socketio.emit('start_game')
        debutPartie = True
        return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False,data={'name': 'False'})

    return render_template('index.html', joueurConnecté=" - ".join(joueurConnecté))


@app.route('/demarrer')
def demarrer():
    return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False,data={'name': 'False'})


@app.route('/tirer', methods=['POST'])
def tirer():
    global nbLettreATirer, i
    tourJoueur = Partie.tabJoueurs[i].nom

    if tourJoueur != session.get('user_id'):
        return render_template('jeu.html',joueur=session['user_id'],lettres=list("".join(Partie.tabMots)),nbLettre=f"Ce n'est pas votre tour, c'est au tour de {tourJoueur}.",cacher_div=False,data={'name': 'False'})

    if len(Partie.tabMots) == Partie.nbLettres:
        affichageLettres = "".join(Partie.tabMots)
        return render_template('jeu.html',joueur=session['user_id'],lettres=list(affichageLettres),nbLettre="Tirage impossible : toutes les lettres ont déjà été tirées.",cacher_div=False,data={'name': 'False'})

    typeLettre = request.form.get('typeLettre')
    if not Partie.tirer(typeLettre):
        affichageLettres = "".join(Partie.tabMots)
        return render_template('jeu.html',joueur=session['user_id'],lettres=list(affichageLettres),nbLettre="Veuillez choisir une lettre valide.",cacher_div=False,data={'name': 'False'})
    
    affichageLettres = "".join(Partie.tabMots)
    nbLettreATirer = Partie.nbLettres - len(Partie.tabMots)
    i += 1
    i = i % Partie.nbJoueurs
    socketio.emit('update_letters', {"lettres": list(affichageLettres)})

    if nbLettreATirer == 0:
        return render_template('jeu.html',joueur=session['user_id'],lettres=list(affichageLettres),nbLettre="Faites un mot avec les lettres ci-dessous !",cacher_div=True,data={'name': 'True'})
    else:
        return render_template('jeu.html',joueur=session['user_id'],lettres=list(affichageLettres),nbLettre=f"Plus que {nbLettreATirer} lettre(s) à tirer.",cacher_div=False,data={'name': 'false'})


@app.route('/affichageLettre', methods=['GET', 'POST'])
def affichageLettre():
    global nbLettreATirer, index
    affichageLettres = "".join(Partie.tabMots)
    nbLettreATirer = Partie.nbLettres - len(Partie.tabMots)
    if nbLettreATirer == 0:
        return render_template('jeu.html',joueur=session['user_id'],lettres=list(affichageLettres),nbLettre="Faites un mot avec les lettres ci-dessous !",cacher_div=True,data={'name': 'True'})
    else:
        return render_template('jeu.html',joueur=session['user_id'],lettres=list(affichageLettres),nbLettre=f"Plus que {nbLettreATirer} lettre(s) à tirer.",cacher_div=False,data={'name': 'False'})


@app.route('/proposer', methods=['POST'])
def proposer():
    global nbProposition
    disable = True
    nbProposition +=1
    lettres_proposees = request.form.get('tabLettres')
    joueur_nom = session.get('user_id') 
    joueur_actuel = next((joueur for joueur in Partie.tabJoueurs if joueur.nom == joueur_nom), None) 
    print(joueur_actuel.proposition)
    est_valide = Partie.proposition(joueur_actuel, lettres_proposees)
    message = f"Mot proposé : {lettres_proposees} - {'Valide' if est_valide else 'Invalide'}"
    print(nbProposition)
    print(Partie.nbJoueurs)
    if nbProposition==Partie.nbJoueurs:
        return redirect('/terminer')
    return render_template('jeu.html', joueur=session['user_id'], lettres=list(Partie.tabMots), nbLettre=message,disable=disable,cacher_div=True,data={'name': 'True'})


@app.route('/terminer', methods=['GET', 'POST'])
def terminer():
    global Partie,nbProposition
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:  
        print(joueur.nbPoints)
    Partie.comparaison()
    motMax=Partie.motMax()
    socketio.emit('end_game')
    nbProposition = 2
    return render_template('resultat.html',motMax=motMax,joueurs=joueurs)

@app.route('/affichageterminer', methods=['GET', 'POST'])
def affichageterminer():
    motMax=Partie.motMax()
    joueurs=Partie.tabJoueurs
    return render_template('resultat.html',motMax=motMax,joueurs=joueurs)
    

@app.route('/quitter', methods=['POST','GET'])
def quitter():
    global joueurConnecté,nbProposition
    joueur_nom = session.get('user_id')
    nbProposition=0
    Partie.tabMots=[]
    joueurConnecté=[]
    Partie.nbLettres=9
    Partie.tabJoueurs=[]
    Partie.nbJoueurs = 2
    session.clear()
    socketio.emit('quitter')
    return render_template('home.html')


@app.route('/relancer', methods=['POST'])
def relancer(): 
    global nbProposition
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:
        joueur.proposition=""
        print(joueur.nbPoints)
    Partie.tabMots=[]
    Partie.nbLettres=9
    nbProposition=0
    if len(Partie.tabJoueurs) == Partie.nbJoueurs:
        socketio.emit('start_game')
        return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False,data={'name': 'False'})

    return render_template('index.html', joueurConnecté=" - ".join(joueurConnecté))



"""-------------------------------------------------"""
""" Routes pour le jeu du Mot Le Plus Long en Local """
"""-------------------------------------------------"""
@app.route('/inscriptionLocale', methods=['POST'])
def inscriptionLocale():
    global nom, debutPartie
    data = request.get_json()
    nom = data.get("pseudo")

    if len(Partie.tabJoueurs)==Partie.nbJoueurs:
        return jsonify({"message": f"Désolé {nom} ! La partie est pleine.", "debutPartie": debutPartie})

    if nom in joueurConnecté:
        return jsonify({"message": f"Tu es déja connecté {nom} !.", "debutPartie": debutPartie })

    Partie.ajoutJoueur(nom)
    session['user_id'] = nom
    joueurConnecté.append(nom)

    if len(Partie.tabJoueurs)==Partie.nbJoueurs:
        socketio.emit('start_game')
        debutPartie = True
    return jsonify({"message": f"{nom} à rejoint la partie.", "debutPartie": debutPartie})


@app.route('/tirerLocal', methods=['POST'])
def tirerLocal():
    global Partie, i, nbLettreATirer, nom
    data = request.get_json()
    lettre = data.get("lettre")
    tourJoueur = Partie.tabJoueurs[i].nom

    if nom != tourJoueur:
        return jsonify({"message": f"Ce n'est pas votre tour, c'est au tour de {tourJoueur}.", "lettres": "".join(Partie.tabMots), "nbrLettreRestant": nbLettreATirer})

    if len(Partie.tabMots) == Partie.nbLettres:
        affichageLettres = "".join(Partie.tabMots)
        return jsonify({"message": "Tirage impossible : toutes les lettres ont déjà été tirées.", "lettres": affichageLettres, "nbrLettreRestant": nbLettreATirer})

    if not Partie.tirer(lettre):
        affichageLettres = "".join(Partie.tabMots)
        return jsonify({"message": "Veuillez choisir une lettre valide.", "lettres": affichageLettres, "nbrLettreRestant": nbLettreATirer})

    affichageLettres = "".join(Partie.tabMots)
    nbLettreATirer = Partie.nbLettres - len(Partie.tabMots)
    i += 1 
    i = i%Partie.nbJoueurs
    socketio.emit('update_letters', {"lettres": list(affichageLettres)})

    if nbLettreATirer == 0:
        socketio.emit('chrono')
        return jsonify({"message": "Toutes les lettres ont été tirées. Faites un mot avec les lettres ci-dessous !", "lettres": affichageLettres, "nbrLettreRestant": nbLettreATirer})
    else:
        return jsonify({"message": f"Plus que {nbLettreATirer} lettre(s) à tirer.", "lettres": affichageLettres, "prochainTour": Partie.tabJoueurs[i].nom, "nbrLettreRestant": nbLettreATirer})


@app.route('/proposerLocal', methods=['POST'])
def proposerLocal():
    global nbProposition, nom
    data = request.get_json()
    mot = data.get("motPropose").upper()

    joueur_actuel = next((joueur for joueur in Partie.tabJoueurs if joueur.nom == nom), None) 
    est_valide = Partie.proposition(joueur_actuel, mot)
    nbProposition +=1
    return jsonify({"message": f"Mot proposé : {mot} - {'Valide' if est_valide else 'Invalide'}" })


@app.route('/terminerLocal', methods=['POST'])
def terminerLocal():
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:  
        print(joueur.nbPoints)
    Partie.comparaison()
    motMax = Partie.motMax()
    socketio.emit('end_game')
    propositions = [{"joueur": joueur.nom, "proposition": joueur.proposition, "points": joueur.nbPoints} for joueur in Partie.tabJoueurs]
    return jsonify({"message": f"Le mot max était : {motMax}","propositions": propositions})


@app.route('/affichageTerminerLocal', methods=['GET', 'POST'])
def affichageTerminerLocal():
    motMax=Partie.motMax()
    propositions = [{"joueur": joueur.nom, "proposition": joueur.proposition, "points": joueur.nbPoints} for joueur in Partie.tabJoueurs]
    return jsonify({"message": f"Le mot max était : {motMax}","propositions": propositions})


@app.route('/etatProposition', methods=['POST', 'GET'])
def etatProposition():
    global nbProposition, Partie
    return jsonify({"nbProposition": nbProposition, "nbJoueurs": Partie.nbJoueurs})


@app.route('/relancerLocal', methods=['POST'])
def relancerLocal(): 
    global nbProposition,nbLettreATirer
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:
        joueur.proposition=""
        print(joueur.nbPoints)
    Partie.tabMots=[]
    Partie.nbLettres=9
    nbProposition=0
    nbLettreATirer=0
    if len(Partie.tabJoueurs) == Partie.nbJoueurs:
        socketio.emit('start_game')
        return jsonify({"message": "La partie est prête a être relancée"})
    return jsonify({"message": "Erreur lors de la tentative de relance de la partie"})



"""------------------------------"""
""" Routes pour le jeu Opti Mots """
"""------------------------------"""
@app.route('/indexOpti')
def indexOpti():
    session['user_id'] = ""
    return render_template('indexOpti.html')


@app.route('/inscriptionOpti', methods=['POST'])
def inscriptionOpti():
    global debutPartieOpti
    if len(PartieOpti.tabJoueurs) == PartieOpti.nbJoueursMax:
        return render_template('indexOpti.html', joueurConnecté=" - ".join(joueurConnectéOpti), message="Partie pleine")

    nom = request.form["nomJoueur"]

    if nom in joueurConnectéOpti:
        return render_template('indexOpti.html', joueurConnecté=" - ".join(joueurConnectéOpti), message="Déjà connecté")

    PartieOpti.ajoutJoueur(nom)
    session['user_id'] = nom
    joueurConnectéOpti.append(nom)

    if len(PartieOpti.tabJoueurs) == PartieOpti.nbJoueursMax:
        socketio.emit('start_game_Opti')
        debutPartieOpti = True
        return render_template('jeuOpti.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : ",cacher_div=False)

    return render_template('indexOpti.html', joueurConnecté=" - ".join(joueurConnectéOpti))



"""------------------------------------"""
""" Route pour les modes de jeu Banana """
"""------------------------------------"""
@app.route('/indexBanana')
def indexBanana():
    return render_template('indexBanana.html')



"""------------------------------------"""
""" Route pour le jeu Banana Solitaire """
"""------------------------------------"""
@app.route('/indexBananaSolitaire')
def indexBananaSolitaire():
    return render_template('indexBananaSolitaire.html')

@app.route('/initialiserBananaSolitaire', methods=['POST'])
def initialiser():
    # Générer un identifiant unique pour chaque utilisateur s'il n'existe pas
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    user_id = session['user_id']

    # Initialiser une nouvelle partie pour cet utilisateur si elle n'existe pas déjà
    if user_id not in partiesBanana:
        partiesBanana[user_id] = JeuBananaSolitaire()
        partiesBanana[user_id].initialiser_plateau_joueur()

    partie = partiesBanana[user_id]
    return jsonify({
        'plateau': partie.plateauJeu,
        'plateau_joueur': partie.plateauJoueur,
        'regime': len(partie.regime)
    })

@app.route('/confirmerPlateau', methods=['POST'])
def confirmer_plateau():
    user_id = session.get('user_id')
    if not user_id or user_id not in partiesBanana:
        return jsonify({"message": "Partie non initialisée pour cet utilisateur.", "validite": False})

    partie = partiesBanana[user_id]
    data = request.get_json()
    partie.plateauProposition = data

    connexe = partie.verifier_connexe(data)
    if connexe:
        mots_extraits = partie.extraireMots(data)
        validite, mots_invalides = partie.comparer_avec_dictionnaire(mots_extraits)
        nouveauPlateau = partie.plateauJeu

        if validite:
            return jsonify({"message": "Tous les mots sont valides dans le dictionnaire, veuillez placer les autres lettres.", "validite": True, "plateau": nouveauPlateau})
        else:
            motsInvalidesStr = ", ".join(mots_invalides)
            return jsonify({"message": f"Le(s) mot(s) {motsInvalidesStr} ne sont/n'est pas dans le dictionnaire.", "validite": False})
    else:
        return jsonify({"message": "Les lettres ajoutées ne sont pas connexes.", "validite": False})

@app.route('/piocherCarte', methods=['POST'])
def piocherCarte():
    user_id = session.get('user_id')
    if not user_id or user_id not in partiesBanana:
        return jsonify({"message": "Partie non initialisée pour cet utilisateur."})

    partie = partiesBanana[user_id]
    lettrePioche = partie.piocher_lettres(1)
    partie.plateauJoueur += lettrePioche

    return jsonify({'lettrePioche': lettrePioche})

@app.route('/rejouerBananaSolitaire', methods=['POST'])
def rejouer():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Aucun utilisateur en session."})

    # Réinitialiser la partie pour l'utilisateur
    partiesBanana[user_id] = JeuBananaSolitaire()
    partiesBanana[user_id].initialiser_plateau_joueur()
    partie = partiesBanana[user_id]

    return jsonify({
        'plateau': partie.plateauJeu,
        'plateau_joueur': partie.plateauJoueur,
        'regime': len(partie.regime)
    })

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8888, debug=True)