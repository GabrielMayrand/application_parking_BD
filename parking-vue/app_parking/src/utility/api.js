export class API {
    constructor() {
      this.url = "http://127.0.0.1:5000/";
      this.response = "";
    }
    
      async getAPIDataSecure(query, HTTPOptions) {
        try {
            console.log( query+HTTPOptions);
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
                'Access-Control-Allow-Origin': 'origin-list',
                'Access-Control-Allow-Methods': 'GET',
            },
            method: "GET",
            'Content-Type': 'application/json'
        };
        let URL = "parkingList";
        console.log(this.url + URL, HTTPOptions);
        await this.getAPIDataSecure(URL, HTTPOptions);
    }
}  