import collections
from msilib import type_binary
from multiprocessing import context
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

from OpenSSL import crypto

# with open("/", "r") as file:
#     data = file.read()

# x509 = crypto.load_certificate(crypto.FILETYPE_PEM, data);

# p12 = crypto.PKCS12()
# p12.set_certificate(x509)


app = Flask(__name__)

CORS(app)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'application_parking'
app.config['SECRET_KEY'] = 'thisissecret'

mysql = MySQL(app)


def get_token_from_request(requestHeaders):
    token = requestHeaders.get('Authorization')
    if token is None:
        return None
    return token.split(' ')[1]


@app.route('/', methods=['GET'])
def home():
    if(request.method == 'GET'):
        return 'API is running'


@app.route('/login', methods=['POST'])
def login():
    try:
        if(request.method == 'POST'):
            # Get data from request
            data = request.get_json()
            courriel = data['courriel']
            password = data['password']

            # Create cursor
            cur = mysql.connection.cursor()

            # Get user by username
            result = cur.execute(
                "SELECT mot_de_passe FROM utilisateur WHERE courriel = %s", [courriel])

            if result > 0:
                # Get stored hash
                data = cur.fetchone()
                password_hash = data[0]

                # Compare passwords
                if(check_password_hash(password_hash, password)):
                    cur.execute(
                        "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE courriel = %s", [courriel])
                    utilisateur = cur.fetchall()
                    objUtilisateur = []
                    for row in utilisateur:
                        d = collections.OrderedDict()
                        d['courriel'] = row[0]
                        d['nom'] = row[1]
                        d['prenom'] = row[2]
                        d['token'] = row[3]
                        d['id_utilisateur'] = row[4]
                        objUtilisateur.append(d)
                    return jsonify(objUtilisateur)
                else:
                    return jsonify({'message': 'Mot de passe incorrect'})
            else:
                return jsonify({'message': 'Utilisateur non trouvé'})
    except Exception as e:
        return str(e)


@app.route('/signup', methods=['POST'])
def signup():
    try:
        if(request.method == 'POST'):
            # Get data from request
            data = request.get_json()
            courriel = data['courriel']
            nom = data['nom']
            prenom = data['prenom']
            password = generate_password_hash(data['password'])

            # Create cursor
            cur = mysql.connection.cursor()

            # Check if user already exists
            result = cur.execute(
                "SELECT * FROM utilisateur WHERE courriel = %s", [courriel])

            if result > 0:
                return jsonify({'message': 'Utilisateur déjà existant'})

            # Create new user
            cur.execute("INSERT INTO utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe) VALUES (md5(%s), sha1(%s), %s, %s, %s, %s)",
                        (courriel, courriel, courriel, nom, prenom, password))

            # Commit to DB
            mysql.connection.commit()

            # Return user info
            cur.execute(
                "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE courriel = %s", [courriel])
            utilisateur = cur.fetchall()
            objUtilisateur = []
            for row in utilisateur:
                d = collections.OrderedDict()
                d['courriel'] = row[0]
                d['nom'] = row[1]
                d['prenom'] = row[2]
                d['token'] = row[3]
                d['id_utilisateur'] = row[4]
                objUtilisateur.append(d)
            return jsonify(objUtilisateur)
    except Exception as e:
        return str(e)


@app.route('/tokenInfo', methods=['GET'])
def tokenInfo():
    try:
        if(request.method == 'GET'):
            auth_token = get_token_from_request(request.headers)

            # Create cursor
            cur = mysql.connection.cursor()

            # Get user by username
            result = cur.execute(
                "SELECT token FROM utilisateur WHERE token = %s", [auth_token])

            if result > 0:
                # Get stored hash
                data = cur.fetchone()
                token_hash = data[0]

                # Compare tokens
                if(token_hash == auth_token):
                    cur.execute(
                        "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE token = %s", [auth_token])
                    utilisateur = cur.fetchall()
                    objUtilisateur = []
                    for row in utilisateur:
                        d = collections.OrderedDict()
                        d['courriel'] = row[0]
                        d['nom'] = row[1]
                        d['prenom'] = row[2]
                        d['token'] = row[3]
                        d['id_utilisateur'] = row[4]
                        objUtilisateur.append(d)
                    return jsonify(objUtilisateur)
                else:
                    return jsonify({'message': 'Token incorrect'})
            else:
                return jsonify({'message': 'Utilisateur non trouvé'})
    except Exception as e:
        return str(e)


