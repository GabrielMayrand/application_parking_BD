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

  async postReservation(id, date_arrivee, date_depart) {
    let query = {
      id_parking: `${id}`,
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
    let URL = "parking/" + id + "/plageHoraires/"+ "400" +"/reserver";
    console.log(HTTPOptions);
    await this.getAPIDataSecure(URL, HTTPOptions);
  }

  async postSignUp(prenom, nom, courriel, password) {
    let query = { nom: `${nom}`, prenom: `${prenom}`, courriel: `${courriel}`, password: `${password}` };
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
}  