<template>
  <div>
    <div id="filters">
        <ul v-for="filter in filters" v-bind:key="filter.name">
        <FilterComponent  :filterName="filter.name"/>
        </ul>
    </div>
  </div>
</template>

<script>
import FilterComponent from "./Filter.vue";

export default {
    name : "Filters",
    data() {
        return {
            filters: [],
            filtersCheked: [],
        }
    },
    components: {
        FilterComponent,
    },
    methods:{
        // filterChange(filterName, value){
            
        // },
    },
    created() {
        this.$root.$refs.filters = this;
        this.filters=[
            {
                name:"prixMin",

            },
            {
                name:"prixMax",
            },
            {
                name:"joursDavance",
            },
            {
                name:"longueur",
            },
            {
                name:"largeur",
            },
            {
                name:"hauteur",
            },
            {
                name:"dateFin",
            },
        ];
    },
};
</script>

<style scoped>
#filters{
    display: flex;
    flex-direction: column;
    margin-top: 10px;
    margin-left:10px;
    padding:10px;
    border-style: solid;
    border-color: rgb(0, 196, 167);
    border-radius: 10px;
}
</style>