@app.route('/parkingList', methods=['GET'])
def parkingList():
    try:
        if(request.method == 'GET'):
            prixMin = request.args.get('prixMin')
            prixMax = request.args.get('prixMax')
            longueur = request.args.get('longueur')
            largeur = request.args.get('largeur')
            hauteur = request.args.get('hauteur')
            joursAvance = request.args.get('joursDavance')
            dateFin = request.args.get('dateFin')
            cur = mysql.connection.cursor()
            cur.execute("call select_parkingList(%s, %s, %s, %s, %s, %s, %s)",
                        (prixMin, prixMax, longueur, largeur, hauteur, joursAvance, dateFin))
            parking = cur.fetchall()
            objParking = []
            for row in parking:
                d = collections.OrderedDict()
                d['id_stationnement'] = row[0]
                d['prix'] = row[1]
                d['longueur'] = row[2]
                d['largeur'] = row[3]
                d['hauteur'] = row[4]
                d['emplacement'] = row[5]
                d['jours_d_avance'] = row[6]
                d['date_fin'] = row[7]
                objParking.append(d)
            return jsonify(objParking)
    except Exception as e:
        return str(e)


@ app.route('/parking/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def parking(id):
    try:
        if(request.method == 'GET'):
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM stationnement WHERE id_stationnement=%s", [id])
            parking = cur.fetchall()
            objParking = []
            for row in parking:
                d = collections.OrderedDict()
                d['id_stationnement'] = row[0]
                d['prix'] = row[1]
                d['longueur'] = row[2]
                d['largeur'] = row[3]
                d['hauteur'] = row[4]
                d['emplacement'] = row[5]
                d['jours_d_avance'] = row[6]
                d['date_fin'] = row[7]
                objParking.append(d)
            return jsonify(objParking)
        elif(request.method == 'POST'):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin) VALUE (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (id, data['prix'], data['longueur'], data['largeur'], data['hauteur'], data['emplacement'], data['jours_d_avance'], data['date_fin']))
            cur.execute("INSERT INTO gerer (id_stationnement, id_utilisateur) VALUE (%s, %s)",
                        (id, data['id_utilisateur']))
            cur.execute(
                "INSERT INTO Locateur (id_utilisateur, cote) VALUE (%s, NULL) ON DUPLICATE KEY UPDATE id_utilisateur = id_utilisateur", [data['id_utilisateur']])
            mysql.connection.commit()
            return 'Parking ajoutée'
        elif(request.method == 'PUT'):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("UPDATE stationnement SET prix=%s, longueur=%s, largeur=%s, hauteur=%s, emplacement=%s, jours_d_avance=%s, date_fin=%s WHERE id_stationnement=%s",
                        (data['prix'], data['longueur'], data['largeur'], data['hauteur'], data['emplacement'], data['jours_d_avance'], data['date_fin'], id))
            mysql.connection.commit()
            return 'Parking updated'
        elif(request.method == 'DELETE'):
            cur = mysql.connection.cursor()
            cur.execute(
                "call delete_stationnement(%s)", [id])
            mysql.connection.commit()
            return 'Parking supprimée'
    except Exception as e:
        return str(e)


@ app.route('/parking/<int:parkingId>/plageHoraires', methods=['GET'])
def plageHoraires(parkingId):
    try:
        if(request.method == 'GET'):
            debut = (request.args.get('debut'))
            if(debut is not None):
                debut.replace("%20", " ")
            fin = (request.args.get('fin'))
            if(fin is not None):
                fin.replace("%20", " ")
            cur = mysql.connection.cursor()
            cur.execute("call select_plageHoraire(%s, %s, %s)",
                        (debut, fin, parkingId))
            plageHoraires = cur.fetchall()
            objPlageHoraires = []
            for row in plageHoraires:
                d = collections.OrderedDict()
                d['id_plage_horaires'] = row[0]
                d['date_arrivee'] = row[1]
                d['date_depart'] = row[2]
                objPlageHoraires.append(d)
            return jsonify(objPlageHoraires)
    except Exception as e:
        return str(e)


@ app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>/reserver', methods=['POST'])
def reserver(parkingId, plageHoraireId):
    try:
        if(request.method == 'POST'):

            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("call insert_plageHoraire_reserver(%s, %s, %s, %s, %s)",
                        (data['date_arrivee'], data['date_depart'], parkingId, plageHoraireId, data['id_utilisateur']))
            mysql.connection.commit()
            return 'Plage reservation ajoutée'
    except Exception as e:
        return str(e)


@ app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>/inoccupable', methods=['POST'])
def inoccupable(parkingId, plageHoraireId):
    try:
        if(request.method == 'POST'):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("call insert_plageHoraire_inoccupable(%s, %s, %s, %s, %s)",
                        (data['date_arrivee'], data['date_depart'], parkingId, plageHoraireId, data['id_utilisateur']))
            mysql.connection.commit()
            return 'Plage inoccupable ajoutée'
    except Exception as e:
        return str(e)


@ app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>', methods=['DELETE'])
def deletePlageHoraire(parkingId, plageHoraireId):
    try:
        if(request.method == 'DELETE'):
            cur = mysql.connection.cursor()
            cur.execute(
                "call delete_plageHoraire ((SELECT id_plage_horaire FROM Possede WHERE id_plage_horaire = %s AND id_stationnement = %s))",
                (plageHoraireId, parkingId))
            mysql.connection.commit()
            return 'Plage horaire supprimée'
    except Exception as e:
        return str(e)


