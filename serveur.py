from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from Jeu import JeuMotPlusLong, JeuOptiMot, JeuBanana, JeuLeCompteEstBon
from Joueur import Joueur


app = Flask(__name__)
app.secret_key = 'projetGroupe2'
socketio = SocketIO(app) 


"""-----------------------------"""
""" Lancement des parties """
"""-----------------------------"""
PartieOpti = JeuOptiMot()

"""----------------------------------"""
""" Parties utilisateurs et sessions """
"""----------------------------------"""
joueurEnAttenteM = []
joueurEnAttenteC = []
joueurEnAttenteCL = []
joueurEnAttenteCB = []
joueurEnAttenteCAB = []
joueurConnecté = []

partiesMotLePlusLong = {}
partiesCompteEstBon = {}
partiesChiffresEtLettres = {}
partiesBananaSolitaire = {}
partiesCafeBanane = {}

partiesChronoBanane = {}



"""------------------------------"""
""" Variables globales """
"""------------------------------"""
i = 0
debutPartie = False

"""------------------------------"""
""" Route pour la page d'accueil """
"""------------------------------"""

@app.route('/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        nom = request.form['nomJoueur']
        if nom in joueurConnecté:
            return render_template('index.html', message="Nom déjà utilisé.", joueurConnecte=joueurConnecté)
        session['user_id'] = nom
        joueurConnecté.append(nom)
        return redirect(url_for('home'))
    return render_template('index.html', joueurConnecte=joueurConnecté)

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    return render_template('home.html', joueur=session['user_id'], joueurConnecte=joueurConnecté)


@app.route('/homedcedl')
def homedcedl():
    return render_template('homedcedl.html', joueurConnecte=joueurConnecté)

"""------------------------------------------------"""
""" Routes pour le jeu des chiffres et des lettres """
"""------------------------------------------------"""

@socketio.on('join_gameDesChiffresEtDesLettres')
def join_gameDesChiffresEtDesLettres():
    joueur_nom = session.get('user_id')
    if not joueur_nom:
        return render_template('index.html')

    if len(joueurEnAttenteCL) < 2 and (joueur_nom not in joueurEnAttenteCL):
        joueurEnAttenteCL.append(joueur_nom)
        emit('update_statusDesChiffresEtDesLettres', {'statusDesChiffresEtDesLettres': f"{len(joueurEnAttenteCL)}/2 joueurs prêts"}, broadcast=True)

    if len(joueurEnAttenteCL) == 2:
        partie_id = len(partiesMotLePlusLong) + 1
        Partie = JeuMotPlusLong(9,2)
        Partie.ajoutJoueur(joueurEnAttenteCL[0])
        Partie.ajoutJoueur(joueurEnAttenteCL[1])
        tabJoueursLocal = []
        for joueur in Partie.tabJoueurs:
            tabJoueursLocal.append(joueur.nom)
            joueurEnAttenteCL.remove(joueur.nom)
        partiesMotLePlusLong[partie_id] = Partie
        Partie.nbManches = 1
        print(partiesMotLePlusLong)
        print(partiesMotLePlusLong[partie_id])
        emit('start_gameDesChiffresEtDesLettres', {'partie_id': partie_id, 'tabJoueurs': tabJoueursLocal}, broadcast=True)

@app.route('/afficherResultatDCEDL/<int:partie_id>')
def afficherResultatDCEDL(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))
    return render_template('afficherResultatDCEDL.html', numManche=((Partie.nbManches)-1)/3,joueurs=Partie.tabJoueurs, partie_id=partie_id)


"""----------------------------------------"""
""" Routes pour le jeu du Mot Le Plus Long """
"""----------------------------------------"""

@socketio.on('join_gameMotPlusLong')
def join_gameMotPlusLong():
    joueur_nom = session.get('user_id')
    if not joueur_nom:
        return render_template('index.html')

    if len(joueurEnAttenteM) < 2 and (joueur_nom not in joueurEnAttenteM):
        joueurEnAttenteM.append(joueur_nom)
        emit('update_statusMotPlusLong', {'statusMotPlusLong': f"{len(joueurEnAttenteM)}/2 joueurs prêts"}, broadcast=True)

    if len(joueurEnAttenteM) == 2:
        partie_id = len(partiesMotLePlusLong) + 1
        Partie = JeuMotPlusLong(9,2)
        Partie.ajoutJoueur(joueurEnAttenteM[0])
        Partie.ajoutJoueur(joueurEnAttenteM[1])
        tabJoueursLocal = []
        for joueur in Partie.tabJoueurs:
            tabJoueursLocal.append(joueur.nom)
            joueurEnAttenteM.remove(joueur.nom)
        partiesMotLePlusLong[partie_id] = Partie
        print(partiesMotLePlusLong)
        print(partiesMotLePlusLong[partie_id])
        emit('start_gameMotPlusLong', {'partie_id': partie_id, 'tabJoueurs': tabJoueursLocal}, broadcast=True)


