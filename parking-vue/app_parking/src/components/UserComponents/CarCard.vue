<template>
    <div id="carCard" class="card is-link">
        <div class="title">
            {{this.carCard.modele}}
        </div>
        <div class="subtitle">
            {{this.carCard.couleur}}
        </div>
        <div class="input">
            Dimensions: 
            {{this.carCard.longueur}}x
            {{this.carCard.largeur}}x
            {{this.carCard.hauteur}}
        </div>
    </div>
</template>

<style scoped>
    #carCard {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        padding: 100px;
        margin: 100px;
    }
</style>

<script>
export default {
    name : "CarCard",
    props: {
        carCard: Object,
    },
};
</script>