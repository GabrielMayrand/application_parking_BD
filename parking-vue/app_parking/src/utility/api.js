export class API {
    constructor() {
      this.url = "https://127.0.0.1:5000/";
      this.response = "";
    }
    
      async getAPIDataSecure(query, HTTPOptions) {
        try {
          let JSONresponse = await fetch(this.url + query, HTTPOptions);
          this.response = await JSONresponse.json();
        } catch (error) {
          console.log(error);
          this.response = "error";
        }
      }

    async getParkingList() {
        let HTTPOptions = {
            headers: {},
            method: "GET",
            'Content-Type': 'application/json'
        };
        let URL = "parkingList";
        await this.getAPIDataSecure(URL, HTTPOptions);
    }
}  