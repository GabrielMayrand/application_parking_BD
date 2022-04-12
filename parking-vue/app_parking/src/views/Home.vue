<template>
  <div>
    <Browsing/>
    <ParkingList :ParkingList="this.parkingList"/>
  </div>
</template>

<script>
import Browsing from "../components/CatalogComponents/Browsing.vue";
import ParkingList from "../components/ParkingComponents/ParkingList.vue"

export default {
    components: {
        Browsing,
        ParkingList,
    },
    data() {
        return {
            parkingList: [],
        }
    },
    methods: {
        getParkingList() {
           this.parkingList = [
                {
                  id: 1,
                  advanceDays: 10,
                  finalDate: "2019-12-12",
                  dimensions:[10,30,40],
                  address: "155 rue de la gare, Québec, QC, Canada",
                  landlordId: 45,
                },
                {
                  id: 2,
                  advanceDays: 10,
                  finalDate: "2019-12-12",
                  dimensions:[10,30,40],
                  address: "155 rue de la gare, Québec, QC, Canada",
                  landlordId: 45,
                },
                {
                  id: 3,
                  advanceDays: 10,
                  finalDate: "2019-12-12",
                  dimensions:[10,30,40],
                  address: "155 rue de la gare, Québec, QC, Canada",
                  landlord: 45,
                }
           ]
        },
    },
    created() {
        this.getParkingList();
    },
};
</script>

<style scoped>

</style>