@app.route('/demarrer/<int:partie_id>')
def demarrer(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))
    return render_template('jeu.html', joueur=session['user_id'], i =0, nbLettre=f"Nombre de lettres pour ce mot : {Partie.nbLettres}", cacher_div=False, data={'name': 'False'},partie_id=partie_id)


@app.route('/tirer/<int:partie_id>', methods=['POST'])
def tirer(partie_id):
    global i
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))

    tourJoueur = Partie.tabJoueurs[i].nom

    if tourJoueur != session.get('user_id'):
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list("".join(Partie.tabMots)),nbLettre=f"Ce n'est pas votre tour, c'est au tour de {tourJoueur}.",cacher_div=False,data={'name': 'False'}, partie_id=partie_id)

    if len(Partie.tabMots) == Partie.nbLettres:
        affichageLettres = "".join(Partie.tabMots)
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list(affichageLettres),nbLettre="Tirage impossible : toutes les lettres ont déjà été tirées.",cacher_div=False,data={'name': 'False'}, partie_id=partie_id)

    typeLettre = request.form.get('typeLettre')
    if not Partie.tirer(typeLettre):
        affichageLettres = "".join(Partie.tabMots)
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list(affichageLettres),nbLettre="Veuillez choisir une lettre valide.",cacher_div=False,data={'name': 'False'}, partie_id=partie_id)
    
    affichageLettres = "".join(Partie.tabMots)
    Partie.nbLettresATirer = Partie.nbLettres - len(Partie.tabMots)
    i += 1
    i = i % Partie.nbJoueurs
    tabJoueursLocal = []
    for joueur in Partie.tabJoueurs:
        tabJoueursLocal.append(joueur.nom)
    socketio.emit('update_letters', {"lettres": list(affichageLettres), 'partie_id': partie_id,'tabJoueurs': tabJoueursLocal})

    if Partie.nbLettresATirer == 0:
        motMax=Partie.motMax()
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list(affichageLettres),nbLettre="Faites un mot avec les lettres ci-dessous !",cacher_div=True,data={'name': 'True'}, partie_id=partie_id)
    else:
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list(affichageLettres),nbLettre=f"Plus que {Partie.nbLettresATirer} lettre(s) à tirer.",cacher_div=False,data={'name': 'false'}, partie_id=partie_id)


@app.route('/affichageLettre/<int:partie_id>', methods=['GET', 'POST'])
def affichageLettre(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))

    affichageLettres = "".join(Partie.tabMots)
    Partie.nbLettresATirer = Partie.nbLettres - len(Partie.tabMots)
    if Partie.nbLettresATirer == 0:
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list(affichageLettres),nbLettre="Faites un mot avec les lettres ci-dessous !",cacher_div=True,data={'name': 'True'}, partie_id=partie_id)
    else:
        return render_template('jeu.html',joueur=session['user_id'],i=0,lettres=list(affichageLettres),nbLettre=f"Plus que {Partie.nbLettresATirer} lettre(s) à tirer.",cacher_div=False,data={'name': 'False'}, partie_id=partie_id)


