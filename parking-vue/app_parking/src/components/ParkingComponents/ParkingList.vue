<template>
  <div>
      <div id="ParkingList">
          <ul v-for="parking in ParkingList" v-bind:key="parking.id">
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
        ParkingList: Object,
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