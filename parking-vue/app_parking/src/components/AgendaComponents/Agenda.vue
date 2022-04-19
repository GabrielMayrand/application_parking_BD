<template>
 <div>
     <!-- Si c'est un utilisateur -->
     <div id="createPlageForm">
         <button class="button is-primary formElements" @click="createReservation()">Create reservation</button>
         <div>Starting date :</div>
         <input type="text" class="input formElements" placeholder="2022-04-19" id="date_arrivee">
         <input type="text" class="input formElements" placeholder="13:00" id="heure_arrivee"> 
         <div>Finishing date :</div>
         <input type="text" class="input formElements" placeholder="2022-04-19" id="date_depart">
         <input type="text" class="input formElements" placeholder="13:00" id="heure_depart">        
     </div>

     <div class="tag is-danger" v-if="!formatOk">
         Invalid Format
     </div>

    <div class="card">
        Today : {{today}}
    </div>
    <div id="plagesDivision">
        <div>
            <div class="title">Reserved</div>
            <ul v-for="plage in plagesHorairesReservation" v-bind:key="plage.id_plage_horaires">
            <div class="reserve card">
                <Plage :plage="plage"/>
            </div>
            </ul>
        </div>
        <div>
            <div class="title">Disabled</div>
            <ul v-for="plage in plagesHorairesInoccupable" v-bind:key="plage.id_plage_horaires">
            <div class="inoccupable card">
                <Plage :plage="plage"/>
            </div>
            </ul>
        </div>
    </div>
    <div class="card">
        Final reservation Date : {{finalDate}}
    </div>
    </div>
</template>

<script>
import {API} from "../../utility/api.js";
import Plage from "./Plage.vue";
export default {
    data() {
        return {
            api : new API(),
            pageId : this.$route.params.id,
            today: new Date(),
            formatOk: true,
        }
    },
    components: {
        Plage,
    },
    props: {
        plagesHorairesReservation: Array,
        plagesHorairesInoccupable: Array,
        finalDate: String,
    },
    methods: {
        async createReservation() {
            console.log("pageId : " + this.pageId);
            //if(document.getElementById("date_depart").value.match(/^\d{4}-\d{2}-\d{2}$/) && document.getElementById("date_depart").value.match(/^\d{4}-\d{2}-\d{2}$/) && document.getElementById("heure_arrivee").value.match(/^\d{2}:\d{2}$/) && document.getElementById("heure_depart").value.match(/^\d{2}:\d{2}$/)) {
                await this.api.postReservation(this.pageId, this.pageId, 
                `${document.getElementById("date_arrivee").value} ${document.getElementById("heure_arrivee").value}:00`, 
                `${document.getElementById("date_depart").value} ${document.getElementById("heure_depart").value}:00`);
            // }
            // else {
            //     this.formatOk = false;
            // }
        },
    },
    created() {
        this.pageId = this.$route.params.id;
        this.plagesHorairesReservation.forEach(plage => {
            plage.type = "reserve";
        });
        this.plagesHorairesReservation.sort((date1, date2) => date1 - date2);
        this.plagesHorairesInoccupable.forEach(plage => {
            plage.type = "inoccupable";
        });
        this.plagesHorairesInoccupable.sort((date1, date2) => date1 - date2);
    },
}
</script>

<style scoped>
.card {
    padding: 10px;
    margin: 10px;
}
.reserve {
    background-color: rgb(228, 222, 117);
}
.inoccupable {
    background-color: #ff0000;
}
#plagesDivision {
    display: flex;
    flex-direction: row;
}
#createPlageForm {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.formElements{
    margin: 10px;
    padding: 10px;
}
</style>