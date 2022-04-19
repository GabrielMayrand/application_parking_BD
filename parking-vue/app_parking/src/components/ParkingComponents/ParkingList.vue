<template>
  <div>
      <div id="ParkingList">
          <ul v-for="parking in ParkingList" v-bind:key="parking.id_stationnement">
            <ParkingCard id="parkingCard" :parking="parking"/>
          </ul>
      </div>
  </div>
</template>

<script>
import ParkingCard from "./ParkingCard.vue";

export default {
    name : "ParkingList",
    props: {
        ParkingList: Array,
    },
    components: {
        ParkingCard,
    },
};
</script>

<style scoped>
#parkingList{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}
</style>