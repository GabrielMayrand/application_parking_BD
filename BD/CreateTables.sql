DROP DATABASE IF EXISTS application_parking;
CREATE DATABASE application_parking;
use application_parking;



CREATE TABLE Utilisateur (id_utilisateur char(32) PRIMARY KEY, token char(40), courriel char(50) UNIQUE, nom char(50),
        prenom char(50), mot_de_passe char(255));

CREATE TABLE Locateur (id_utilisateur char(32) PRIMARY KEY, cote integer,
    FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur));

CREATE TABLE Locataire (id_utilisateur char(32) PRIMARY KEY,
    FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur));

CREATE TABLE Evalue (id_utilisateur_locateur char(32) NOT NULL REFERENCES Locateur(id_utilisateur),
    id_utilisateur_locataire char(32) REFERENCES Locataire(id_utilisateur), cote integer);

CREATE TABLE Vehicule (plaque char(6) PRIMARY KEY, modele char(50), couleur char(20),
    longueur double, largeur double, hauteur double);

CREATE TABLE Appartient (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    plaque char(6) NOT NULL UNIQUE REFERENCES Vehicule(plaque));

CREATE TABLE Stationnement (id_stationnement char(20) PRIMARY KEY, prix double, longueur double, largeur double,
    hauteur double, emplacement char(50), jours_d_avance integer, date_fin date);

CREATE TABLE Gerer (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    id_stationnement char(20) NOT NULL UNIQUE REFERENCES Stationnement(id_stationnement));

CREATE TABLE Plage_horaire (id_plage_horaire char(20) PRIMARY KEY, date_arrivee datetime(0), date_depart datetime(0));

