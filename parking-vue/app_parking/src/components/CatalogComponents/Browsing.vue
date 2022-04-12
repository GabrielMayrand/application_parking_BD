<template>
  <div>
    <SearchBar/>
    <Filters/>
  </div>
</template>

<script>
import Filters from "./Filters.vue";
import SearchBar from "./SearchBar.vue";

export default {
    components: {
        Filters,
        SearchBar,
    },
};
</script>

<style scoped>

</style>