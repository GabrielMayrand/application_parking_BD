<template>
    <div id="carCard" class="card is-link">
        <div class="title">
            {{this.carCard.Model}}
        </div>
        <div class="subtitle">
            {{this.carCard.Couleur}}
        </div>
        <div class="input">
            Dimensions: 
            {{this.carCard.Dimensions[0]}}x
            {{this.carCard.Dimensions[1]}}x
            {{this.carCard.Dimensions[2]}}
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