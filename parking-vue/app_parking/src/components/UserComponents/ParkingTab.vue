 <template>
  <div>
    <div class="createParkingForm" v-if="isAdmin">
      <div class="part">
        <input type="price" class="input" placeholder="Price" id="price">
        <input type="text" class="input" placeholder="length" id="length">
        <input type="text" class="input" placeholder="width" id="width">
        <input type="text" class="input" placeholder="height" id="height">
      </div>
      <div class="part">
        <input type="text" class="input" placeholder="address" id="address">
        <input type="text" class="input" placeholder="Maximum days" id="daysAdvance">
        <input type="text" class="input" placeholder="Final reservation Date" id="finalReservationDate">
      </div>
      <button class="button is-primary" @click="postParking()">Create Parking</button>
    </div>
    <ParkingList :ParkingList="this.parkingList" v-if="!isFetching"/>
  </div>
</template>

<script>
import ParkingList from "./../ParkingComponents/ParkingList.vue"
import {API} from "../../utility/api.js";
import Cookies from 'js-cookie';
export default {
    components: {
        ParkingList,
    },
    data() {
        return {
          infoWrong: false,
          parkingList: [],
          api: new API(),
          pageId : this.$route.params.id,
          isFetching: true,
          isConnected : false,
          isAdmin : false,
        }
    },
    methods:{
        async getParkingList() {
          await this.api.getUserParkingList(this.pageId);
          this.parkingList = this.api.response;
          this.isFetching = false;
        },
        async postParking() {
          // if(document.getElementById("price").value.isdigit() && document.getElementById("length").value.isdigit() && document.getElementById("width").value.isdigit() && document.getElementById("height").value.isdigit() &&
          // document.getElementById("address").value != "" && document.getElementById("daysAdvance").value.isdigit() && document.getElementById("finalReservationDate").value != ""){
            await this.api.postParking(this.pageId, document.getElementById("price").value, document.getElementById("length").value, document.getElementById("width").value, document.getElementById("height").value, document.getElementById("address").value, document.getElementById("daysAdvance").value, document.getElementById("finalReservationDate").value);
            this.infoWrong = false;
            this.getParkingList();
          // }
          // else{
          //   this.infoWrong = true;
          // }
        },
    },
    async created() {
        this.getParkingList();
        
        if(Cookies.get('token') != '' || Cookies.get('token') != undefined){
          this.isConnected = true;
          await this.api.getTokenInfo(Cookies.get('token'));
          if(this.api.response[0].id_utilisateur == this.pageId){
            this.isAdmin = true;
          }
        }
    },
};
</script>

<style scoped>
.createParkingForm{
  display: flex;
  flex-direction: column;
  margin: 10px;
}
.input {
  padding: 10px;
  margin-bottom: 10px;
}
.part{
  display: flex;
  flex-direction: row;
}
</style>