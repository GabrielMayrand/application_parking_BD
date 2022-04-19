<template>
  <div>
    <div id="filters">
        <ul v-for="filter in filters" v-bind:key="filter.name">
        <FilterComponent  :filter="filter"/>
        </ul>
        <button class="button is-primary">Apply</button>
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
                value:0,
            },
            {
                name:"prixMax",
                value:0,
            },
            {
                name:"joursDavance",
                value:0,
            },
            {
                name:"longueur",
                value:0,
            },
            {
                name:"largeur",
                value:0,
            },
            {
                name:"hauteur",
                value:0,
            },
            {
                name:"dateFin",
                value:0,
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
    margin-top: 10px;
    padding:10px;
    border-style: solid;
    border-color: rgb(0, 196, 167);
    border-radius: 10px;
}
</style>
