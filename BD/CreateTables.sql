CREATE DATABASE application_parking;
use application_parking;



CREATE TABLE Utilisateur (id_utilisateur char(20) PRIMARY KEY, courriel char(50), nom char(50),
    prenom char(50), mot_de_passe char(250));

CREATE TABLE Locateur (id_utilisateur char(20) PRIMARY KEY, cote integer,
    FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE);

CREATE TABLE Locataire (id_utilisateur char(20) PRIMARY KEY,
    FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE);

CREATE TABLE Evalue (id_utilisateur_locateur char(20) NOT NULL REFERENCES Locateur(id_utilisateur) ON DELETE CASCADE,
    id_utilisateur_locataire char(20) REFERENCES Locataire(id_utilisateur) ON DELETE CASCADE, cote integer);

CREATE TABLE Vehicule (plaque char(6) PRIMARY KEY, modele char(50), couleur char(20),
    longueur double, largeur double, hauteur double);

CREATE TABLE Appartient (id_utilisateur char(20) NOT NULL REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE,
    plaque char(6) NOT NULL REFERENCES Vehicule(plaque) ON DELETE CASCADE);

CREATE TABLE Stationnement (id_stationnement char(20) PRIMARY KEY, prix double, longueur double, largeur double,
    hauteur double, emplacement char(50), jours_d_avance integer, date_fin date);

CREATE TABLE Gerer (id_utilisateur char(20) NOT NULL REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_stationnement char(20) NOT NULL REFERENCES Stationnement(id_stationnement) ON DELETE CASCADE);

CREATE TABLE Plage_horaire (id_plage_horaire char(20) PRIMARY KEY, annee year, mois integer, jour integer,
    heure_arrivee time(0), heure_depart time(0));

CREATE TABLE Reservation (id_plage_horaire char(20) PRIMARY KEY,
    FOREIGN KEY(id_plage_horaire) REFERENCES Plage_horaire(id_plage_horaire) ON DELETE CASCADE);

CREATE TABLE Inoccupable (id_plage_horaire char(20) PRIMARY KEY,
    FOREIGN KEY(id_plage_horaire) REFERENCES Plage_horaire(id_plage_horaire) ON DELETE CASCADE);

CREATE TABLE Louer (id_utilisateur char(20) NOT NULL REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_plage_horaire char(20) REFERENCES Plage_horaire(id_plage_horaire) ON DELETE CASCADE);

CREATE TABLE Retirer (id_utilisateur char(20) NOT NULL REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_plage_horaire char(20) REFERENCES Plage_horaire(id_plage_horaire) ON DELETE CASCADE);

CREATE TABLE Possede (id_plage_horaire char(20) NOT NULL REFERENCES Plage_horaire(id_plage_horaire) ON DELETE CASCADE,
    id_stationnement char(20) REFERENCES Stationnement(id_stationnement) ON DELETE CASCADE);



INSERT INTO Utilisateur (id_utilisateur, courriel, nom, prenom, mot_de_passe)
    VALUES  (1, 'joe.blo@mail.com', 'Blo', 'Joe', 'a'),
            (2, 'john.cena@mail.com', 'Cena', 'John', 'b'),
            (3, 'test@mail.com', 'Test', 'Monsieur', 'c'),
            (4, 'monsieurNet@mail.com', 'Net', 'Monsieur', 'd');

INSERT INTO Locateur (id_utilisateur, cote) VALUES (1, NULL), (2, NULL), (3, NULL);

INSERT INTO Locataire (id_utilisateur) VALUES (3), (4);

INSERT INTO Evalue (id_utilisateur_locateur, id_utilisateur_locataire, cote) VALUES (1, 4, 5);
UPDATE Locateur L SET L.cote = (SELECT AVG(E.cote) FROM Evalue E WHERE E.id_utilisateur_locateur = L.id_utilisateur)
    WHERE L.id_utilisateur = 1;

INSERT INTO Evalue (id_utilisateur_locateur, id_utilisateur_locataire, cote) VALUES (1, 3, 3);
UPDATE Locateur L SET L.cote = (SELECT AVG(E.cote) FROM Evalue E WHERE E.id_utilisateur_locateur = L.id_utilisateur)
    WHERE L.id_utilisateur = 1;

INSERT INTO Vehicule (plaque, modele, couleur, longueur, largeur, hauteur)
    VALUES ('K99QQX', 'Toyota', 'Noir', 4.575, 1.760, 1.471),
           ('E60BON', 'Civic', 'Bleu', 4.250, 1.760, 1.460),
           ('B74BLA', 'Accent', 'Bleu', 4.186, 1.730, 1.450);

INSERT INTO Appartient (id_utilisateur, plaque) VALUES (1, 'K99QQX'), (3, 'E60BON'), (4, 'B74BLA');

INSERT INTO Stationnement (id_stationnement, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin)
    VALUES (1, 45, 6, 3, 5, '783 avenue Myrand', 2, '22-06-01'),
           (2, 20, 6, 3, 5, '775 avenue Myrand', 30, '23-01-01'),
           (3, 400, 6, 3, 40, '766 avenue Myrand', 10, '26-08-08');

INSERT INTO Gerer (id_utilisateur, id_stationnement) VALUES (1, 1), (2, 2), (3, 3);

INSERT INTO Plage_horaire (id_plage_horaire, annee, mois, jour, heure_arrivee, heure_depart)
    VALUES (1, 2007, 8, 14, '9:00:00', '10:00:00'),
           (2, 2010, 8, 15, '17:00:00', '17:00:00'),
           (3, 2021, 5, 24, '9:30:00', '10:00:00'),
           (4, 2006, 3, 26, '12:00:00', '13:00:00'),
           (5, 2003, 9, 30, '2:30:00', '3:45:00'),
           (6, 2004, 11, 21, '20:15:00', '21:00:00');

INSERT INTO Reservation (id_plage_horaire) VALUES (2), (3), (4), (5), (6);

INSERT INTO Inoccupable (id_plage_horaire) VALUES (1);

INSERT INTO LOUER (id_utilisateur, id_plage_horaire) VALUES (3, 2), (3, 3), (4, 4), (4, 5), (3, 6);

INSERT INTO Retirer (id_utilisateur, id_plage_horaire) VALUES (2, 1);

INSERT INTO Possede (id_plage_horaire, id_stationnement) VALUES (1, 3), (2, 3), (3, 1), (4, 2), (5, 1), (6, 2);