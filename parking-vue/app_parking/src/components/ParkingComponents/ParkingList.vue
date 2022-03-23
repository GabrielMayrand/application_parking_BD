<template>
  <div>
      <div id="ParkingList">
          <ul v-for="parkingCard in ParkingList" v-bind:key="parkingCard.id">
            <ParkingCard id="parkingCard" :parkingCard="parkingCard"/>
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

</style>