<template>
    <div>
        <Header :todayDate="todayDate" :finalWeekDate="finalWeekDate" :finalReservationDate="finalReservationDate"/>
        <Week :todayDate="todayDate" :finalReservationDate="finalReservationDate" :finalWeekDate="finalWeekDate" :plagesWeek="plagesWeek"/>
    </div>
</template>

<script>
import Header from "./Header.vue";
import Week from "./Week.vue";

export default {
    data() {
        return {
            plagesWeek: [],
            todayDate: new Date(),
            finalWeekDate: new Date(),
            finalReservationDate: new Date(),
        }
    },
    components : {
        Header,
        Week,
    },
    props: {
        plagesHoraire: Array,
        parking: Object,
    },
    methods :{
        nextWeek(){
            this.todayDate = new Date(this.todayDate.setDate(this.todayDate.getDate() + 7));
            this.finalWeekDate = new Date(this.finalWeekDate.setDate(this.finalWeekDate.getDate() + 7));
        },
        previousWeek(){
            this.todayDate = new Date(this.todayDate.setDate(this.todayDate.getDate() - 7));
            this.finalWeekDate = new Date(this.finalWeekDate.setDate(this.finalWeekDate.getDate() - 7));
        },
        getWeekBlocks(){
            this.plagesHoraire.every(plage => {
                let date = new Date(plage.date.split("-")[0], plage.date.split("-")[1] - 1, plage.date.split("-")[2]);
                if(date.getTime() >= this.todayDate.getTime() && date.getTime() <= this.finalWeekDate.getTime()){
                    this.plagesWeek.push(plage);
                    return true;
                }
                else if(date.getTime() > this.finalWeekDate.getTime()){
                    return false;
                }
                else{
                    return true;
                }
            });
        }
    },
    created() {
        this.$root.$refs.ParkingHoraire = this;
        this.finalReservationDate = new Date(this.finalReservationDate.setDate(this.todayDate.getDate() + this.parking.advanceDays));
        this.finalWeekDate = new Date(this.finalWeekDate.setDate(this.todayDate.getDate() + 6));
        this.getWeekBlocks();
    },
}
</script>
