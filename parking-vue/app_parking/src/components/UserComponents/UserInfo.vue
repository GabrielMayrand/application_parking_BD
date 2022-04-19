<template>
    <div id="userWrap" class="hero is-primary">
        <div id="userInfoCard" >
            <div class="title">{{user.prenom}} {{user.nom}}</div>
            <div class="subtitle">{{user.courriel}}</div>
        </div>
        <div id="coteCard" v-if="user.cote != undefined">
            <div class="subtitle">Cote: {{user.cote}}</div>
        </div>
    </div>
</template>

<script>

export default {
    props:{
        user: Object,
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