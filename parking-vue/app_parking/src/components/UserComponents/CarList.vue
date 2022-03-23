<template>
  <div>
      <div id="CarList">
          <ul v-for="CarCard in CarList" v-bind:key="CarCard.id">
            <CarCard id="CarCard" :CarCard="CarCard"/>
          </ul>
      </div>
  </div>
</template>

<script>
import CarCard from "./CarCard.vue";

export default {
    name : "CarList",
    props: {
        CarList: Array,
    },
    components: {
        CarCard,
    },
};
</script>

<style scoped>

</style>