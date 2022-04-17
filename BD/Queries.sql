--post login
SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE courriel = '$courriel';

--post signup
INSERT INTO utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe)
    VALUE (md5('$nom'), sha1(md5('$nom')), '$courriel', '$nom', '$prenom', '$mdp');
SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE id_utilisateur = md5('$nom');

--get tokenInfo
SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE token = '$token';

--get parkingList
DROP TABLE IF EXISTS tempStationnement;
CREATE TEMPORARY TABLE IF NOT EXISTS tempStationnement AS (SELECT * FROM stationnement);
SELECT * FROM tempStationnement;

--get parkingList by filters
--price
DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                    (SELECT id_stationnement FROM stationnement WHERE $prix_min <= prix AND $prix_max >= prix);
SELECT * FROM tempStationnement;

--dimension
DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                    (SELECT id_stationnement FROM stationnement WHERE longueur >= $longueur AND largeur >= $largeur AND hauteur >= $hauteur);
SELECT * FROM tempStationnement;

--jour davance
DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                    (SELECT id_stationnement FROM stationnement WHERE jours_d_avance <= $jours_d_avance);
SELECT * FROM tempStationnement;

--date de fin
DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                    (SELECT id_stationnement FROM stationnement WHERE date_fin >= $date);
SELECT * FROM tempStationnement;

--get parkingListId
SELECT * FROM stationnement
    WHERE id_stationnement = '$id_stationnement';

--post parking
INSERT INTO stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin)
    VALUE ('$id_stationnement', $prix, $longueur, $largeur, $hauteur, '$emplacement',
           $jours_d_avance, '$date_fin');
INSERT INTO gerer (id_stationnement, id_utilisateur) VALUE ('$id_stationnement', '$id_utilisateur');
INSERT INTO Locateur (id_utilisateur, cote) VALUE ('$id_utilisateur', NULL) ON DUPLICATE KEY UPDATE id_utilisateur = id_utilisateur;

--put parking
UPDATE stationnement SET prix = $prix, longueur = $longueur, largeur = $largeur, hauteur = $hauteur,
    emplacement = '$emplacement', jours_d_avance = $jours_d_avance, date_fin = '$date_fin'
    WHERE id_stationnement = '$id_stationnement';

--delete parking
DELETE FROM stationnement WHERE id_stationnement = '$id_stationnement';
DELETE FROM gerer WHERE id_stationnement = '$id_stationnement';
DELETE FROM Possede WHERE id_stationnement = '$id_stationnement';

--get plageHoraire by stationnement_id
SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                  (SELECT id_plage_horaire FROM possede WHERE id_stationnement = '$id_stationnement');

--get plageHoraire by stationnement_id and jour
SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                             (SELECT id_plage_horaire FROM possede WHERE id_stationnement = '$id_stationnement')
                              AND '$date' BETWEEN date_arrivee AND date_depart;

--post Reservation plageHoraire by stationnement_id
INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart)
    VALUE ('$id_plage_horaire', '$date_arrivee', '$date_depart');
INSERT INTO possede (id_plage_horaire, id_stationnement)
    VALUE ('$id_plage_horaire', '$id_stationnement');
INSERT INTO Reservation (id_plage_horaire, id_utilisateur)
    VALUE ('$id_plage_horaire', '$id_utilisateur');

--post Inoccupable plageHoraire by stationnement_id
INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart)
    VALUE ('$id_plage_horaire', '$date_arrivee', '$date_depart');
INSERT INTO possede (id_plage_horaire, id_stationnement)
    VALUE ('$id_plage_horaire', '$id_stationnement');
INSERT INTO Inoccupable (id_plage_horaire, id_utilisateur)
    VALUE ('$id_plage_horaire', '$id_utilisateur');

--delete plageHoraire by stationnement_id
DELETE FROM Inoccupable WHERE id_plage_horaire = '$id_plage_horaire';
DELETE FROM Reservation WHERE id_plage_horaire = '$id_plage_horaire';
DELETE FROM Plage_horaire WHERE id_plage_horaire = '$id_plage_horaire';
DELETE FROM possede WHERE id_stationnement = '$id_stationnement' AND id_plage_horaire = '$id_plage_horaire';

--get user by id and cote from Locateur
SELECT * FROM (SELECT id_utilisateur, courriel, nom, prenom FROM Utilisateur WHERE id_utilisateur = '$id_utilisateur') AS infos
INNER JOIN (SELECT IF ('$id_utilisateur' IN (SELECT id_utilisateur FROM Locateur),
    (SELECT cote FROM Locateur WHERE id_utilisateur = '$id_utilisateur'), NULL)) AS cote;

--delete user by id
DELETE FROM Utilisateur WHERE id_utilisateur = '$id_utilisateur';

--get parking by user id
SELECT * FROM stationnement WHERE id_stationnement IN
                                  (SELECT id_stationnement FROM gerer WHERE id_utilisateur = '$id_utilisateur');

--get vehicule by user id
SELECT * FROM vehicule WHERE plaque IN (SELECT plaque FROM Appartient WHERE id_utilisateur = '$id_utilisateur');

--post vehicule by user id
INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur)
    VALUE ('$plaque', '$modele', '$couleur', $longueur, $largeur, $hauteur);
INSERT INTO Appartient (plaque, id_utilisateur) VALUE ('$plaque', '$id_utilisateur');
INSERT INTO Locataire (id_utilisateur) VALUE ('$id_utilisateur') ON DUPLICATE KEY UPDATE id_utilisateur = id_utilisateur;

--put vehicule by plaque
UPDATE vehicule SET modele = '$modele', couleur = '$couleur', longueur = $longueur, largeur = $largeur, hauteur = $hauteur
    WHERE plaque = '$plaque';

--delete vehicule by plaque
DELETE FROM vehicule WHERE plaque = '$plaque';
DELETE FROM Appartient WHERE plaque = '$plaque';

--post Evalue id_utilisateur_locateur by id_utilisateur_locataire
INSERT INTO Evalue (id_utilisateur_locateur, id_utilisateur_locataire, cote)
    VALUE ('$id_utilisateur_locateur', '$id_utilisateur_locataire', '$cote');