@app.route('/proposer/<int:partie_id>', methods=['POST'])
def proposer(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))

    disable = True
    Partie.nbProp +=1
    lettres_proposees = str(request.form.get('tabLettres'))
    joueur_nom = session.get('user_id') 
    joueur_actuel = next((joueur for joueur in Partie.tabJoueurs if joueur.nom == joueur_nom), None) 
    joueur_actuel.proposition=""
    est_valide = Partie.proposition(joueur_actuel, lettres_proposees)
    message = f"Mot proposé : {lettres_proposees} - {'Valide' if est_valide else 'Invalide'}"
    print(Partie.nbProp)
    print(Partie.nbJoueurs)
    if Partie.nbProp==Partie.nbJoueurs:
        if(Partie.nbManches>0): 
            if(Partie.nbManches%3==1):
                Partie.nbManches+=1
                Partie.comparaison()
                partie_id = len(partiesCompteEstBon) + 1
                PartieLCEB = JeuLeCompteEstBon(2)
                partiesCompteEstBon[partie_id] = PartieLCEB
                PartieLCEB.tabJoueurs = Partie.tabJoueurs
                PartieLCEB.nbManches = Partie.nbManches
                tabJoueursLocal =[]
                for joueur in PartieLCEB.tabJoueurs:
                    joueur.propostion = 0
                    tabJoueursLocal.append(joueur.nom)
                PartieLCEB.tirer_nb_partie()
                PartieLCEB.calculer_nb_a_trouver()
                socketio.emit('allerMancheLCEB',{'partie_id':partie_id, 'tabJoueurs' :tabJoueursLocal})
                return redirect('/demarrer_lceb/'+str(partie_id))
            if(Partie.nbManches%3==0):
                Partie.nbManches+=1
                tabJoueursLocal =[]
                for joueur in Partie.tabJoueurs:
                    tabJoueursLocal.append(joueur.nom)
                Partie.comparaison()
                socketio.emit('afficherResultatDCEDL',{'partie_id':partie_id, 'tabJoueurs' :tabJoueursLocal})
                return redirect('/afficherResultatDCEDL/'+str(partie_id))
        return redirect('/terminer/'+str(partie_id))
    return render_template('jeu.html', joueur=session['user_id'], lettres=list(Partie.tabMots), nbLettre=message,disable=disable,affichageIndices=Partie.infoMotLePlusLong,i=4,cacher_div=True,data={'name': 'False'}, partie_id=partie_id)

@app.route('/indice/<int:partie_id>', methods=['POST'])
def indice(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))
        
    i=0
    print(Partie.infoMotLePlusLong)
    for joueur in Partie.tabJoueurs:
        if joueur.nom == session['user_id']:
            if joueur.nombreIndice<4:
                joueur.nombreIndice+=1
                i=joueur.nombreIndice
            else :
                i=4
    return render_template('jeu.html', joueur=session['user_id'], lettres=list(Partie.tabMots), nbLettre="Faites un mot avec les lettres ci-dessous !",i=i,affichageIndices=Partie.infoMotLePlusLong,cacher_div=True,data={'name': 'True'}, partie_id=partie_id)

@app.route('/terminer/<int:partie_id>', methods=['GET', 'POST'])
def terminer(partie_id):
    global Partie
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))
        
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:  
        print(joueur.nbPoints)
    Partie.comparaison()
    tabJoueursLocal = []
    for joueur in Partie.tabJoueurs:
        tabJoueursLocal.append(joueur.nom)
    socketio.emit('end_game', {'partie_id': partie_id, 'tabJoueurs' :tabJoueursLocal})
    Partie.nbProp = 2
    return render_template('resultat.html',motMax=Partie.infoMotLePlusLong[0],joueurs=joueurs, partie_id=partie_id)

@app.route('/affichageterminer/<int:partie_id>', methods=['GET', 'POST'])
def affichageterminer(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))
        
    joueurs=Partie.tabJoueurs
    return render_template('resultat.html',motMax=Partie.infoMotLePlusLong[0],joueurs=joueurs, partie_id=partie_id)
    

@app.route('/quitter', methods=['POST','GET'])
def quitter():
    global joueurConnecté
    Partie.nbProp=0
    Partie.tabMots=[]
    Partie.nbLettres=9
    Partie.nbJoueurs = 2
    Partie.infoMotLePlusLong=[]
    tabJoueursLocal = []
    for joueur in Partie.tabJoueurs:
        tabJoueursLocal.append(joueur.nom)
    Partie.tabJoueurs=[]
    socketio.emit('quitter',{'tabJoueurs': tabJoueursLocal})
    return render_template('home.html')


@app.route('/relancer/<int:partie_id>', methods=['POST'])
def relancer(partie_id): 
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    Partie = partiesMotLePlusLong.get(partie_id)
    if not Partie:
        return redirect(url_for('home'))
        
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:
        joueur.proposition=""
        joueur.nombreIndice=0
        print(joueur.nbPoints)
    Partie.tabMots=[]
    Partie.nbLettres=9
    Partie.nbProp=0
    Partie.infoMotLePlusLong=[]
    if len(Partie.tabJoueurs) == Partie.nbJoueurs:
        tabJoueursLocal = []
        for joueur in Partie.tabJoueurs:
            tabJoueursLocal.append(joueur.nom)
        socketio.emit('start_game', {'partie_id':partie_id,'tabJoueurs': tabJoueursLocal})
        return render_template('jeu.html',joueur=session['user_id'],i=0,nbLettre="Nombre de lettres pour ce mot : "+str(Partie.nbLettres),cacher_div=False,data={'name': 'False'}, partie_id=partie_id)

    return redirect(url_for('home'))



