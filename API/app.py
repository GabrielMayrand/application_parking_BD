from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

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


#################### login and all


@app.route('/parkingList', methods=['GET'])
def parkingList():
    if(request.method == 'GET'):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM stationnement")
        parking = cur.fetchall()
        return jsonify(parking)


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
        return 'Parking created'
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
        return 'Parking deleted'


# parking filter


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
            "SELECT courriel, nom, prenom, id_utilisateur FROM utilisateur WHERE id_utilisateur=%s", [id])
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
