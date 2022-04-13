 <template>
  <div>
    <ParkingList :ParkingList="this.parkingList"/>
  </div>
</template>

<script>
import ParkingList from "./../ParkingComponents/ParkingList.vue"

export default {
    components: {
        ParkingList,
    },
    methods:{
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