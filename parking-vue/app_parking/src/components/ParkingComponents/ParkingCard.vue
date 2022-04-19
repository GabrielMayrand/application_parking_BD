<template>
    <div class="container" id="parkingCard">
        <div class="notification is-link">
            <router-link  :to="{path:`/parking/${this.parking.id_stationnement}`}">
                <h4 class="card-title">Address: {{ this.parking.emplacement }}</h4>
                <div>Price: {{this.parking.prix}}$</div>
            </router-link>
        </div>
        
    </div>
</template>

<script>
export default {
    name: "ParkingCard",
    props: {
        parking: Object,
    },
};
</script>
<style scoped>
#parkingCard {
    margin-bottom: 20px;
    padding: 10px;
}
</style>