<template>
    <div>
        <div id="infoCard" class="hero is-link">
            <div id="parkingCard">
                <p class="title">Stationnement : </p>
                <p class="subtitle">{{parking.address}}</p>
            </div>
            <router-link  :to="{path:`/user/${owner.id}`}">
            <div class="card notification is-primary is-light" id="ownerCard">
                <h5><strong>Propriétaire: </strong>{{owner.prenom}} {{owner.nom}}</h5> 
                <p> <strong>Cote: </strong>{{owner.cote}}</p>
                <p> <strong>Courriel: </strong>{{owner.email}}</p>
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
export default {
    data() {
        return {
            owner: Object,
        }
    },
    props: {
        parking: Object,
    },
    methods: {
        getOwner() {
           this.owner = {
                id: 1,
                prenom: "Jean",
                nom: "Dupont",
                cote: 5,
                email: "jeanDupont@mail.com",
            }
        },
    },
    mounted() {
        this.getOwner();
    },
}
</script>
