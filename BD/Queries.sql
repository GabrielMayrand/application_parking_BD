#post login
SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE courriel = '$courriel';

#post signup
INSERT INTO utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe)
    VALUE (md5('$courriel'), sha1(md5('$courriel')), '$courriel', '$nom', '$prenom', '$mdp');
SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE id_utilisateur = md5('$courriel');

#get tokenInfo
SELECT courriel, nom, prenom, token, id_utilisateur FROM utilisateur WHERE token = '$token';

#get parkingList
call select_parkingList('$prixMin', '$prixMax', '$longueur', '$largeur', '$hauteur');

#get parkingListId
SELECT * FROM stationnement WHERE id_stationnement = '$id_stationnement';

#post parking
call insert_parking('$id_stationnement', '$id_utilisateur', '$prix', '$longueur', '$largeur', '$hauteur', '$emplacment', '$joursDavance', '$dateFin');

#put parking
UPDATE stationnement SET prix = '$prix', longueur = '$longueur', largeur = '$largeur', hauteur = '$hauteur',
    emplacement = '$emplacement', jours_d_avance = '$jours_d_avance', date_fin = '$date_fin'
    WHERE id_stationnement = '$id_stationnement';

#delete parking
call delete_stationnement('$id_stationnement');

#get plageHoraire by stationnement_id
call select_plageHoraire('$date_debut', '$date_fin', '$id_stationnement');

#post Reservation plageHoraire by stationnement_id
call insert_plageHoraire_reserver('$date_debut', '$date_fin', '$id_stationnement', '$id_plage_horaire', '$id_utilisateur');

#post Inoccupable plageHoraire by stationnement_id
call insert_plageHoraire_inoccupable('$date_debut', '$date_fin', '$id_stationnement', '$id_plage_horaire', '$id_utilisateur');

#delete plageHoraire by stationnement_id
call delete_plageHoraire ((SELECT id_plage_horaire FROM Possede WHERE id_plage_horaire = '$id_plage_horaire' AND id_stationnement = '$id_stationnement'));

#get user by id and cote from Locateur
SELECT * FROM (SELECT id_utilisateur, courriel, nom, prenom FROM Utilisateur WHERE id_utilisateur = '$id_utilisateur') AS infos
INNER JOIN (SELECT IF ('$id_utilisateur' IN (SELECT id_utilisateur FROM Locateur),
    (SELECT cote FROM Locateur WHERE id_utilisateur = '$id_utilisateur'), NULL)) AS cote;

#delete user by id
call delete_utilisateur('$id_utilisateur');

#get parking by user id
SELECT * FROM stationnement WHERE id_stationnement IN
                                  (SELECT id_stationnement FROM gerer WHERE id_utilisateur = '$id_utilisateur');

#get vehicule by user id
SELECT * FROM vehicule WHERE plaque IN (SELECT plaque FROM Appartient WHERE id_utilisateur = '$id_utilisateur');

#post vehicule by user id
call insert_vehicule('$plaque', '$modele', '$couleur', '$longueur', '$largeur', '$hauteur', '$id_utilisateur');

#put vehicule by plaque
UPDATE vehicule SET modele = '$modele', couleur = '$couleur', longueur = '$longueur', largeur = '$largeur', hauteur = '$hauteur'
    WHERE plaque = '$plaque';

#delete vehicule by plaque
call delete_voiture('$plaque');

#post Evalue id_utilisateur_locateur by id_utilisateur_locataire
INSERT INTO Evalue (id_utilisateur_locateur, id_utilisateur_locataire, cote)
    VALUE ('$id_utilisateur_locateur', '$id_utilisateur_locataire', '$cote');