CREATE TABLE Reservation (id_plage_horaire char(20) PRIMARY KEY,
    FOREIGN KEY(id_plage_horaire) REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Inoccupable (id_plage_horaire char(20) PRIMARY KEY,
    FOREIGN KEY(id_plage_horaire) REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Louer (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    id_plage_horaire char(20) UNIQUE REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Retirer (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    id_plage_horaire char(20) UNIQUE REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Possede (id_plage_horaire char(20) NOT NULL UNIQUE REFERENCES Plage_horaire(id_plage_horaire),
    id_stationnement char(20) REFERENCES Stationnement(id_stationnement));



CREATE INDEX idx_courriel_utilisateur ON Utilisateur(courriel) USING HASH;
CREATE INDEX idx_token_utilisateur ON Utilisateur(token) USING HASH;

CREATE INDEX idx_cote_locateur ON Locateur(cote) USING HASH;

CREATE INDEX idx_dimension_stationnement ON Stationnement (longueur, largeur, hauteur) USING BTREE;
CREATE INDEX idx_emplacement_stationnement ON Stationnement (jours_d_avance) USING BTREE;
CREATE INDEX idx_dateFin_stationnement ON Stationnement (date_fin) USING BTREE;
CREATE INDEX idx_prix_stationnement ON Stationnement (prix) USING BTREE;

CREATE INDEX idx_plageHoraire_dateDebut ON Plage_horaire (date_arrivee) USING BTREE;
CREATE INDEX idx_plageHoraire_dateFin ON Plage_horaire (date_depart) USING BTREE;



DELIMITER //
CREATE TRIGGER `Evalue_locateur` AFTER INSERT ON `Evalue` FOR EACH ROW
BEGIN
    UPDATE Locateur L SET L.cote = (SELECT AVG(E.cote) FROM Evalue E WHERE E.id_utilisateur_locateur = L.id_utilisateur)
        WHERE L.id_utilisateur = NEW.id_utilisateur_locateur;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE select_parkingList
    (IN p_prixMin double, p_prixMax double, p_longueur double, p_largeur double,
    p_hauteur double, p_joursAvance integer, p_dateFin date)
BEGIN
    DROP TABLE IF EXISTS tempStationnement;
    CREATE TEMPORARY TABLE IF NOT EXISTS tempStationnement AS (SELECT * FROM stationnement);
    IF p_prixMin is not NULL and p_prixMax is not NULL THEN
        DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                        (SELECT id_stationnement FROM stationnement WHERE p_prixMin <= prix
                                                                                      AND p_prixMax >= prix);
    END IF ;
    IF p_longueur is not NULL and p_largeur is not NULL and p_hauteur is not NULL THEN
        DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                        (SELECT id_stationnement FROM stationnement WHERE longueur <= p_longueur
                                                                                      AND largeur <= p_largeur
                                                                                      AND hauteur <= p_hauteur);
    END IF ;
    IF p_joursAvance is not NULL THEN
        DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                        (SELECT id_stationnement FROM stationnement WHERE jours_d_avance <= p_joursAvance);
    END IF ;
    IF p_dateFin is not NULL THEN
        DELETE FROM tempStationnement WHERE id_stationnement NOT IN
                                        (SELECT id_stationnement FROM stationnement WHERE date_fin >= p_dateFin);
    END IF ;
    SELECT * FROM tempStationnement;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE select_plageHoraire
    (IN p_debut datetime, p_fin datetime, p_id_stationnement char(20))
BEGIN
    IF p_debut is not NULL and p_fin is not NULL THEN
        SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                          (SELECT id_plage_horaire FROM possede WHERE id_stationnement = p_id_stationnement)
                                      AND p_debut <= date_arrivee AND p_fin >= date_depart;
    ELSEIF p_debut is not NULL and p_fin is NULL THEN
        SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                          (SELECT id_plage_horaire FROM possede WHERE id_stationnement = p_id_stationnement)
                                      AND p_debut <= date_arrivee;
    ELSEIF p_debut is NULL and p_fin is not NULL THEN
        SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                          (SELECT id_plage_horaire FROM possede WHERE id_stationnement = p_id_stationnement)
                                      AND p_fin >= date_depart;
    ELSE
        SELECT * FROM Plage_horaire WHERE id_plage_horaire IN
                                          (SELECT id_plage_horaire FROM possede WHERE id_stationnement = p_id_stationnement);
    END IF ;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_plageHoraire_reserver
    (IN p_debut datetime, p_fin datetime, p_id_stationnement char(20), p_id_plage_horaire char(20), p_id_utilisateur char(32))
BEGIN
    INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart)
        VALUE (p_id_plage_horaire, p_debut, p_fin);
    INSERT INTO possede (id_plage_horaire, id_stationnement)
        VALUE (p_id_plage_horaire, p_id_stationnement);
    INSERT INTO louer (id_plage_horaire, id_utilisateur)
        VALUE (p_id_plage_horaire, p_id_utilisateur);
    INSERT INTO Reservation (id_plage_horaire)
        VALUE (p_id_plage_horaire);
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_plageHoraire_inoccupable
    (IN p_debut datetime, p_fin datetime, p_id_stationnement char(20), p_id_plage_horaire char(20), p_id_utilisateur char(32))
BEGIN
    INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart)
        VALUE (p_id_plage_horaire, p_debut, p_fin);
    INSERT INTO possede (id_plage_horaire, id_stationnement)
        VALUE (p_id_plage_horaire, p_id_stationnement);
    INSERT INTO Retirer (id_plage_horaire, id_utilisateur)
        VALUE (p_id_plage_horaire, p_id_utilisateur);
    INSERT INTO Inoccupable (id_plage_horaire)
        VALUE (p_id_plage_horaire);
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_parking
    (IN p_id_stationnement char(20), p_id_utilisateur char(32), p_prix double, p_longueur double, p_largeur double,
    p_hauteur double, p_emplacement char(20), p_joursDavance integer, p_dateFin date)
BEGIN
    INSERT INTO stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin)
        VALUE (p_id_stationnement, p_prix, p_longueur, p_largeur, p_hauteur, p_emplacement, p_joursDavance, p_dateFin);
    INSERT INTO gerer (id_stationnement, id_utilisateur) VALUE (p_id_stationnement, p_id_utilisateur);
    INSERT INTO Locateur (id_utilisateur, cote) VALUE (p_id_utilisateur, NULL) ON DUPLICATE KEY UPDATE id_utilisateur = id_utilisateur;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_vehicule
    (IN p_plaque char(6), p_modele char(20), p_couleur char(20), p_longueur double,
    p_largeur double, p_hauteur double, p_id_utilisateur char(32))
BEGIN
    INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur)
        VALUE (p_plaque, p_modele, p_couleur, p_longueur, p_largeur, p_hauteur);
    INSERT INTO Appartient (plaque, id_utilisateur) VALUE (p_plaque, p_id_utilisateur);
    INSERT INTO Locataire (id_utilisateur) VALUE (p_id_utilisateur) ON DUPLICATE KEY UPDATE id_utilisateur = id_utilisateur;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_utilisateur
    (IN p_id_utilisateur char(32), p_token char(40))
