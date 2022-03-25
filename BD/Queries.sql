#post login
select IF(mot_de_passe = '$mdp', (courriel, nom, prenom, id_utilisateur), null)
from utilisateur where courriel = '$courriel';

#post signup
INSERT INTO utilisateur (id_utilisateur, courriel, nom, prenom, mot_de_passe)
    VALUE (md5('$nom'), '$courriel', '$nom', '$prenom', '$mdp');

#get tokenInfo
SELECT courriel, nom, prenom, id_utilisateur FROM utilisateur WHERE token = '$token';

#get parkingList
SELECT * FROM stationnement;

#get parkingList by filters
#price
SELECT * FROM stationnement WHERE prix_min <= $prix AND prix_max >= $prix;

#dimension
SELECT * FROM stationnement WHERE longueur >= $longueur AND largeur >= $largeur AND hauteur >= $hauteur;

#jour d'avance
SELECT * FROM stationnement WHERE jours_d_avance >= $jours_d_avance;

#date de fin
SELECT * FROM stationnement WHERE date_fin >= $date;

#get parkingListId
SELECT * FROM stationnement WHERE id_stationnement = '$id_stationnement';

#post parking
INSERT INTO stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin)
    VALUE ('$id_stationnement', '$prix', '$longueur', '$largeur', '$hauteur', '$emplacement',
           '$jours_d_avance', '$date_fin');

#delete parking
DELETE FROM stationnement WHERE id_stationnement = '$id_stationnement';

#get plageHoraire by stationnement_id
SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                  (SELECT id_plage_horaire FROM possede WHERE id_stationnement = '$id_stationnement');

#get plageHoraire by stationnement_id and jour
SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                  (SELECT id_plage_horaire FROM possede WHERE id_stationnement = '$id_stationnement')
                                  AND '$jour' BETWEEN date_arrivee AND date_depart;

#post plageHoraire by stationnement_id
INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart)
    VALUE ('$id_plage_horaire', '$date_arrivee', '$date_depart');
INSERT INTO possede (id_plage_horaire, id_stationnement)
    VALUE ('$id_plage_horaire', '$id_stationnement');

#delete plageHoraire by stationnement_id
DELETE FROM Plage_horaire WHERE id_plage_horaire = '$id_plage_horaire';
DELETE FROM possede WHERE id_stationnement = '$id_stationnement' AND id_plage_horaire = '$id_plage_horaire';

#get user by id
SELECT * FROM utilisateur WHERE id_utilisateur = '$id_utilisateur';

#get parking by user id
SELECT * FROM stationnement WHERE id_stationnement IN
                                  (SELECT id_stationnement FROM gerer WHERE id_utilisateur = '$id_utilisateur');

#get vehicule by user id
SELECT * FROM vehicule WHERE plaque IN
                                  (SELECT plaque FROM Appartient WHERE id_utilisateur = '$id_utilisateur');

#post vehicule by user id
INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur)
    VALUES ('$plaque', '$modele', '$couleur', '$longueur', '$largeur', '$hauteur');
INSERT INTO Appartient (plaque, id_utilisateur)
    VALUES ('$plaque', '$id_utilisateur');