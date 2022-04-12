<template>
    <div>
        <table id="table" :v-if="!Days.length != 0">
            <tr>
                <th v-for="day in Days" v-bind:key="day.id">
                    <Day :dateDay="day.date" :plages="plagesWeek"/>
                </th>
            </tr>      
      </table>
    </div>
</template>

<style scoped>
    #table {
        width: 100%;
        border-collapse: collapse;
    }
    #table th {
        border: 1px solid whitesmoke;
        padding: 10px;
    }
    #table td {
        border: 1px solid black;
        padding: 10px;
    }
</style>

<script>
import Day from "./Day.vue";

export default {
    data() {
        return {
            Days:Array,
            secondDate: new Date(),
            thirdDate: new Date(),
            forthDate: new Date(),
            fithDate: new Date(),
            sixthDate: new Date(),
            seventhDate: new Date(),
        };
    },
    components: {
        Day,
    },
    props :{
        plagesWeek: Array,
        todayDate: Date,
        finalWeekDate: Date,
        finalReservationDate: Date,
    },
    created() {
        console.log(this.plagesWeek);
        this.secondDate = new Date(this.secondDate.setDate(this.todayDate.getDate() + 1));
        this.thirdDate = new Date(this.thirdDate.setDate(this.todayDate.getDate() + 2));
        this.forthDate = new Date(this.forthDate.setDate(this.todayDate.getDate() + 3));
        this.fithDate = new Date(this.fithDate.setDate(this.todayDate.getDate() + 4));
        this.sixthDate = new Date(this.sixthDate.setDate(this.todayDate.getDate() + 5));
        this.seventhDate = new Date(this.seventhDate.setDate(this.todayDate.getDate() + 6));
        this.Days = [
            {
                id: 1,
                date: this.todayDate,
            },
            {
                id: 2,
                date: this.secondDate,
            },
            {
                id: 3,
                date:  this.thirdDate,
            },
            {
                id: 4,
                date:  this.forthDate,
            },
            {
                id: 5,
                date:  this.fithDate,
            },
            {
                id: 6,
                date:  this.sixthDate,
            },
            {
                id: 7,
                date:  this.seventhDate,
            },
        ];
        
    }
}
</script>
