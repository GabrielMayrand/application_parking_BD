<template>
  <div>
    <div id="filters">
        <ul v-for="filter in filters" v-bind:key="filter.name">
        <FilterComponent  :filter="filter"/>
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
                checked:false,
                value:0,
            },
            {
                name:"prixMax",
                checked:false,
                value:0,
            },
            {
                name:"joursDavance",
                checked:false,
                value:0,
            },
            {
                name:"longueur",
                checked:false,
                value:0,
            },
            {
                name:"largeur",
                checked:false,
                value:0,
            },
            {
                name:"hauteur",
                checked:false,
                value:0,
            },
            {
                name:"dateFin",
                checked:false,
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
    padding:10px;
    border-style: solid;
    border-color: rgb(0, 196, 167);
    border-radius: 10px;
}
</style>
