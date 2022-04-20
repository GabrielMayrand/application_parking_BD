<template>
<div :id="plage.id_plage_horaires" v-if="plage.date_arrivee != null && plage.date_depart != null">
    <div class="card"> 
        {{plage.date_arrivee}}
        {{plage.date_depart}}
    </div>
    <button class="button is-danger is-light" v-if="connectedUser === ownerId || plage.id_utilisateur === connectedUser">Delete</button>
</div>
</template>

<script>
import Cookies from 'js-cookie';
import {API} from "../../utility/api.js";
export default {
    data() {
        return {
            api: new API(),
            pageId : this.$route.params.id,
            ownerId : Number,
            connectedUser: String,
        };
    },
    props:{    
        plage: Object,
    },
    async created(){
        if(Cookies.get('token') != undefined){
            await this.api.getTokenInfo(Cookies.get('token'));
            //console.log(this.api.response);
            this.connectedUser = this.api.response[0].id_utilisateur;
        }
        await this.api.getParkingById(this.pageId);
        this.ownerId = this.api.response[0].id_utilisateur;
        console.log(this.ownerId);
        console.log(this.connectedUser);
        console.log(this.plage.id_utilisateur);
    },
}
</script>

<style scoped>
.card {
    padding: 10px;
    margin: 10px;
}
</style>