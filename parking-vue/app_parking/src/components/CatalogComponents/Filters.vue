<template>
  <div>
      <div id="Filters">
          <ul v-for="filter in filters" v-bind:key="filter.id">
            <FilterComponent  :filter="filter"/>
          </ul>
      </div>
  </div>
</template>

<script>
import FilterComponent from "./Filter.vue";

export default {
    name : "Filters",
    props: {
        filters: Array,
    },
    components: {
        FilterComponent,
    },
};
</script>

<style scoped>

</style>