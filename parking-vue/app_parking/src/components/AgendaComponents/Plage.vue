<template>
<div :id="plage.id_plage_horaires">
    <div class="card"> 
        {{plage.date_arrivee}}
        {{plage.date_depart}}
    </div>
    <button class="button is-danger is-light" v-if="connectedUser == ownerId || plage.id_utilisateur == connectedUser">Delete</button>
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
            connectedUser: Object,
        };
    },
    props:{    
        plage: Object,
    },
    async created(){
        if(Cookies.get('token') != undefined){
            await this.api.getTokenInfo(Cookies.get('token'));
            this.connectedUser = this.api.response[0].id;
        }
        await this.api.getParkingById(this.pageId);
        this.ownerId = this.api.response[0].id_utilisateur;

    },
}
</script>

<style scoped>
.card {
    padding: 10px;
    margin: 10px;
}
</style>