<template>
<div :id="plage.id_plage_horaires">
    <div class="card"> 
        {{plage.id_plage_horaires}}
        {{plage.date_arrivee}}
        {{plage.date_depart}}
    </div>
    <button class="button is-danger is-light">Delete</button>
</div>
</template>

<script>
export default {
    props:{
        plage: Object,
    },
}
</script>

<style scoped>
.card {
    padding: 10px;
    margin: 10px;
}
</style>