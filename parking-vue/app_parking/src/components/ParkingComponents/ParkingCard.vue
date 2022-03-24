<template>
    <div class="container" id="parkingCard">
        <div class="notification is-link">
            <router-link  :to="{path:`/parking/${this.parking.id}`}">
                <h4 class="card-title">{{ this.parking.address }}</h4>
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
    max-width: fit-content;
}

</style>