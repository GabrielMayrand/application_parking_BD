<template>
    <div id="headerWrapper" class="card">
        <button class="button headerItem" @click="previousWeek()" v-if="minDate < todayDate">Précédent</button>
        <p class="headerItem">{{this.todayDate.getFullYear()}}-{{this.todayDate.getMonth()}}-{{this.todayDate.getDate()}}</p>
        <strong>-</strong>
        <p class="headerItem">{{this.finalWeekDate.getFullYear()}}-{{this.finalWeekDate.getMonth()}}-{{this.finalWeekDate.getDate()}}</p>
        <button class="button headerItem" @click="nextWeek()" v-if="finalReservationDate > finalWeekDate">Suivant</button>
    </div>
</template>

<style scoped>
    #headerWrapper {
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
    .headerItem {
        margin: 10px;
        padding: 10px;
    }
</style>

<script>

export default {
    data() {
        return {
            minDate : new Date(),
        };
    },
    props: {
        todayDate: Date,
        finalWeekDate: Date,
        finalReservationDate: Date,
    },
    methods:{
        nextWeek(){
            this.$root.$refs.ParkingHoraire.nextWeek();
        },
        previousWeek(){
            this.$root.$refs.ParkingHoraire.previousWeek();
        },
    },
    created() {
        this.minDate = new Date();
    },
}
</script>
