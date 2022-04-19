<template>
  <div id="navHome">
    <input class="input " type="text" id="SearchBar" placeholder="Search an address">
    <button class="button is-primary " id="SearchButton">Search</button>
    <button class="button is-primary " id="Filters" @click="filterToggleClicked">Filters</button>
    <Filters v-if="filterToggle"/>
  </div>
</template>

<script>
import Filters from "./Filters.vue";

export default {
  data () {
    return {
      filterToggle : false,
    }
  },
  components: {
      Filters,
  },
  methods: {
      filterToggleClicked(){
          this.filterToggle = !this.filterToggle;
      },
  },
};
</script>

<style scoped>
#navHome{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    margin: 10px;
    padding: 10px;
}
#SearchBar {
    margin: 10px;
    padding: 10px;
    max-width: 300px;
}
#wrapper {
    display: flex;
    flex-direction: row;
}
.button {
    margin: 10px;
    padding: 10px;
}
</style>