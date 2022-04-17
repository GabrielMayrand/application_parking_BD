import collections
import datetime
import jwt
from msilib import type_binary
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'application_parking'
app.config['SECRET_KEY'] = 'thisissecret'

mysql = MySQL(app)

def encode_auth_token(self, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'



@app.route('/', methods=['GET'])
def home():
    if(request.method == 'GET'):
        return 'API is running'


@app.route('/login', methods=['POST'])
def login():
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


@app.route('/signup', methods=['POST'])
def signup():
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
        cur.execute("INSERT INTO utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe) VALUES (md5(%s), sha1(md5(%s)), %s, %s, %s, %s)",
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


@app.route('/tokenInfo', methods=['GET'])
def tokenInfo():
    if(request.method == 'GET'):
        # Get token from request
        token = request.args.get('token')
        print(token)

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute(
            "SELECT token FROM utilisateur WHERE token = %s", [token])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            token_hash = data[0]

            # Compare tokens
            if(token_hash == token):
                cur.execute(
                    "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE token = %s", [token])
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


# parkinglist filters
@app.route('/parkingList', methods=['GET'])
def parkingList():
    if(request.method == 'GET'):
        prixMin = request.args.get('prixMin')
        prixMax = request.args.get('prixMax')
        longueur = request.args.get('longueur')
        largeur = request.args.get('largeur')
        hauteur = request.args.get('hauteur')
        joursAvance = request.args.get('joursDavance')
        dateFin = request.args.get('dateFin')
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE IF EXISTS tempStationnement")
        cur.execute(
            "CREATE TEMPORARY TABLE IF NOT EXISTS tempStationnement AS (SELECT * FROM stationnement)")
        if prixMin is not None and prixMax is not None:
            cur.execute(
                "DELETE FROM tempStationnement WHERE id_stationnement NOT IN (SELECT id_stationnement FROM stationnement WHERE %s <= prix AND %s >= prix)", (prixMin, prixMax))
        if longueur is not None and largeur is not None and hauteur is not None:
            cur.execute(
                "DELETE FROM tempStationnement WHERE id_stationnement NOT IN (SELECT id_stationnement FROM stationnement WHERE %s <= longueur AND %s <= largeur AND %s <= hauteur)", (longueur, largeur, hauteur))
        if joursAvance is not None:
            cur.execute(
                "DELETE FROM tempStationnement WHERE id_stationnement NOT IN (SELECT id_stationnement FROM stationnement WHERE jours_d_avance <= %s)", [joursAvance])
        if dateFin is not None:
            cur.execute(
                "DELETE FROM tempStationnement WHERE id_stationnement NOT IN (SELECT id_stationnement FROM stationnement WHERE date_fin >= %s)", [dateFin])
        cur.execute("SELECT * FROM tempStationnement")
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


@ app.route('/parking/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def parking(id):
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
            "DELETE FROM stationnement WHERE id_stationnement=%s", [id])
        cur.execute(
            "DELETE FROM gerer WHERE id_stationnement=%s", [id])
        cur.execute(
            "DELETE FROM possede WHERE id_stationnement=%s", [id])
        mysql.connection.commit()
        return 'Parking supprimée'


# filters
@ app.route('/parking/<int:parkingId>/plageHoraires', methods=['GET'])
def plageHoraires(parkingId):
    if(request.method == 'GET'):
        debut = (request.args.get('debut')).replace("+", " ")
        fin = (request.args.get('fin')).replace("+", " ")
        cur = mysql.connection.cursor()
        if debut is not None and fin is not None:
            cur.execute(
                "SELECT * FROM Plage_horaire WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM possede WHERE id_stationnement=%s) AND %s >= date_arrivee AND %s <= date_depart", (parkingId, debut, fin))
        elif debut is not None and fin is None:
            cur.execute(
                "SELECT * FROM Plage_horaire WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM possede WHERE id_stationnement=%s) AND %s >= date_arrivee", (parkingId, debut))
        elif debut is None and fin is not None:
            cur.execute(
                "SELECT * FROM Plage_horaire WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM possede WHERE id_stationnement=%s) AND %s <= date_depart", (parkingId, fin))
        else:
            cur.execute(
                "SELECT * FROM Plage_horaire WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM possede WHERE id_stationnement=%s)", [parkingId])
        plageHoraires = cur.fetchall()
        objPlageHoraires = []
        for row in plageHoraires:
            d = collections.OrderedDict()
            d['id_plage_horaires'] = row[0]
            d['date_arrivee'] = row[1]
            d['date_depart'] = row[2]
            objPlageHoraires.append(d)
        return jsonify(objPlageHoraires)


@ app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>/reserver', methods=['POST'])
def reserver(parkingId, plageHoraireId):
    if(request.method == 'POST'):
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart) VALUE (%s, %s, %s)",
                    (plageHoraireId, data['date_arrivee'], data['date_depart']))
        cur.execute("INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUE (%s, %s)",
                    (plageHoraireId, parkingId))
        cur.execute("INSERT INTO louer (id_plage_horaire, id_utilisateur) VALUE (%s, %s)", 
                    (plageHoraireId, data['id_utilisateur']))
        cur.execute("INSERT INTO Reservation (id_plage_horaire) VALUE (%s)", [plageHoraireId])
        mysql.connection.commit()
        return 'Plage reservation ajoutée'


