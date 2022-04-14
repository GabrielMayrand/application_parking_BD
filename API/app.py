from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'application_parking'

mysql = MySQL(app)


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
            "SELECT * FROM users WHERE courriel = %s", [courriel])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password_hash = data['password']

            # Compare passwords
            if(password_hash == password):
                cur.execute(
                    "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE courriel = %s", [courriel])
                utilisateur = cur.fetchall()
                return jsonify(utilisateur)
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
        password = data['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Check if user already exists
        result = cur.execute(
            "SELECT * FROM users WHERE courriel = %s", [courriel])

        if result > 0:
            return jsonify({'message': 'Utilisateur déjà existant'})

        # Create new user
        cur.execute("INSERT INTO utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe) VALUES (md5(%s), sha1(md5(%s)), %s, %s, %s, %s)",
                    (nom, nom, courriel, nom, prenom, password))

        # Commit to DB
        mysql.connection.commit()

        # Return user info
        cur.execute(
            "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE courriel = %s", [courriel])
        utilisateur = cur.fetchall()
        return jsonify(utilisateur)


@app.route('/tokenInfo', methods=['GET'])
def tokenInfo():
    if(request.method == 'GET'):
        # Get token from request
        token = request.args.get('token')

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute(
            "SELECT * FROM utilisateur WHERE token = %s", [token])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            token_hash = data['token']

            # Compare tokens
            if(token_hash == token):
                cur.execute(
                    "SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE token = %s", [token])
                utilisateur = cur.fetchall()
                return jsonify(utilisateur)
            else:
                return jsonify({'message': 'Token incorrect'})
        else:
            return jsonify({'message': 'Utilisateur non trouvé'})


@app.route('/parkingList', methods=['GET'])
def parkingList():
    if(request.method == 'GET'):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM stationnement")
        parking = cur.fetchall()
        parking = [dict(row) for row in parking]
        return json.dumps(parking)


# parkinglist filters


@app.route('/parking/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def parking(id):
    if(request.method == 'GET'):
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM stationnement WHERE id_stationnement=%s", [id])
        parking = cur.fetchall()
        return jsonify(parking)
    elif(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin) VALUE (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, request.json['prix'], request.json['longueur'], request.json['largeur'], request.json['hauteur'], request.json['emplacement'], request.json['jours_d_avance'], request.json['date_fin']))
        cur.execute("INSERT INTO gerer (id_stationnement, id_utilisateur) VALUE (%s, %s)",
                    (id, request.json['id_utilisateur']))
        cur.execute(
            "INSERT INTO Locateur (id_utilisateur, cote) VALUE (%s, NULL)", [id])
        mysql.connection.commit()
        return 'Parking ajoutée'
    elif(request.method == 'PUT'):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE stationnement SET prix=%s, longueur=%s, largeur=%s, hauteur=%s, emplacement=%s, jours_d_avance=%s, date_fin=%s WHERE id_stationnement=%s",
                    (request.json['prix'], request.json['longueur'], request.json['largeur'], request.json['hauteur'], request.json['emplacement'], request.json['jours_d_avance'], request.json['date_fin'], id))
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


# parking filter et pas filter


@app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>/reserver', methods=['POST'])
def reserver(parkingId, plageHoraire):
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart) VALUE (%s, %s, %s)",
                    (plageHoraire, request.json['date_arrivee'], request.json['date_depart']))
        cur.execute("INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUE (%s, %s)",
                    (plageHoraire, parkingId))
        cur.execute("INSERT INTO Reservation (id_plage_horaire, id_utilisateur) VALUE (%s, %s)",
                    (plageHoraire, request.json['id_utilisateur']))
        mysql.connection.commit()
        return 'Plage reservation ajoutée'


@app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>/inoccupable', methods=['POST'])
def inoccupable(parkingId, plageHoraire):
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart) VALUE (%s, %s, %s)",
                    (plageHoraire, request.json['date_arrivee'], request.json['date_depart']))
        cur.execute("INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUE (%s, %s)",
                    (plageHoraire, parkingId))
        cur.execute("INSERT INTO Inoccupable (id_plage_horaire, id_utilisateur) VALUE (%s, %s)",
                    (plageHoraire, request.json['id_utilisateur']))
        mysql.connection.commit()
        return 'Plage inoccupable ajoutée'


