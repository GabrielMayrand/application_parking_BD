<template>
  <div>
    <div id="filters">
        <div class="filterInputs">
        <div class="titreInput">
            Minimum price
        </div>
        <input class="inputBox" id='prixMin' placeholder="99">
        </div>
        <div class="filterInputs">
        <div class="titreInput">
            Maximum price
        </div>
        <input class="inputBox" id='prixMax' placeholder="99">
        </div>
        <div class="filterInputs">
        <div class="titreInput">
            Days in advance
        </div>
        <input class="inputBox" id='joursDavance' placeholder="99">
        </div>
        <div class="filterInputs">
        <div class="titreInput">
            Length
        </div>
        <input class="inputBox" id='longueur' placeholder="99">
        </div>
        <div class="filterInputs">
        <div class="titreInput">
            Width
        </div>
        <input class="inputBox" id='largeur' placeholder="99">
        </div>
        <div class="filterInputs">
        <div class="titreInput">
            Height
        </div>
        <input class="inputBox" id='hauteur' placeholder="99">
        </div>
        <div class="filterInputs">
        <div class="titreInput">
            Only after this date
        </div>
        <input class="inputBox" id='dateFin' placeholder="22-02-21">
        </div>
        <div class="tag is-danger" v-if="dateFormatOk">
            Wrong date format
        </div>
        <button class="button is-primary" @click="applyFilters()">Apply</button>
    </div>
  </div>
</template>

<script>
//import FilterComponent from "./Filter.vue";

export default {
    name : "Filters",
    data() {
        return {
            filters: String,
            dateFormatOk: false,
        }
    },
    methods:{
        applyFilters(){
            this.filters = '';
            if(document.getElementById('prixMin').value != ''){
                this.filters += 'prixMin=' + document.getElementById('prixMin').value + '&';
            }
            if(document.getElementById('prixMax').value != ''){
                this.filters += 'prixMax=' + document.getElementById('prixMax').value + '&';
            }
            if(document.getElementById('joursDavance').value != ''){
                this.filters+= 'joursDavance=' + document.getElementById('joursDavance').value + '&';
            }
            if(document.getElementById('longueur').value != ''){
                this.filters += 'longueur=' + document.getElementById('longueur').value + '&';
            }
            if(document.getElementById('largeur').value != ''){
                this.filters+= 'largeur=' + document.getElementById('largeur').value + '&';
            }
            if(document.getElementById('hauteur').value != ''){
                this.filters+= 'hauteur=' + document.getElementById('hauteur').value + '&';
            }
            if(document.getElementById('dateFin').value != ''){
                if(document.getElementById('dateFin').value.match(/^\d{2}-\d{2}-\d{2}$/)){
                    this.dateFormatOk = false;
                    this.filters+= 'dateFin=' + document.getElementById('dateFin').value + '&';
                }
                else{
                    this.dateFormatOk = true;
                }
                
            }
            if(this.filters.length > 0){
                this.$root.$refs.Home.getFilteredParkingList(this.filters);
            }
            else{
                this.$root.$refs.Home.getParkingList();
            }
        },
        getCurrentFilters(){
            return this.filters;
        },
    },
    created(){
        this.filters = [];
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
