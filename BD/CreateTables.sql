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
    plaque char(6) NOT NULL REFERENCES Vehicule(plaque));

CREATE TABLE Stationnement (id_stationnement char(20) PRIMARY KEY, prix double, longueur double, largeur double,
    hauteur double, emplacement char(50), jours_d_avance integer, date_fin date);

CREATE TABLE Gerer (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    id_stationnement char(20) NOT NULL REFERENCES Stationnement(id_stationnement));

CREATE TABLE Plage_horaire (id_plage_horaire char(20) PRIMARY KEY, date_arrivee datetime(0), date_depart datetime(0));

CREATE TABLE Reservation (id_plage_horaire char(20) PRIMARY KEY,
    FOREIGN KEY(id_plage_horaire) REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Inoccupable (id_plage_horaire char(20) PRIMARY KEY,
    FOREIGN KEY(id_plage_horaire) REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Louer (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    id_plage_horaire char(20) REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Retirer (id_utilisateur char(32) NOT NULL REFERENCES Utilisateur(id_utilisateur),
    id_plage_horaire char(20) REFERENCES Plage_horaire(id_plage_horaire));

CREATE TABLE Possede (id_plage_horaire char(20) NOT NULL REFERENCES Plage_horaire(id_plage_horaire),
    id_stationnement char(20) REFERENCES Stationnement(id_stationnement));



DELIMITER //
CREATE TRIGGER `Evalue_locateur` AFTER INSERT ON `Evalue` FOR EACH ROW
BEGIN
    UPDATE Locateur L SET L.cote = (SELECT AVG(E.cote) FROM Evalue E WHERE E.id_utilisateur_locateur = L.id_utilisateur)
        WHERE L.id_utilisateur = NEW.id_utilisateur_locateur;
END
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER `Delete_utilisateur` BEFORE DELETE ON `Utilisateur` FOR EACH ROW
BEGIN
    DECLARE id_utilisateur_to_delete CHAR(32);
    SET id_utilisateur_to_delete = OLD.id_utilisateur;

    IF (SELECT token FROM Utilisateur WHERE id_utilisateur = id_utilisateur_to_delete) = OLD.token THEN
        DELETE FROM Inoccupable WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM Retirer WHERE id_utilisateur = id_utilisateur_to_delete);
        DELETE FROM Reservation WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM Louer WHERE id_utilisateur = id_utilisateur_to_delete);
        DELETE FROM Plage_horaire WHERE id_plage_horaire IN (SELECT id_plage_horaire FROM possede WHERE id_stationnement IN (SELECT id_stationnement FROM Gerer WHERE id_utilisateur = id_utilisateur_to_delete))
                                        OR id_plage_horaire NOT IN (SELECT id_plage_horaire FROM Louer)
                                        OR id_plage_horaire NOT IN (SELECT id_plage_horaire FROM Retirer);
        DELETE FROM Retirer WHERE id_utilisateur = id_utilisateur_to_delete;
        DELETE FROM Louer WHERE id_utilisateur = id_utilisateur_to_delete;
        DELETE FROM Stationnement WHERE id_stationnement IN (SELECT id_stationnement FROM Gerer WHERE id_utilisateur = id_utilisateur_to_delete);
        DELETE FROM Gerer WHERE id_utilisateur = id_utilisateur_to_delete;
        DELETE FROM Possede WHERE id_stationnement NOT IN (SELECT id_stationnement FROM Stationnement)
                                OR id_plage_horaire NOT IN (SELECT id_plage_horaire FROM Plage_horaire);
        DELETE FROM Vehicule WHERE plaque IN (SELECT plaque FROM Appartient WHERE id_utilisateur = id_utilisateur_to_delete);
        DELETE FROM Appartient WHERE id_utilisateur = id_utilisateur_to_delete;
        DELETE FROM Evalue WHERE id_utilisateur_locataire = id_utilisateur_to_delete or id_utilisateur_locateur = id_utilisateur_to_delete;
        DELETE FROM Locataire WHERE id_utilisateur = id_utilisateur_to_delete;
        DELETE FROM Locateur WHERE id_utilisateur = id_utilisateur_to_delete;
    END IF;
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
    VALUES (1, '2022-2-20 9:00:00', '2022-2-20 10:00:00'),
           (2, '2022-2-22 9:00:00', '2022-2-23 10:15:00'),
           (3, '2022-2-28 9:00:00', '2022-3-1 10:00:00'),
           (4, '2022-3-14 9:00:00', '2022-3-14 10:00:00'),
           (5, '2022-3-15 15:00:00', '2022-3-15 20:45:00'),
           (6, '2022-3-16 12:00:00', '2022-3-17 17:30:00');

INSERT INTO Reservation (id_plage_horaire) VALUES (2), (3), (4), (5), (6);

INSERT INTO Inoccupable (id_plage_horaire) VALUES (1);

INSERT INTO louer (id_utilisateur, id_plage_horaire) VALUES (@id3, 2), (@id3, 3), (@id4, 4), (@id4, 5), (@id3, 6);

INSERT INTO Retirer (id_utilisateur, id_plage_horaire) VALUES (@id2, 1);

INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUES (1, 3), (2, 3), (3, 1), (4, 2), (5, 1), (6, 2);