"""--------------------------------------"""
""" Routes pour le jeu du Compte est bon """
"""--------------------------------------"""


@socketio.on('join_gameLeCompteEstBon')
def join_gameMotPlusLong():
    joueur_nom = session.get('user_id')
    if not joueur_nom:
        return render_template('index.html')

    if len(joueurEnAttenteC) < 2 and (joueur_nom not in joueurEnAttenteC):
        joueurEnAttenteC.append(joueur_nom)
        emit('update_statusLeCompteEstBon', {'statusLeCompteEstBon': f"{len(joueurEnAttenteC)}/2 joueurs prêts"}, broadcast=True)

    if len(joueurEnAttenteC) == 2:
        partie_id = len(partiesCompteEstBon) + 1
        PartieLCEB = JeuLeCompteEstBon(2)
        PartieLCEB.ajoutJoueur(joueurEnAttenteC[0])
        PartieLCEB.ajoutJoueur(joueurEnAttenteC[1])
        tabJoueursLocal = []
        for joueur in PartieLCEB.tabJoueurs:
            tabJoueursLocal.append(joueur.nom)
            joueurEnAttenteC.remove(joueur.nom)
        partiesCompteEstBon[partie_id] = PartieLCEB
        PartieLCEB.tirer_nb_partie()
        PartieLCEB.calculer_nb_a_trouver()
        print(partiesCompteEstBon)
        print(partiesCompteEstBon[partie_id])
        emit('start_gameLeCompteEstBon', {'partie_id': partie_id,'tabJoueurs': tabJoueursLocal}, broadcast=True)


@app.route('/demarrer_lceb/<int:partie_id>')
def demarrer_lceb(partie_id):
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    PartieLCEB = partiesCompteEstBon.get(partie_id)
    if not PartieLCEB:
        return redirect(url_for('home'))
    return render_template('jeulceb.html',partie_id=partie_id,joueur=session['user_id'], numbers=PartieLCEB.nbDeLaPartie, target_number=PartieLCEB.nbATrouver,message="Essayez le plus possible de vous rapprocher de ce chiffre !")


@app.route('/submit/<int:partie_id>', methods=['POST'])
def submit(partie_id):
    PartieLCEB = partiesCompteEstBon.get(partie_id)
    if not PartieLCEB:
        return redirect(url_for('home'))
    PartieLCEB.nbProp +=1
    nb_proposees = request.form.get('tabnb')
    joueur_nom = session.get('user_id')
    joueur_actuel = next((joueur for joueur in PartieLCEB.tabJoueurs if joueur.nom == joueur_nom), None)
    est_valide = PartieLCEB.proposition(joueur_actuel, nb_proposees)
    message = f"Expression proposée : {nb_proposees} = {joueur_actuel.proposition} {'Valide' if est_valide else 'car expression Invalide'}"
    if PartieLCEB.nbProp==PartieLCEB.nbJoueurs:
        if PartieLCEB.nbManches>0:
            PartieLCEB.nbManches+=1
            PartieLCEB.ajout_info_optimales()
            PartieLCEB.comparaison_proposition()
            partie_id = len(partiesMotLePlusLong) + 1
            Partie = JeuMotPlusLong(9,2)
            partiesMotLePlusLong[partie_id] = Partie
            Partie.tabJoueurs = PartieLCEB.tabJoueurs
            Partie.nbManches = PartieLCEB.nbManches
            tabJoueursLocal =[]
            for joueur in Partie.tabJoueurs:
                joueur.propostion = ""
                tabJoueursLocal.append(joueur.nom)
            socketio.emit('allerMancheMLPL',{'partie_id':partie_id, 'tabJoueurs' :tabJoueursLocal})
            print(Partie)
            return redirect('/demarrer/'+str(partie_id))
        return redirect('/terminerlceb/'+str(partie_id))
    return render_template('jeulceb.html',partie_id=partie_id,joueur=session['user_id'], numbers=PartieLCEB.nbDeLaPartie, disable=True, target_number=PartieLCEB.nbATrouver,message=message)

