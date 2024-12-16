from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from Jeu import Jeu
from Joueur import Joueur


app = Flask(__name__)
app.secret_key = 'projetGroupe2'
socketio = SocketIO(app) 
Partie = Jeu(9,2)
joueurConnecté = []
socketio = SocketIO(app)
nbProposition = 0
i = 0
debutPartie = False
nbLettreATirer = 9



@app.route('/')
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
        return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False)

    return render_template('index.html', joueurConnecté=" - ".join(joueurConnecté))



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

@app.route('/demarrer')
def demarrer():
    return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False)

@app.route('/tirer', methods=['POST'])
def tirer():
    global nbLettreATirer, i
    tourJoueur = Partie.tabJoueurs[i].nom

    # Vérification : Est-ce au tour du joueur actuel ?
    if tourJoueur != session.get('user_id'):
        return jsonify({
            "success": False,
            "message": f"Ce n'est pas votre tour, c'est au tour de {tourJoueur}."
        })

    # Vérification : Toutes les lettres ont-elles été tirées ?
    if len(Partie.tabMots) == Partie.nbLettres:
        affichageLettres = "".join(Partie.tabMots)
        return jsonify({
            "success": False,
            "message": "Tirage impossible : toutes les lettres ont déjà été tirées.",
            "lettres": affichageLettres
        })

    # Récupération et validation du type de lettre
    typeLettre = request.form.get('lettre')
    if not Partie.tirer(typeLettre):
        affichageLettres = "".join(Partie.tabMots)
        return jsonify({
            "success": False,
            "message": "Veuillez choisir une lettre valide.",
            "lettres": affichageLettres
        })

    # Mise à jour des lettres affichées et calcul des lettres restantes
    affichageLettres = "".join(Partie.tabMots)
    nbLettreATirer = Partie.nbLettres - len(Partie.tabMots)

    # Mise à jour de l'index pour changer de joueur
    i += 1
    i = i % Partie.nbJoueurs

    # Emission de l'événement pour mettre à jour les lettres via SocketIO
    socketio.emit('update_letters', {"lettres": list(affichageLettres)})

    # Vérification : Toutes les lettres ont été tirées ?
    if nbLettreATirer == 0:
        return jsonify({
            "success": True,
            "message": "Faites un mot avec les lettres ci-dessous !",
            "lettres": affichageLettres
        })
    else:
        return jsonify({
            "success": True,
            "message": f"Plus que {nbLettreATirer} lettre(s) à tirer.",
            "lettres": affichageLettres
        })


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

    if nbLettreATirer == 0:
        return jsonify({"message": "Toutes les lettres ont été tirées. Faites un mot avec les lettres ci-dessous !", "lettres": affichageLettres, "nbrLettreRestant": nbLettreATirer})
    else:
        return jsonify({"message": f"Plus que {nbLettreATirer} lettre(s) à tirer.", "lettres": affichageLettres, "prochainTour": Partie.tabJoueurs[i].nom, "nbrLettreRestant": nbLettreATirer})

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
    if nbProposition==Partie.nbJoueurs:
        return redirect('/terminer')
    return render_template('jeu.html', joueur=session['user_id'], lettres=list(Partie.tabMots), nbLettre=message,disable=disable,cacher_div=True)


@app.route('/proposerLocal', methods=['POST'])
def proposerLocal():
    global nbProposition, nom
    data = request.get_json()
    mot = data.get("motPropose")

    joueur_actuel = next((joueur for joueur in Partie.tabJoueurs if joueur.nom == nom), None) 
    est_valide = Partie.proposition(joueur_actuel, mot)
    nbProposition +=1
    return jsonify({"message": f"Mot proposé : {mot} - {'Valide' if est_valide else 'Invalide'}" })

    if nbProposition==Partie.nbJoueurs:
        return redirect('/terminerLocal')



@app.route('/affichageterminer', methods=['GET', 'POST'])
def affichageterminer():
    motMax=Partie.motMax()
    joueurs=Partie.tabJoueurs
    return render_template('resultat.html',motMax=motMax,joueurs=joueurs)


@app.route('/affichageterminerLocal', methods=['POST'])
def affichageterminerLocal():
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:  
        print(joueur.nbPoints)
    Partie.comparaison()
    motMax = Partie.motMax()
    socketio.emit('end_game')
    propositions = [{"joueur": joueur.nom, "proposition": joueur.proposition, "points": joueur.nbPoints} for joueur in Partie.tabJoueurs]
    return jsonify({"message": f"Le mot max était : {motMax}","propositions": propositions})


@app.route('/etatProposition', methods=['POST', 'GET'])
def etatProposition():
    global nbProposition, Partie
    return jsonify({"nbProposition": nbProposition, "nbJoueurs": Partie.nbJoueurs})


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
    joueur.proposition=""




@app.route('/quitter', methods=['POST','GET'])
def quitter():
    global Partie, joueurConnecté
    joueur_nom = session.get('user_id')
    Partie.tabJoueurs = [joueur for joueur in Partie.tabJoueurs if joueur.nom != joueur_nom]
    if joueur_nom in joueurConnecté:
        joueurConnecté.remove(joueur_nom)
    session.clear()
    socketio.emit('quitter') 
    return render_template('index.html', joueurConnecté="")

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
        return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False)

    return render_template('index.html', joueurConnecté=" - ".join(joueurConnecté))

@app.route('/relancerLocal', methods=['POST'])
def relancerLocal(): 
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
        return jsonify({"message": "La partie est prête a être relancée"})
    return jsonify({"message": "Erreur lors de la tentative de relance de la partie"})

if __name__ == '__main__':
   socketio.run(app, host="0.0.0.0", port=8888, debug=True)