<template>
  <div>
    <Browsing/>
    <ParkingList :ParkingList="this.parkingList"/>
  </div>
</template>

<script>
import Browsing from "../components/CatalogComponents/Browsing.vue";
import ParkingList from "../components/ParkingComponents/ParkingList.vue"
import {API} from "../utility/api.js";

export default {
    components: {
        Browsing,
        ParkingList,
    },
    data() {
        return {
          parkingList: [],
          api: new API(),
        }
    },
    methods: {
      async getParkingList() {
        await this.api.getParkingList();
        this.parkingList = this.api.response;
      },
    },
    created() {
        this.getParkingList();
    },
};
</script>

<style scoped>

</style>