@app.route('/terminerlceb/<int:partie_id>', methods=['GET', 'POST'])
def terminerlceb(partie_id):
    global PartieLCEB
    PartieLCEB = partiesCompteEstBon.get(partie_id)
    if not PartieLCEB:
        return redirect(url_for('home'))
    joueurs=PartieLCEB.tabJoueurs
    PartieLCEB.ajout_info_optimales()
    PartieLCEB.comparaison_proposition()
    repOpti=PartieLCEB.infoMotOpti
    resultat = repOpti[0]
    expression = repOpti[1]
    erreur = repOpti[2]
    tabJoueursLocal = []
    for joueur in PartieLCEB.tabJoueurs:
        tabJoueursLocal.append(joueur.nom)
    socketio.emit('end_game_lceb', {'partie_id':partie_id,'tabJoueurs': tabJoueursLocal})
    return render_template('resultatlceb.html',partie_id=partie_id,resultat=resultat, expression=expression, erreur=erreur,joueurs=joueurs)


@app.route('/affichageterminerlceb/<int:partie_id>', methods=['GET', 'POST'])
def affichageterminerlceb(partie_id):
    PartieLCEB = partiesCompteEstBon.get(partie_id)
    if not PartieLCEB:
        return redirect(url_for('home'))
    joueurs=PartieLCEB.tabJoueurs
    repOpti=PartieLCEB.infoMotOpti
    resultat = repOpti[0]
    expression = repOpti[1]
    erreur = repOpti[2]
    return render_template('resultatlceb.html',partie_id=partie_id,resultat=resultat, expression=expression, erreur=erreur,joueurs=joueurs)


@app.route('/quitterlceb/<int:partie_id>', methods=['POST','GET'])
def quitterlceb(partie_id):
    PartieLCEB = partiesCompteEstBon.get(partie_id)
    if not PartieLCEB:
        return redirect(url_for('home'))
    PartieLCEB.nbProp=0
    PartieLCEB.nbATrouver = 0
    PartieLCEB.nbJoueurs = 2
    PartieLCEB.infoMotOpti=[]
    PartieLCEB.nbDeLaPartie=[]
    tabJoueursLocal = []
    for joueur in PartieLCEB.tabJoueurs:
        tabJoueursLocal.append(joueur.nom)
    PartieLCEB.tabJoueurs=[]
    socketio.emit('quitterlceb',{'tabJoueurs': tabJoueursLocal})
    return redirect(url_for('home'))


@app.route('/relancerlceb/<int:partie_id>', methods=['POST'])
def relancerlceb(partie_id):
    PartieLCEB = partiesCompteEstBon.get(partie_id)
    if not PartieLCEB:
        return redirect(url_for('home')) 
    joueurs=PartieLCEB.tabJoueurs
    tabJoueursLocal = []
    for joueur in joueurs:
        joueur.proposition=0
        tabJoueursLocal.append(joueur.nom)
        print(joueur.nbPoints)
    PartieLCEB.nbDeLaPartie=[]
    PartieLCEB.nbATrouver=9
    PartieLCEB.nbProp=0
    PartieLCEB.infoMotOpti=[]
    PartieLCEB.tirer_nb_partie()
    PartieLCEB.calculer_nb_a_trouver()
    if len(PartieLCEB.tabJoueurs) == PartieLCEB.nbJoueurs:
        socketio.emit('start_game_lceb', {'partie_id':partie_id,'tabJoueurs': tabJoueursLocal})
        return render_template('jeulceb.html',partie_id=partie_id,joueur=session['user_id'], numbers=PartieLCEB.nbDeLaPartie, target_number=PartieLCEB.nbATrouver,message="Essayez le plus possible de vous rapprocher de ce chiffre !")

    return redirect(url_for('home'))

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
    global Partie, i, nom
    data = request.get_json()
    lettre = data.get("lettre")
    tourJoueur = Partie.tabJoueurs[i].nom

    if nom != tourJoueur:
        return jsonify({"message": f"Ce n'est pas votre tour, c'est au tour de {tourJoueur}.", "lettres": "".join(Partie.tabMots), "nbrLettreRestant": Partie.nbLettresATirer})

    if len(Partie.tabMots) == Partie.nbLettres:
        affichageLettres = "".join(Partie.tabMots)
        return jsonify({"message": "Tirage impossible : toutes les lettres ont déjà été tirées.", "lettres": affichageLettres, "nbrLettreRestant": Partie.nbLettresATirer})

    if not Partie.tirer(lettre):
        affichageLettres = "".join(Partie.tabMots)
        return jsonify({"message": "Veuillez choisir une lettre valide.", "lettres": affichageLettres, "nbrLettreRestant": Partie.nbLettresATirer})

    affichageLettres = "".join(Partie.tabMots)
    Partie.nbLettresATirer = Partie.nbLettres - len(Partie.tabMots)
    i += 1 
    i = i%Partie.nbJoueurs
    socketio.emit('update_letters', {"lettres": list(affichageLettres)})

    if Partie.nbLettresATirer == 0:
        socketio.emit('chrono')
        return jsonify({"message": "Toutes les lettres ont été tirées. Faites un mot avec les lettres ci-dessous !", "lettres": affichageLettres, "nbrLettreRestant": Partie.nbLettresATirer})
    else:
        return jsonify({"message": f"Plus que {Partie.nbLettresATirer} lettre(s) à tirer.", "lettres": affichageLettres, "prochainTour": Partie.tabJoueurs[i].nom, "nbrLettreRestant": Partie.nbLettresATirer})


