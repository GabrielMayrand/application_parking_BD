<template>
  <div>
    <div class="tabs is-centered">
      <ul>
        <li id="Stationnements" class="is-active" @click="changeTab('Stationnements')"><a>Stationnements</a></li>
        <li id="Voitures" @click="changeTab('Voitures')"><a>Voitures</a></li>
      </ul>
    </div>
    <ParkingTab v-if="currentTab=='Stationnements'"/>
    <CarTab v-if="currentTab=='Voitures'"/>
  </div>
</template>

<script>
import CarTab from "./CarTab.vue";
import ParkingTab from "./ParkingTab.vue"

export default {
    data() {
        return {
            currentTab: "Stationnements",
        };
    },
    components: {
        CarTab,
        ParkingTab,
    },
    methods :{
      changeTab(clickedTab) {
        this.currentTab = clickedTab;
        document.getElementById(clickedTab).className = "is-active";
        if(clickedTab == "Stationnements"){
          document.getElementById("Voitures").className = "";
        }
        else if (clickedTab == "Voitures"){
          document.getElementById("Stationnements").className = "";
        }
      },
    }
};
</script>

<style scoped>

</style>