@app.route('/parking/<int:parkingId>/plageHoraires/<int:plageHoraireId>', methods=['DELETE'])
def deletePlageHoraire(parkingId, plageHoraire):
    if(request.method == 'DELETE'):
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM Reservation WHERE id_plage_horaire=%s", [plageHoraire])
        cur.execute(
            "DELETE FROM Inoccupable WHERE id_plage_horaire=%s", [plageHoraire])
        cur.execute(
            "DELETE FROM Plage_horaire WHERE id_plage_horaire=%s", [plageHoraire])
        cur.execute(
            "DELETE FROM Possede WHERE id_stationnement = %s AND id_plage_horaire=%s", (parkingId, plageHoraire))
        mysql.connection.commit()
        return 'Plage horaire supprimée'


@app.route('/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def utilisateur_id(id):
    if(request.method == 'GET'):
        cur = mysql.connection.cursor()
        utilisateurs = cur.execute(
            "SELECT IF (%s IN (SELECT id_utilisateur FROM Locateur), (SELECT * FROM Locateur WHERE id_utilisateur = %s), (SELECT * FROM Locataire WHERE id_utilisateur = %s))", (id, id, id))
        utilisateurs = cur.fetchall()
        return jsonify(utilisateurs)
    if(request.method == 'PUT'):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE utilisateur SET nom=%s, prenom=%s, email=%s, mot_de_passe=%s WHERE id_utilisateur=%s",
                    (request.json['nom'], request.json['prenom'], request.json['email'], request.json['mot_de_passe'], id))
        mysql.connection.commit()
        return 'Utilisateur modifié'
    if(request.method == 'DELETE'):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Utilisateur WHERE id_utilisateur=%s", [id])
        mysql.connection.commit()
        return 'Utilisateur supprimé'


@app.route('/user/<int:id>/parkingList', methods=['GET'])
def utilisateur_id_parkingList(id):
    if(request.method == 'GET'):
        cur = mysql.connection.cursor()
        utilisateurs = cur.execute(
            "SELECT * FROM stationnement WHERE id_stationnement IN (SELECT id_stationnement FROM gerer WHERE id_utilisateur = %s)", [id])
        utilisateurs = cur.fetchall()
        return jsonify(utilisateurs)


@app.route('/user/<int:id>/cars', methods=['GET', 'POST'])
def utilisateur_id_cars(id):
    if(request.method == 'GET'):
        cur = mysql.connection.cursor()
        utilisateurs = cur.execute(
            "SELECT * FROM vehicule WHERE plaque IN (SELECT plaque FROM Appartient WHERE id_utilisateur = %s", [id])
        utilisateurs = cur.fetchall()
        return jsonify(utilisateurs)
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur) VALUE (%s, %s, %s, %s, %s, %s)",
                    (request.json['plaque'], request.json['modele'], request.json['couleur'], request.json['longueur'], request.json['largeur'], request.json['hauteur']))
        cur.execute("INSERT INTO Appartient (plaque, id_utilisateur) VALUE (%s, %s)",
                    (request.json['plaque'], id))
        cur.execute("INSERT INTO locataire (id_utilisateur) VALUE (%s)", [id])
        mysql.connection.commit()
        return 'Voiture ajoutée'


@app.route('/user/<int:id_utilisateur>/cars/<string:plaque>', methods=['PUT', 'DELETE'])
def cars_id(id_utilisateur, plaque):
    if(request.method == 'PUT'):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Vehicule SET modele=%s, couleur=%s, longueur=%s, largeur=%s, hauteur=%s WHERE plaque=%s",
                    (request.json['modele'], request.json['couleur'], request.json['longueur'], request.json['largeur'], request.json['hauteur'], plaque))
        mysql.connection.commit()
        return 'Voiture modifiée'
    if(request.method == 'DELETE'):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Vehicule WHERE plaque=%s", [plaque])
        cur.execute("DELETE FROM Appartient WHERE plaque=%s", [plaque])
        mysql.connection.commit()
        return 'Voiture supprimée'


@app.route('/user/<int:id_utilisateur_locataire>/evalue/<int:id_utilisateur_locateur>', methods=['POST'])
def evalue(id_utilisateur_locataire, id_utilisateur_locateur):
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Evalue (id_utilisateur_locataire, id_utilisateur_locateur, cote) VALUE (%s, %s, %s)",
                    (id_utilisateur_locataire, id_utilisateur_locateur, request.json['cote']))
        mysql.connection.commit()
        return 'Evaluation ajoutée'


if __name__ == '__main__':
    app.run(debug=True)