@app.route('/proposerLocal', methods=['POST'])
def proposerLocal():
    global nom
    data = request.get_json()
    mot = data.get("motPropose").upper()

    joueur_actuel = next((joueur for joueur in Partie.tabJoueurs if joueur.nom == nom), None) 
    est_valide = Partie.proposition(joueur_actuel, mot)
    Partie.nbProp +=1
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
    global Partie
    return jsonify({"Partie.nbProp": Partie.nbProp, "nbJoueurs": Partie.nbJoueurs})


@app.route('/relancerLocal', methods=['POST'])
def relancerLocal(): 
    joueurs=Partie.tabJoueurs
    for joueur in joueurs:
        joueur.proposition=""
        print(joueur.nbPoints)
    Partie.tabMots=[]
    Partie.nbLettres=9
    Partie.nbProp=0
    Partie.nbLettresATirer=0
    if len(Partie.tabJoueurs) == Partie.nbJoueurs:
        socketio.emit('start_game')
        return jsonify({"message": "La partie est prête a être relancée"})
    return jsonify({"message": "Erreur lors de la tentative de relance de la partie"})



"""------------------------------"""
""" Routes pour le jeu Opti Mots """
"""------------------------------"""
@app.route('/demarrerOpti')
def demarrerOpti():
    return render_template('jeuOpti.html')


"""------------------------------------"""
""" Route pour les modes de jeu Banana """
"""------------------------------------"""
@app.route('/indexBanana')
def indexBanana():
    return render_template('indexBanana.html', joueurConnecte=joueurConnecté)


"""------------------------------------"""
""" Route pour le jeu Banana Solitaire """
"""------------------------------------"""
@app.route('/indexBananaSolitaire')
def indexBananaSolitaire():
    return render_template('indexBananaSolitaire.html')

@app.route('/initialiserBananaSolitaire', methods=['POST'])
def initialiser():
    if 'user_id' not in session:
        return render_template("index.html")

    user_id = session['user_id']

    if user_id not in partiesBananaSolitaire:
        partiesBananaSolitaire[user_id] = JeuBanana()
        partiesBananaSolitaire[user_id].initialiser_plateau_solitaire()

    return jsonify({'plateau': partiesBananaSolitaire[user_id].plateauJeu, 'plateau_joueur': partiesBananaSolitaire[user_id].plateauSolitaire})

@app.route('/confirmerPlateau', methods=['POST'])
def confirmer_plateau():
    user_id = session.get('user_id')
    if not user_id or user_id not in partiesBananaSolitaire:
        return jsonify({"message": "Partie non initialisée pour cet utilisateur.", "validite": False})

    data = request.get_json()
    partiesBananaSolitaire[user_id].plateauProposition = data

    connexe = partiesBananaSolitaire[user_id].verifier_connexe(data)
    if connexe:
        mots_extraits = partiesBananaSolitaire[user_id].extraireMots(data)
        validite, mots_invalides = partiesBananaSolitaire[user_id].comparer_avec_dictionnaire(mots_extraits)
        nouveauPlateau = partiesBananaSolitaire[user_id].plateauJeu

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
    if not user_id or user_id not in partiesBananaSolitaire:
        return jsonify({"message": "Partie non initialisée pour cet utilisateur."})

    lettrePioche = partiesBananaSolitaire[user_id].piocher_lettres(1)
    partiesBananaSolitaire[user_id].plateauSolitaire += lettrePioche

    return jsonify({'lettrePioche': lettrePioche})

@app.route('/rejouerBananaSolitaire', methods=['POST'])
def rejouer():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Aucun utilisateur en session."})

    partiesBananaSolitaire[user_id] = JeuBanana()
    partiesBananaSolitaire[user_id].initialiser_plateau_solitaire()
    

    return jsonify({'plateau': partiesBananaSolitaire[user_id].plateauJeu, 'plateau_joueur': partiesBananaSolitaire[user_id].plateauSolitaire})

