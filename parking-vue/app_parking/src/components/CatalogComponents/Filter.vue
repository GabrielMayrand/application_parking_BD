<template>
    <div class="filterInputs">
        <div class="titreInput">
            <input class="checkbox" type="checkbox" id='filterChecked' >
            {{filter.name}}
        </div>
        <input class="inputBox" :id='filter.name'>
    </div>
</template>

<script>
export default {
    props:{
        filter: Object,
    },
    methods: {
        // applyFilter() {
        //     this.$refs.filters.filterChange(this.filterName, document.getElementById('filterName').value, document.getElementById('filterCheked').value);
        //     console.log(document.getElementById('filterChecked'));
        // },
    },
}
</script>

<style scoped>
    .filterInputs{
        display: flex;
        flex-direction: row;
        align-items: center;
        padding:2px 0px;
    }
    .inputBox{
        width:6rem;
        height:1.5rem;
    }
    .checkbox{
        margin-right:5px; 
    }
    .titreInput{
        width:150px;
        text-align: left;
    }
</style>