from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from Jeu import Jeu
from Joueur import Joueur


app = Flask(__name__)
app.secret_key = 'projetGroupe2'


@app.route('/')
def index():
    global Partie
    Partie = Jeu(9,2)
    return render_template('index.html')

@app.route('/inscription', methods=['POST'])
def inscription():
    global Partie, joueurConnecté

    session['user_id'] = "Admin"
    if len(Partie.tabJoueurs)==Partie.nbJoueurs:
        return render_template('index.html',joueurConnecté=" - ".join(joueurConnecté),message="Partie pleine")

    nom = request.form["nomJoueur"]

    if nom in session['user_id']:
        return render_template('index.html',joueurConnecté=" - ".join(joueurConnecté),message="Déjà connecté")

    joueurConnecté = []
    Partie.ajoutJoueur(nom)
    session['user_id'] = nom
    for jou in Partie.tabJoueurs:
        joueurConnecté.append(jou.nom)
    return render_template('index.html',joueurConnecté=" - ".join(joueurConnecté))


@app.route('/demarrer', methods=['POST'])
def demarrer():
    global Partie

    return render_template('jeu.html',joueur=session['user_id'],nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres))


@app.route('/tirer', methods=['POST'])
def tirer():
    global Partie,nbLettreATirer

    if len(Partie.tabMots)==Partie.nbLettres:
        affichageLettres = "".join(Partie.tabMots)
        return render_template('jeu.html',joueur=session['user_id'],affichageLettres=affichageLettres,nbLettre="Tirage impossible : toutes les lettres ont déjà été tirées")

    typeLettre = request.form['lettre']
    if Partie.tirer(typeLettre)==False:
        affichageLettres = "".join(Partie.tabMots)
        return render_template('jeu.html',joueur=session['user_id'],affichageLettres=affichageLettres,nbLettre="Veuillez choisir une lettre valide")
    affichageLettres = "".join(Partie.tabMots)
    nbLettreATirer = Partie.nbLettres-len(Partie.tabMots)

    if nbLettreATirer==0        :
        return render_template('jeu.html',joueur=Partie.tabJoueurs[0].nom,affichageLettres=affichageLettres,nbLettre="Faites un mot avec les lettres ci-dessous !")

    return render_template('jeu.html',joueur=Partie.tabJoueurs[0].nom,affichageLettres=affichageLettres,nbLettre="Plus que "+str(nbLettreATirer)+" lettre(s) à tirer",lettres=list(affichageLettres))
        


@app.route('/proposer', methods=['POST'])
def proposer():
    global Partie, nom

    lettres_proposees = request.form.getlist('tabLettres')
    mot_propose = "".join(lettres_proposees)


    est_valide = Partie.proposition(nom, mot_propose)
    message = f"Mot proposé : {mot_propose} - {'Valide' if est_valide else 'Invalide'}"

    return render_template('jeu.html', joueur=nom, message=message, lettres=list(Partie.tabMots), nbLettre="Plus que 0 lettre(s) à tirer")



if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8888, debug=True)
