<template>
  <div>
    <Browsing/>
    <ParkingList/>
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
};
</script>

<style scoped>

</style>
