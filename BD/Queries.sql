--post login
SELECT IF(mot_de_passe = '$mdp',
    JSON_ARRAY(JSON_OBJECT('courriel', courriel, 'nom', nom, 'prenom', prenom, 'token', token, 'id', id_utilisateur)),
    null) from utilisateur where courriel = '$courriel';

--post signup
INSERT INTO utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe)
    VALUE (md5('$nom'), sha1(md5('$nom')), '$courriel', '$nom', '$prenom', '$mdp');
SELECT JSON_ARRAY(JSON_OBJECT('courriel', courriel, 'nom', nom, 'prenom', prenom, 'id', id_utilisateur))
    FROM utilisateur WHERE id_utilisateur = md5('$nom');

--get tokenInfo
SELECT JSON_ARRAY(JSON_OBJECT('courriel', courriel, 'nom', nom, 'prenom', prenom, 'token', token, 'id', id_utilisateur))
    FROM utilisateur WHERE token = '$token';

--get parkingList
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin)) FROM stationnement;

--get parkingList by filters
--price
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin)) FROM stationnement
    WHERE $prix_min <= prix AND $prix_max >= prix;

--dimension
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin)) FROM stationnement
    WHERE longueur >= $longueur AND largeur >= $largeur AND hauteur >= $hauteur;

--jour davance
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin)) FROM stationnement
    WHERE jours_d_avance >= $jours_d_avance;

--date de fin
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin)) FROM stationnement
    WHERE date_fin >= $date;

--get parkingListId
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin)) FROM stationnement
    WHERE id_stationnement = '$id_stationnement';

--post parking
INSERT INTO stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin)
    VALUE ('$id_stationnement', $prix, $longueur, $largeur, $hauteur, '$emplacement',
           $jours_d_avance, '$date_fin');
INSERT INTO gerer (id_stationnement, id_utilisateur) VALUE ('$id_stationnement', '$id_utilisateur');
INSERT INTO Locateur (id_utilisateur, cote) VALUE ('$id_utilisateur', NULL);

--put parking
UPDATE stationnement SET prix = $prix, longueur = $longueur, largeur = $largeur, hauteur = $hauteur,
    emplacement = '$emplacement', jours_d_avance = $jours_d_avance, date_fin = '$date_fin'
    WHERE id_stationnement = '$id_stationnement';

--delete parking
DELETE FROM stationnement WHERE id_stationnement = '$id_stationnement';
DELETE FROM gerer WHERE id_stationnement = '$id_stationnement';
DELETE FROM Possede WHERE id_stationnement = '$id_stationnement';

--get plageHoraire by stationnement_id
SELECT JSON_ARRAY(JSON_OBJECT('id', id_plage_horaire, 'date_arrivee', date_arrivee, 'date_depart', date_depart))
    FROM Plage_horaire WHERE id_plage_horaire IN
                                  (SELECT id_plage_horaire FROM possede WHERE id_stationnement = '$id_stationnement');

--get plageHoraire by stationnement_id and jour
SELECT JSON_ARRAY(JSON_OBJECT('id', id_plage_horaire, 'date_arrivee', date_arrivee, 'date_depart', date_depart))
    FROM Plage_horaire WHERE id_plage_horaire IN
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

--get user by id and cote from Locateur                   ###############################################
SELECT JSON_ARRAY(JSON_OBJECT('email', U.email, 'nom', U.nom, 'prenom', U.prenom, 'id', U.id_utilisateur, 'cote', L.cote)) 
FROM Utilisateur U, Locateur L WHERE U.id_utilisateur = '$id_utilisateur' AND L.id_utilisateur = '$id_utilisateur';

--put user by id
UPDATE utilisateur SET courriel = '$courriel', nom = '$nom', prenom = '$prenom', mot_de_passe = '$mot_de_passe'
    WHERE id_utilisateur = '$id_utilisateur';

--delete user by id
DELETE FROM Utilisateur WHERE id_utilisateur = '$id_utilisateur';

--get parking by user id
SELECT JSON_ARRAY(JSON_OBJECT('id', id_stationnement, 'prix', prix, 'longueur', longueur, 'largeur', largeur, 'hauteur',
    hauteur, 'emplacement', emplacement, 'jours_d_avance', jours_d_avance, 'date_fin', date_fin))
    FROM stationnement WHERE id_stationnement IN
                                  (SELECT id_stationnement FROM gerer WHERE id_utilisateur = '$id_utilisateur');

--get vehicule by user id
SELECT JSON_ARRAY(JSON_OBJECT('plaque', plaque, 'modele', modele, 'couleur', couleur, 'longueur', longueur, 'largeur',
    largeur, 'hauteur', hauteur))
    FROM vehicule WHERE plaque IN (SELECT plaque FROM Appartient WHERE id_utilisateur = '$id_utilisateur');

--post vehicule by user id
INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur)
    VALUE ('$plaque', '$modele', '$couleur', $longueur, $largeur, $hauteur);
INSERT INTO Appartient (plaque, id_utilisateur) VALUE ('$plaque', '$id_utilisateur');
INSERT INTO Locataire (id_utilisateur) VALUE ('$id_utilisateur');

--put vehicule by plaque
UPDATE vehicule SET modele = '$modele', couleur = '$couleur', longueur = $longueur, largeur = $largeur, hauteur = $hauteur
    WHERE plaque = '$plaque';

--delete vehicule by plaque
DELETE FROM vehicule WHERE plaque = '$plaque';
DELETE FROM Appartient WHERE plaque = '$plaque';

--post Evalue id_utilisateur_locateur by id_utilisateur_locataire
INSERT INTO Evalue (id_utilisateur_locateur, id_utilisateur_locataire, cote)
    VALUE ('$id_utilisateur_locateur', '$id_utilisateur_locataire', '$cote');