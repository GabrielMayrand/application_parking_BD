<template>
  <div>
      <div id="Filters">
          <ul v-for="filter in filters" v-bind:key="filter.id">
            <Filter id="filter" :filter="filter"/>
          </ul>
      </div>
  </div>
</template>

<script>
import Filter from "./Filter.vue";

export default {
    name : "Filters",
    props: {
        filters: Array,
    },
    components: {
        Filter,
    },
};
</script>

<style scoped>

</style>