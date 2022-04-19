export class API {
  constructor() {
    this.url = "http://127.0.0.1:5000/";
    this.response = "";
  }
  
    async getAPIDataSecure(query, HTTPOptions) {
      try {
          let JSONresponse = await fetch(this.url + query, HTTPOptions);
          this.response = await JSONresponse.json();
      } catch (error) {
          console.error(error);
          this.response = "error";
      }
    }

  async getTokenInfo(token) {
    let HTTPOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      
    };
    HTTPOptions.headers.Authorization = `Bearer ${token}`;

    let URL = "tokenInfo";

    await this.getAPIDataSecure(URL, HTTPOptions);
    console.log(this.response);
  }

  async getParkingList() {
      let HTTPOptions = {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          method: "GET",
      };
      let URL = "parkingList";
      await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async getFilteredParkingList(filtersString) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "parkingList?" + filtersString;
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async getUserParkingList(id) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "user/" + id + "/parkingList";
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async getUserCars(id) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "user/" + id + "/cars";
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  
  async getParkingById(id) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "parking/" + id;
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async getUserById(id) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "user/" + id;
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async getPlagesHorairesReservation(id) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "parking/" + id + "/plageHoraires/reservation";
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async getPlagesHorairesInoccupable(id) {
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "GET",
    };
    let URL = "parking/" + id + "/plageHoraires/inoccupable";
    await this.getAPIDataSecure(URL, HTTPOptions);
  }
  async postParking(id_utilisateur, prix, longueur, largeur, hauteur, emplacement, jours_d_avance, date_fin){
    let query = {
      id_utilisateur: `${id_utilisateur}`,
      prix: `${prix}`,
      longueur: `${longueur}`,
      largeur: `${largeur}`,
      hauteur: `${hauteur}`,
      emplacement: `${emplacement}`,
      jours_d_avance: `${jours_d_avance}`,
      date_fin: `${date_fin}`,
    };
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(query),
    };
    let md5 = require("md5");
    let idParking = md5(Math.floor(Math.random() * 999999999));
    let URL = "parking/" + idParking.toString();
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async postReservation(id, id_utilisateur, date_arrivee, date_depart) {
    let query = {
      id_utilisateur: `${id_utilisateur}`,
      date_arrivee: `${date_arrivee}`,
      date_depart: `${date_depart}`,
    };
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(query),
    };
    let md5 = require("md5");
    let idPlage = md5(Math.floor(Math.random() * 999999999));
    let URL = "parking/" + id + "/plageHoraires/"+ idPlage.toString() +"/reserver";
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async postCar(userId, plaque , modele, couleur, longueur, hauteur, largeur) {
    let query = {
      plaque: `${plaque}`,
      modele: `${modele}`,
      couleur: `${couleur}`,
      longueur: `${longueur}`,
      hauteur: `${hauteur}`,
      largeur: `${largeur}`,
    };
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(query),
    };
    let URL = "user/" + userId.toString() + "/cars";
    await this.getAPIDataSecure(URL, HTTPOptions);
  }


  async postSignUp(prenom, nom, courriel, password) {
    let query = { 
      nom: `${nom}`, 
      prenom: `${prenom}`, 
      courriel: `${courriel}`, 
      password: `${password}` 
    };
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(query),
    };
    let URL = "signup";
    await this.getAPIDataSecure(URL, HTTPOptions);
    console.log(this.response);
  }

  async postLogin(courriel, password) {
    let query = { 
      courriel: `${courriel}`, 
      password: `${password}` 
    };
    let HTTPOptions = {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(query),
    };
    let URL = "login";
    await this.getAPIDataSecure(URL, HTTPOptions);
    console.log(this.response);
  }

}  