BEGIN
    DECLARE cur_is_done BOOLEAN DEFAULT FALSE;
    DECLARE cur_id_parking CHAR(20);
    DECLARE cur_id_voiture CHAR(6);
    DECLARE cur_parking CURSOR FOR SELECT id_stationnement FROM Gerer WHERE id_utilisateur = p_id_utilisateur;
    DECLARE cur_voiture CURSOR FOR SELECT plaque FROM Appartient WHERE id_utilisateur = p_id_utilisateur;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur_is_done = TRUE;

    IF (SELECT token FROM Utilisateur WHERE id_utilisateur = p_id_utilisateur) = p_token THEN
        OPEN cur_parking;
        boucle: LOOP
            FETCH cur_parking INTO cur_id_parking;
            IF cur_is_done THEN
                LEAVE boucle;
            END IF;
            call delete_stationnement(cur_id_parking);
        END LOOP boucle;
        CLOSE cur_parking;

        SET cur_is_done = FALSE;

        OPEN cur_voiture;
        boucle: LOOP
            FETCH cur_voiture INTO cur_id_voiture;
            IF cur_is_done THEN
                LEAVE boucle;
            END IF;
            call delete_voiture(cur_id_voiture);
        END LOOP boucle;
        CLOSE cur_voiture;

        DELETE FROM Evalue WHERE id_utilisateur_locataire = p_id_utilisateur or id_utilisateur_locateur = p_id_utilisateur;
        DELETE FROM Locataire WHERE id_utilisateur = p_id_utilisateur;
        DELETE FROM Locateur WHERE id_utilisateur = p_id_utilisateur;
        DELETE FROM Utilisateur WHERE id_utilisateur = p_id_utilisateur;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Token invalide';
    END IF;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_plageHoraire
    (IN p_id_plage_horaire char(20))
BEGIN
    DELETE FROM Inoccupable WHERE id_plage_horaire = p_id_plage_horaire;
    DELETE FROM Reservation WHERE id_plage_horaire = p_id_plage_horaire;
    DELETE FROM louer WHERE id_plage_horaire = p_id_plage_horaire;
    DELETE FROM retirer WHERE id_plage_horaire = p_id_plage_horaire;
    DELETE FROM Plage_horaire WHERE id_plage_horaire = p_id_plage_horaire;
    DELETE FROM possede WHERE id_plage_horaire = p_id_plage_horaire;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_stationnement
    (IN p_id_stationnement char(20))