@ app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>/inoccupable', methods=['POST'])
def inoccupable(parkingId, plageHoraireId):
    if(request.method == 'POST'):
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart) VALUE (%s, %s, %s)",
                    (plageHoraireId, data['date_arrivee'], data['date_depart']))
        cur.execute("INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUE (%s, %s)",
                    (plageHoraireId, parkingId))
        cur.execute("INSERT INTO Retirer (id_plage_horaire, id_utilisateur) VALUE (%s, %s)",
                    (plageHoraireId, data['id_utilisateur']))
        cur.execute("INSERT INTO Inoccupable (id_plage_horaire) VALUE (%s)", [plageHoraireId])
        mysql.connection.commit()
        return 'Plage inoccupable ajoutée'


@ app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>', methods=['DELETE'])
def deletePlageHoraire(parkingId, plageHoraireId):
    if(request.method == 'DELETE'):
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM Reservation WHERE id_plage_horaire=%s", [plageHoraireId])
        cur.execute(
            "DELETE FROM Inoccupable WHERE id_plage_horaire=%s", [plageHoraireId])
        cur.execute("DELETE FROM louer WHERE id_plage_horaire = %s", [plageHoraireId])
        cur.execute("DELETE FROM retirer WHERE id_plage_horaire = %s", [plageHoraireId])
        cur.execute(
            "DELETE FROM Plage_horaire WHERE id_plage_horaire=%s", [plageHoraireId])
        cur.execute(
            "DELETE FROM Possede WHERE id_stationnement = %s AND id_plage_horaire=%s", (parkingId, plageHoraireId))
        mysql.connection.commit()
        return 'Plage horaire supprimée'


@ app.route('/user/<string:id>', methods=['GET', 'DELETE'])
def utilisateur_id(id):
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
        token = request.args.get('token')
        cur = mysql.connection.cursor()
        if token is None:
            return 'Token manquant'
        cur.execute("SELECT id_utilisateur FROM Utilisateur WHERE token = %s", [token])
        utilisateur = cur.fetchone()
        if utilisateur is None:
            return 'Token invalide'
        cur.execute(
            "DELETE FROM Utilisateur WHERE id_utilisateur = %s AND token = %s", (id, token))
        mysql.connection.commit()
        return 'Utilisateur supprimé'


@ app.route('/user/<string:id>/parkingList', methods=['GET'])
def utilisateur_id_parkingList(id):
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


@ app.route('/user/<string:id>/cars', methods=['GET', 'POST'])
def utilisateur_id_cars(id):
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


@ app.route('/user/<string:id_utilisateur>/cars/<string:plaque>', methods=['PUT', 'DELETE'])
def cars_id(id_utilisateur, plaque):
    if(request.method == 'PUT'):
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Vehicule SET modele=%s, couleur=%s, longueur=%s, largeur=%s, hauteur=%s WHERE plaque=%s",
                    (data['modele'], data['couleur'], data['longueur'], data['largeur'], data['hauteur'], plaque))
        mysql.connection.commit()
        return 'Voiture modifiée'
    if(request.method == 'DELETE'):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Vehicule WHERE plaque=%s", [plaque])
        cur.execute("DELETE FROM Appartient WHERE plaque=%s", [plaque])
        mysql.connection.commit()
        return 'Voiture supprimée'


@ app.route('/user/<string:id_utilisateur_locataire>/evalue/<string:id_utilisateur_locateur>', methods=['POST'])
def evalue(id_utilisateur_locataire, id_utilisateur_locateur):
    if(request.method == 'POST'):
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Evalue (id_utilisateur_locataire, id_utilisateur_locateur, cote) VALUE (%s, %s, %s)",
                    (id_utilisateur_locataire, id_utilisateur_locateur, data['cote']))
        mysql.connection.commit()
        return 'Evaluation ajoutée'


if __name__ == '__main__':
    app.run(debug=True)
