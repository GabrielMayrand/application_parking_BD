<template>
  <div>
    <ParkingTab/>
    <CarTab/>
  </div>
</template>

<script>
import CarTab from "./CarTab.vue";
import ParkingTab from "./ParkingTab.vue"

export default {
    components: {
        CarTab,
        ParkingTab,
    },
};
</script>

<style scoped>

</style>