@ app.route('/user/<string:id>', methods=['GET', 'DELETE'])
def utilisateur_id(id):
    try:
        if(request.method == 'GET'):
            cur = mysql.connection.cursor()
            utilisateur = cur.execute(
                "SELECT * FROM (SELECT id_utilisateur, courriel, nom, prenom FROM Utilisateur WHERE id_utilisateur = %s) AS infos INNER JOIN (SELECT IF (%s IN (SELECT id_utilisateur FROM Locateur), (SELECT cote FROM Locateur WHERE id_utilisateur = %s), NULL)) AS cote", (id, id, id))
            utilisateur = cur.fetchall()
            objUtilisateur = []
            for row in utilisateur:
                d = collections.OrderedDict()
                d['id_utilisateur'] = row[0]
                d['courriel'] = row[1]
                d['nom'] = row[2]
                d['prenom'] = row[3]
                if row[4] is not None:
                    d['cote'] = row[4]
                objUtilisateur.append(d)
            return jsonify(objUtilisateur)
        if(request.method == 'DELETE'):
            auth_token = get_token_from_request(request.headers)
            cur = mysql.connection.cursor()
            if auth_token is None:
                return 'Token manquant'
            cur.execute(
                "call delete_user(%s);", [id])
            mysql.connection.commit()
            return 'Utilisateur supprimé'
    except Exception as e:
        return str(e)


@ app.route('/user/<string:id>/parkingList', methods=['GET'])
def utilisateur_id_parkingList(id):
    try:
        if(request.method == 'GET'):
            cur = mysql.connection.cursor()
            parking = cur.execute(
                "SELECT * FROM stationnement WHERE id_stationnement IN (SELECT id_stationnement FROM gerer WHERE id_utilisateur = %s)", [id])
            parking = cur.fetchall()
            objParking = []
            for row in parking:
                d = collections.OrderedDict()
                d['id_stationnement'] = row[0]
                d['prix'] = row[1]
                d['longueur'] = row[2]
                d['largeur'] = row[3]
                d['hauteur'] = row[4]
                d['emplacement'] = row[5]
                d['jours_d_avance'] = row[6]
                d['date_fin'] = row[7]
                objParking.append(d)
            return jsonify(objParking)
    except Exception as e:
        return str(e)


@ app.route('/user/<string:id>/cars', methods=['GET', 'POST'])
def utilisateur_id_cars(id):
    try:
        if(request.method == 'GET'):
            cur = mysql.connection.cursor()
            vehicule = cur.execute(
                "SELECT * FROM vehicule WHERE plaque IN (SELECT plaque FROM Appartient WHERE id_utilisateur = %s)", [id])
            vehicule = cur.fetchall()
            objvehicule = []
            for row in vehicule:
                d = collections.OrderedDict()
                d['plaque'] = row[0]
                d['modele'] = row[1]
                d['couleur'] = row[2]
                d['longueur'] = row[3]
                d['largeur'] = row[4]
                d['hauteur'] = row[5]
                objvehicule.append(d)
            return jsonify(objvehicule)
        if(request.method == 'POST'):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur) VALUE (%s, %s, %s, %s, %s, %s)",
                        (data['plaque'], data['modele'], data['couleur'], data['longueur'], data['largeur'], data['hauteur']))
            cur.execute("INSERT INTO Appartient (plaque, id_utilisateur) VALUE (%s, %s)",
                        (data['plaque'], id))
            cur.execute(
                "INSERT INTO locataire (id_utilisateur) VALUE (%s) ON DUPLICATE KEY UPDATE id_utilisateur = id_utilisateur", [id])
            mysql.connection.commit()
            return 'Voiture ajoutée'
    except Exception as e:
        return str(e)


@ app.route('/user/<string:id_utilisateur>/cars/<string:plaque>', methods=['PUT', 'DELETE'])
def cars_id(plaque):
    try:
        if(request.method == 'PUT'):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Vehicule SET modele=%s, couleur=%s, longueur=%s, largeur=%s, hauteur=%s WHERE plaque=%s",
                        (data['modele'], data['couleur'], data['longueur'], data['largeur'], data['hauteur'], plaque))
            mysql.connection.commit()
            return 'Voiture modifiée'
        if(request.method == 'DELETE'):
            cur = mysql.connection.cursor()
            cur.execute("call delete_voiture(%s)", [plaque])
            mysql.connection.commit()
            return 'Voiture supprimée'
    except Exception as e:
        return str(e)


@ app.route('/user/<string:id_utilisateur_locataire>/evalue/<string:id_utilisateur_locateur>', methods=['POST'])
def evalue(id_utilisateur_locataire, id_utilisateur_locateur):
    try:
        if(request.method == 'POST'):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Evalue (id_utilisateur_locataire, id_utilisateur_locateur, cote) VALUE (%s, %s, %s)",
                        (id_utilisateur_locataire, id_utilisateur_locateur, data['cote']))
            mysql.connection.commit()
            return 'Evaluation ajoutée'
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(ssl_context=('./cert.crt', './certKey.key'), debug=True)
