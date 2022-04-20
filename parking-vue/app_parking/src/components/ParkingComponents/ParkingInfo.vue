<template>
    <div>
        <div id="infoCard" class="hero is-link">
            <div id="parkingCard">
                <p class="title">Parking : </p>
                <p class="subtitle">{{parking.emplacement}}</p>
                <p class="subtitle">Price: {{parking.prix}}$</p>
            </div>
            <router-link  :to="{path:`/user/${owner.id_utilisateur}`}">
            <div class="card notification is-primary is-light" id="ownerCard">
                <h5><strong>Propriétaire: </strong>{{owner.prenom}} {{owner.nom}}</h5> 
                <p> <strong>Cote: </strong>{{owner.cote}}</p>
                <p> <strong>Courriel: </strong>{{owner.courriel}}</p>
            </div>
            </router-link>
        </div>
    </div>
</template>

<style scoped>
    #infoCard {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    #ownerCard {
        display: flex;
        flex-direction: column;
        align-items: start;
        margin: 10px;
        padding: 1rem;
    }
    #parkingCard{
        display: flex;
        flex-direction: column;
        align-items: start;
        margin: 10px;
        padding: 1rem;
    }
</style>

<script>
import { API } from "../../utility/api.js";
export default {
    data() {
        return {
            api : new API(),
        }
    },
    props: {
        parking: Object,
        owner: Object,
    },
}
</script>
