<template>
    <div id="userWrap" class="hero is-primary">
        <div id="userInfoCard" >
            <div class="title">{{this.user.prenom}} {{this.user.nom}}</div>
            <div class="subtitle">{{this.user.courriel}}</div>
        </div>
        <div id="coteCard" v-if="this.user.cote != undefined">
            <div class="subtitle">Cote: {{this.user.cote}}</div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            user: Object,
        };
    },
    methods: {
        getUser() {
            axios.get('/user/' + this.$route.params.id)
                .then(response => {
                    this.user = response.data;
                })
                .catch(error => {
                    console.log(error);
                });
            this.user = {
                id: 1,
                prenom: "Jean",
                nom: "Dupont",
                courriel: "jean@email.com",
            }
        }
    },
    created() {
        this.getUser();
    },
};
</script>

<style scoped>
    #coteCard{
        padding: 20px;
    }

    #userWrap {
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
        justify-content: space-between;
    }

    #userInfoCard {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 10px;
    }
</style>