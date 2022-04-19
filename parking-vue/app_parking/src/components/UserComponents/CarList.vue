<template>
  <div>
      <div id="CarList">
          <ul class="card is-primary carCard" v-for="carCard in CarList" v-bind:key="carCard.id">
            <CarCard id="CarCard" :carCard="carCard"/>
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
    #CarList{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    .carCard{
        flex-wrap: wrap;
        padding: 10px;
        margin: 10px;
    }

</style>