@app.route('/quitterBanana', methods=['POST'])
def quitterBanana():
    user_id = session.get('user_id')  
    if user_id and user_id in partiesBananaSolitaire:
        del partiesBananaSolitaire[user_id]  

    return render_template('home.html')


"""------------------------------------"""
""" Route pour le jeu Chrono Banana  """
"""------------------------------------"""

@socketio.on('join_gameChronoBanane')
def join_gameMotPlusLong():
    joueur_nom = session.get('user_id')
    if not joueur_nom:
        return render_template('index.html')

    if len(joueurEnAttenteCB) < 2 and (joueur_nom not in joueurEnAttenteCB):
        joueurEnAttenteCB.append(joueur_nom)
        emit('update_statusChronoBanane', {'statusChronoBanane': f"{len(joueurEnAttenteCB)}/2 joueurs prêts"}, broadcast=True)

    if len(joueurEnAttenteCB) == 2:
        partie_id = len(partiesChronoBanane) + 1
        partie = JeuBanana() 
        partie.ajoutJoueur(joueurEnAttenteCB[0])
        partie.ajoutJoueur(joueurEnAttenteCB[1])
        for joueur in partie.tabJoueurs:
            joueurEnAttenteCB.remove(joueur.nom)
        partiesChronoBanane[partie_id] = partie
        partiesChronoBanane[partie_id].initialiser_plateau_chrono()
        emit('start_gameChronoBanane', {'partie_id': partie_id}, broadcast=True)

@app.route('/PartieChronoBanane/<int:partie_id>')
def returnPage(partie_id):
    return render_template('indexChronoBanane.html', partie_id=partie_id)


@app.route('/initialiserChronoBanane/<int:partie_id>', methods=['POST'])
def initialiserChronoBanane(partie_id):
    joueur_nom = session.get('user_id')
    print(joueur_nom)
    partie = partiesChronoBanane.get(partie_id)
    for joueur in partie.tabJoueurs:
        #if joueur.nom ==  joueur_nom:
        return jsonify({'plateau': joueur.plateauJeu, 'plateau_joueur': joueur.plateauJoueur, 'partie_id': partie_id})
        #else:
            #return render_template('indexBanana.html')
    return render_template('index.html')


@app.route('/confirmerPlateauChrono/<int:partie_id>', methods=['POST'])
def confirmer_plateauChrono(partie_id):
    user_id = session.get('user_id')
    partie = partiesChronoBanane[partie_id]
    print(partie)
    if not user_id:
        return jsonify({"message": "Partie non initialisée pour cet utilisateur.", "validite": False, 'partie_id': partie_id})

    data = request.get_json()
    partie.plateauProposition = data

    connexe = partie.verifier_connexe(data)
    if connexe:
        mots_extraits = partie.extraireMots(data)
        validite, mots_invalides = partie.comparer_avec_dictionnaire(mots_extraits)
        nouveauPlateau = partie.plateauJeu

        if validite:
            return jsonify({"message": "Tous les mots sont valides dans le dictionnaire, veuillez placer les autres lettres.", "validite": True, "plateau": nouveauPlateau, 'partie_id': partie_id})
        else:
            motsInvalidesStr = ", ".join(mots_invalides)
            return jsonify({"message": f"Le(s) mot(s) {motsInvalidesStr} ne sont/n'est pas dans le dictionnaire.", "validite": False, 'partie_id': partie_id})
    else:
        return jsonify({"message": "Les lettres ajoutées ne sont pas connexes.", "validite": False, 'partie_id': partie_id})
    