BEGIN
    DECLARE cur_is_done BOOLEAN DEFAULT FALSE;
    DECLARE cur_id_plage_horaire CHAR(20);
    DECLARE cur CURSOR FOR SELECT id_plage_horaire FROM Possede WHERE id_stationnement = p_id_stationnement;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur_is_done = TRUE;
    OPEN cur;
    DELETE FROM stationnement WHERE id_stationnement = p_id_stationnement;
    DELETE FROM gerer WHERE id_stationnement = p_id_stationnement;
    boucle: LOOP
        FETCH cur INTO cur_id_plage_horaire;
        IF cur_is_done THEN
            LEAVE boucle;
        END IF;
        call delete_plageHoraire (cur_id_plage_horaire);
   END LOOP boucle;
   CLOSE cur;
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_voiture
    (IN p_voiture_id char(6))
BEGIN
    DELETE FROM vehicule WHERE plaque = p_voiture_id;
    DELETE FROM Appartient WHERE plaque = p_voiture_id;
END
//
DELIMITER ;



set @id1 = md5('joe.blo@mail.com');
set @id2 = md5('john.cena@mail.com');
set @id3 = md5('test@mail.com');
set @id4 = md5('monsieurNet@mail.com');

INSERT INTO Utilisateur (id_utilisateur, token, courriel, nom, prenom, mot_de_passe)
    VALUES  (@id1, sha1(@id1), 'joe.blo@mail.com', 'Blo', 'Joe', ''),
            (@id2, sha1(@id2), 'john.cena@mail.com', 'Cena', 'John', ''),
            (@id3, sha1(@id3), 'test@mail.com', 'Test', 'Monsieur', ''),
            (@id4, sha1(@id4), 'monsieurNet@mail.com', 'Net', 'Monsieur', '');

INSERT INTO Locateur (id_utilisateur, cote) VALUES (@id1, NULL), (@id2, NULL), (@id3, NULL);

INSERT INTO Locataire (id_utilisateur) VALUES (@id3), (@id4);

INSERT INTO Evalue (id_utilisateur_locateur, id_utilisateur_locataire, cote) VALUES (@id1, @id4, 5), (@id1, @id3, 3);

INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur)
    VALUES ('K99QQX', 'Toyota', 'Noir', 4.575, 1.760, 1.471),
           ('E60BON', 'Civic', 'Bleu', 4.250, 1.760, 1.460),
           ('B74BLA', 'Accent', 'Bleu', 4.186, 1.730, 1.450);

INSERT INTO Appartient (id_utilisateur, plaque) VALUES (1, 'K99QQX'), (3, 'E60BON'), (4, 'B74BLA');

INSERT INTO Stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin)
    VALUES (1, 45, 6, 3, 5, '783 avenue Myrand', 2, '22-06-01'),
           (2, 20, 6, 3, 5, '775 avenue Myrand', 30, '23-01-01'),
           (3, 400, 6, 3, 40, '766 avenue Myrand', 10, '26-08-08');

INSERT INTO Gerer (id_utilisateur, id_stationnement) VALUES (@id1, 1), (@id2, 2), (@id3, 3);

INSERT INTO Plage_horaire (id_plage_horaire, date_arrivee, date_depart)
    VALUES (1, '2022-2-20 9:45:00', '2022-2-20 10:00:00'),
           (2, '2022-2-22 10:00:00', '2022-2-22 10:15:00'),
           (3, '2022-2-28 9:00:00', '2022-2-28 9:15:00'),
           (4, '2022-3-14 10:45:00', '2022-3-14 11:00:00'),
           (5, '2022-3-15 15:30:00', '2022-3-15 15:45:00'),
           (6, '2022-3-16 23:00:00', '2022-3-16 23:15:00');

INSERT INTO Reservation (id_plage_horaire) VALUES (2), (3), (4), (5), (6);

INSERT INTO Inoccupable (id_plage_horaire) VALUES (1);

INSERT INTO louer (id_utilisateur, id_plage_horaire) VALUES (@id3, 2), (@id3, 3), (@id4, 4), (@id4, 5), (@id3, 6);

INSERT INTO Retirer (id_utilisateur, id_plage_horaire) VALUES (@id2, 1);

INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUES (1, 3), (2, 3), (3, 1), (4, 2), (5, 1), (6, 2);
