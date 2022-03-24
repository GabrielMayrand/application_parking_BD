<template>
    <div>
        <Header :todayDate="this.todayDate" :finalWeekDate="this.finalWeekDate"/>
        <Week :todayDate="this.todayDate" :finalReservationDate="this.finalReservationDate" :finalWeekDate="this.finalWeekDate" :plagesWeek="this.plagesWeek"/>
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
    mounted() {
        this.finalReservationDate = new Date(this.finalReservationDate.setDate(this.todayDate.getDate() + this.parking.advanceDays));
        this.finalWeekDate = new Date(this.finalWeekDate.setDate(this.todayDate.getDate() + 6));
        this.getWeekBlocks();
        
    },
}
</script>