@app.route('/rejouerChronoBanane/<int:partie_id>', methods=['POST'])
def rejouerChronoBanane(partie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Aucun utilisateur en session."})

    partiesChronoBanane[partie_id] = JeuBanana()
    partiesChronoBanane[partie_id].initialiser_plateau_joueur()
    

    return jsonify({'plateau': partiesChronoBanane[partie_id].plateauJeu, 'plateau_joueur': partiesChronoBanane[partie_id].plateauJoueur, 'partie_id': partie_id})

@app.route('/quitterChronoBanane', methods=['POST'])
def quitterChronoBanane(): 
    return render_template('home.html')


"""------------------------------------"""
""" Route pour le jeu Banane Cafe  """
"""------------------------------------"""



@socketio.on('join_gameBananeCafe')
def join_gameBananeCafe():
    joueur_nom = session.get('user_id')
    if not joueur_nom:
        return render_template('index.html')

    if len(joueurEnAttenteCAB) < 2 and (joueur_nom not in joueurEnAttenteCAB):
        joueurEnAttenteCAB.append(joueur_nom)
        emit('update_statusBananeCafe', {'statusBananeCafe': f"{len(joueurEnAttenteCAB)}/2 joueurs prêts"}, broadcast=True)

    if len(joueurEnAttenteCAB) == 2:
        partie_id = len(joueurEnAttenteCAB) + 1
        partie = JeuBanana()
        partie.ajoutJoueur(joueurEnAttenteCAB[0])
        partie.ajoutJoueur(joueurEnAttenteCAB[1])
        for joueur in partie.tabJoueurs:
            joueurEnAttenteCAB.remove(joueur.nom)
        partiesCafeBanane[partie_id] = partie

        # Utilisation de la méthode `initialiser_plateau_cafe`
        partie.initialiser_plateau_cafe()
        emit('start_gameBananeCafe', {'partie_id': partie_id}, broadcast=True)


@app.route('/PartieBananeCafe/<int:partie_id>')
def returnPageBananaCafe(partie_id):
    return render_template('indexCafeBanane.html', partie_id=partie_id)


@app.route('/initialiserBananeCafe/<int:partie_id>', methods=['POST'])
def initialiserBananeCafe(partie_id):
    joueur_nom = session.get('user_id')
    partie = partiesCafeBanane.get(partie_id)
    if not partie:
        return jsonify({'error': 'Partie non trouvée'})
    for joueur in partie.tabJoueurs:
        if joueur.nom ==  joueur_nom:
            return jsonify({'plateau': joueur.plateauJeu, 'plateau_joueur': joueur.plateauJoueur, 'partie_id': partie_id})
        
    return render_template('index.html')



@app.route('/echangerTuiles/<int:partie_id>', methods=['POST'])
def echanger_tuiles(partie_id):
    lettre = request.get_json()
    joueur_nom = session.get('user_id')

    # Récupérer la partie correspondante
    partie = partiesCafeBanane.get(partie_id)
    if not partie:
        return jsonify({"success": False, "message": "Partie non trouvée."})

    # Trouver le joueur dans la partie
    print("1")
    joueur = next((j for j in partie.tabJoueurs if j.nom == joueur_nom), None)
    if not joueur:
        return jsonify({"success": False, "message": "Joueur non trouvé dans la partie."})

    # Effectuer l'échange pour ce joueur
    print("2")
    nouvelles_lettres = partie.echanger_tuile(joueur, lettre)
    if nouvelles_lettres:
        print("3")
        return jsonify({"success": True, "nouvelles_lettres": nouvelles_lettres})
    else:
        print("4")
        return jsonify({"success": False, "message": "Impossible d'échanger la tuile."})




@app.route('/confirmerPlateauCafe/<int:partie_id>', methods=['POST'])
def confirmer_plateauCafe(partie_id):
    user_id = session.get('user_id')
    partie = partiesCafeBanane[partie_id]
    print(partie)
    if not user_id:
        return jsonify({"message": "Partie non initialisée pour cet utilisateur.", "validite": False, 'partie_id': partie_id})

    print("test")
    data = request.get_json()
    partie.plateauProposition = data

    connexe = partie.verifier_connexe(data)
    if connexe:
        mots_extraits = partie.extraireMots(data)
        validite, mots_invalides = partie.comparer_avec_dictionnaire(mots_extraits)
        nouveauPlateau = partie.plateauJeu

        if validite:
            return jsonify({"message": "Tous les mots sont valides dans le dictionnaire, veuillez placer les autres lettres.", "validite": True, "plateau": nouveauPlateau, 'partie_id': partie_id})
        else:
            motsInvalidesStr = ", ".join(mots_invalides)
            return jsonify({"message": f"Le(s) mot(s) {motsInvalidesStr} ne sont/n'est pas dans le dictionnaire.", "validite": False, 'partie_id': partie_id})
    else:
        return jsonify({"message": "Les lettres ajoutées ne sont pas connexes.", "validite": False, 'partie_id': partie_id})




@app.route('/rejouerCafeBanane/<int:partie_id>', methods=['POST'])
def rejouerCafeBanane(partie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Aucun utilisateur en session."})

    partiesCafeBanane[partie_id] = JeuBanana()
    partiesCafeBanane[partie_id].initialiser_plateau_cafe()
    

    return jsonify({'plateau': partiesCafeBanane[partie_id].plateauJeu, 'plateau_joueur': partiesCafeBanane[partie_id].plateauJoueur, 'partie_id': partie_id})

@app.route('/quitterCafeBanane', methods=['POST'])
def quitterCafeBanane():
    return render_template('home.html')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8888, debug=True)
