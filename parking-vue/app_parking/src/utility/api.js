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
    console.log(this.url + URL);
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

  

  async 
}  