<template>
    <div>
        <div class="notification is-info is-large ">
            {{dateDay.getFullYear()}}-{{dateDay.getMonth()}}-{{dateDay.getDate()}}
        </div>
        <ul v-for="block in blocks" v-bind:key="block.id">
            <Block :block="block" :plagesBlock="convertFunctiontoArray(plagesBlock)"/>
        </ul>
    </div>
</template>

<script>
import Block from "./Block.vue";

export default {
    data() {
        return {
            blocks: Array,
            plagesBlock: Array,
        }
    },
    props: {
        dateDay: Date,
        plages: Array,
    },
    methods: {
        getPlagesBlock() {
            console.log(this.plages[1]);
            this.plages.every(plage => {
                let date = new Date(plage.date.split("-")[0], plage.date.split("-")[1] - 1, plage.date.split("-")[2]);
                if(date.getTime() == this.date.getTime()){
                    this.plagesBlock.push(plage);
                    return true;
                }
                else if(date.getTime() < this.date.getTime()){
                    return true;
                }
                else{
                    return false;
                }
            });
        },
        convertFunctiontoArray(functionToConvert){
            let array = [];
            for(let i = 0; i < functionToConvert.length; i++){
                array.push(functionToConvert[i]);
            }
            return array;
        },
    },
    components: {
        Block,
    },
    created () {
        //console.log("plages:"+this.plages);
        this.getPlagesBlock();
        //console.log(this.plagesBlock);
        this.blocks = [
            {
                id: 1,
                date: this.date,
                startTime: "00:00",
                endTime: "00:15",
            },
            {
                id: 2,
                date: this.date,
                startTime: "00:15",
                endTime: "00:30",
            },
            {
                id: 3,
                date: this.date,
                startTime: "00:30",
                endTime: "00:45",
            },
            {
                id: 4,
                date: this.date,
                startTime: "00:45",
                endTime: "01:00",
            },
            {
                id: 5,
                date: this.date,
                startTime: "01:00",
                endTime: "01:15",
            },
            {
                id: 6,
                date: this.date,
                startTime: "01:15",
                endTime: "01:30",
            },
            {
                id: 7,
                date: this.date,
                startTime: "01:30",
                endTime: "01:45",
            },
            {
                id: 8,
                date: this.date,
                startTime: "01:45",
                endTime: "02:00",
            },
            {
                id: 9,
                date: this.date,
                startTime: "02:00",
                endTime: "02:15",
            },
            {
                id: 10,
                date: this.date,
                startTime: "02:15",
                endTime: "02:30",
            },
            {
                id: 11,
                date: this.date,
                startTime: "02:30",
                endTime: "02:45",
            },
            {
                id: 12,
                date: this.date,
                startTime: "02:45",
                endTime: "03:00",
            },
            {
                id: 13,
                date: this.date,
                startTime: "03:00",
                endTime: "03:15",
            },
            {
                id: 14,
                date: this.date,
                startTime: "03:15",
                endTime: "03:30",
            },
            {
                id: 15,
                date: this.date,
                startTime: "03:30",
                endTime: "03:45",
            },
            {
                id: 16,
                date: this.date,
                startTime: "03:45",
                endTime: "04:00",
            },
            {
                id: 17,
                date: this.date,
                startTime: "04:00",
                endTime: "04:15",
            },
            {
                id: 18,
                date: this.date,
                startTime: "04:15",
                endTime: "04:30",
            },
            {
                id: 19,
                date: this.date,
                startTime: "04:30",
                endTime: "04:45",
            },
            {
                id: 20,
                date: this.date,
                startTime: "04:45",
                endTime: "05:00",
            },
            {
                id: 21,
                date: this.date,
                startTime: "05:00",
                endTime: "05:15",
            },
            {
                id: 22,
                date: this.date,
                startTime: "05:15",
                endTime: "05:30",
            },
            {
                id: 23,
                date: this.date,
                startTime: "05:30",
                endTime: "05:45",
            },
            {
                id: 24,
                date: this.date,
                startTime: "05:45",
                endTime: "06:00",
            },
            {
                id: 25,
                date: this.date,
                startTime: "06:00",
                endTime: "06:15",
            },
            {
                id: 26,
                date: this.date,
                startTime: "06:15",
                endTime: "06:30",
            },
            {
                id: 27,
                date: this.date,
                startTime: "06:30",
                endTime: "06:45",
            },
            {
                id: 28,
                date: this.date,
                startTime: "06:45",
                endTime: "07:00",
            },
            {
                id: 29,
                date: this.date,
                startTime: "07:00",
                endTime: "07:15",
            },
            {
                id: 30,
                date: this.date,
                startTime: "07:15",
                endTime: "07:30",
            },
            {
                id: 31,
                date: this.date,
                startTime: "07:30",
                endTime: "07:45",
            },
            {
                id: 32,
                date: this.date,
                startTime: "07:45",
                endTime: "08:00",
            },
            {
                id: 33,
                date: this.date,
                startTime: "08:00",
                endTime: "08:15",
            },
            {
                id: 34,
                date: this.date,
                startTime: "08:15",
                endTime: "08:30",
            },
            {
                id: 35,
                date: this.date,
                startTime: "08:30",
                endTime: "08:45",
            },
            {
                id: 36,
                date: this.date,
                startTime: "08:45",
                endTime: "09:00",
            },
            {
                id: 37,
                date: this.date,
                startTime: "09:00",
                endTime: "09:15",
            },
            {
                id: 38,
                date: this.date,
                startTime: "09:15",
                endTime: "09:30",
            },
            {
                id: 39,
                date: this.date,
                startTime: "09:30",
                endTime: "09:45",
            },
            {
                id: 40,
                date: this.date,
                startTime: "09:45",
                endTime: "10:00",
            },
            {
                id: 41,
                date: this.date,
                startTime: "10:00",
                endTime: "10:15",
            },
            {
                id: 42,
                date: this.date,
                startTime: "10:15",
                endTime: "10:30",
            },
            {
                id: 43,
                date: this.date,
                startTime: "10:30",
                endTime: "10:45",
            },
            {
                id: 44,
                date: this.date,
                startTime: "10:45",
                endTime: "11:00",
            },
            {
                id: 45,
                date: this.date,
                startTime: "11:00",
                endTime: "11:15",
            },
            {
                id: 46,
                date: this.date,
                startTime: "11:15",
                endTime: "11:30",
            },
            {
                id: 47,
                date: this.date,
                startTime: "11:30",
                endTime: "11:45",
            },
            {
                id: 48,
                date: this.date,
                startTime: "11:45",
                endTime: "12:00",
            },
            {
                id: 49,
                date: this.date,
                startTime: "12:00",
                endTime: "12:15",
            },
            {
                id: 50,
                date: this.date,
                startTime: "12:15",
                endTime: "12:30",
            },
            {
                id: 51,
                date: this.date,
                startTime: "12:30",
                endTime: "12:45",
            },
            {
                id: 52,
                date: this.date,
                startTime: "12:45",
                endTime: "13:00",
            },
            {
                id: 53,
                date: this.date,
                startTime: "13:00",
                endTime: "13:15",
            },
            {
                id: 54,
                date: this.date,
                startTime: "13:15",
                endTime: "13:30",
            },
            {
                id: 55,
                date: this.date,
                startTime: "13:30",
                endTime: "13:45",
            },
            {
                id: 56,
                date: this.date,
                startTime: "13:45",
                endTime: "14:00",
            },
            {
                id: 57,
                date: this.date,
                startTime: "14:00",
                endTime: "14:15",
            },
            {
                id: 58,
                date: this.date,
                startTime: "14:15",
                endTime: "14:30",
            },
            {
                id: 59,
                date: this.date,
                startTime: "14:30",
                endTime: "14:45",
            },
            {
                id: 60,
                date: this.date,
                startTime: "14:45",
                endTime: "15:00",
            },
            {
                id: 61,
                date: this.date,
                startTime: "15:00",
                endTime: "15:15",
            },
            {
                id: 62,
                date: this.date,
                startTime: "15:15",
                endTime: "15:30",
            },
            {
                id: 63,
                date: this.date,
                startTime: "15:30",
                endTime: "15:45",
            },
            {
                id: 64,
                date: this.date,
                startTime: "15:45",
                endTime: "16:00",
            },
            {
                id: 65,
                date: this.date,
                startTime: "16:00",
                endTime: "16:15",
            },
            {
                id: 66,
                date: this.date,
                startTime: "16:15",
                endTime: "16:30",
            },
            {
                id: 67,
                date: this.date,
                startTime: "16:30",
                endTime: "16:45",
            },
            {
                id: 68,
                date: this.date,
                startTime: "16:45",
                endTime: "17:00",
            },
            {
                id: 69,
                date: this.date,
                startTime: "17:00",
                endTime: "17:15",
            },
            {
                id: 70,
                date: this.date,
                startTime: "17:15",
                endTime: "17:30",
            },
            {
                id: 71,
                date: this.date,
                startTime: "17:30",
                endTime: "17:45",
            },
            {
                id: 72,
                date: this.date,
                startTime: "17:45",
                endTime: "18:00",
            },
            {
                id: 73,
                date: this.date,
                startTime: "18:00",
                endTime: "18:15",
            },
            {
                id: 74,
                date: this.date,
                startTime: "18:15",
                endTime: "18:30",
            },
            {
                id: 75,
                date: this.date,
                startTime: "18:30",
                endTime: "18:45",
            },
            {
                id: 76,
                date: this.date,
                startTime: "18:45",
                endTime: "19:00",
            },
            {
                id: 77,
                date: this.date,
                startTime: "19:00",
                endTime: "19:15",
            },
            {
                id: 78,
                date: this.date,
                startTime: "19:15",
                endTime: "19:30",
            },
            {
                id: 79,
                date: this.date,
                startTime: "19:30",
                endTime: "19:45",
            },
            {
                id: 80,
                date: this.date,
                startTime: "19:45",
                endTime: "20:00",
            },
            {
                id: 81,
                date: this.date,
                startTime: "20:00",
                endTime: "20:15",
            },
            {
                id: 82,
                date: this.date,
                startTime: "20:15",
                endTime: "20:30",
            },
            {
                id: 83,
                date: this.date,
                startTime: "20:30",
                endTime: "20:45",
            },
            {
                id: 84,
                date: this.date,
                startTime: "20:45",
                endTime: "21:00",
            },
            {
                id: 85,
                date: this.date,
                startTime: "21:00",
                endTime: "21:15",
            },
            {
                id: 86,
                date: this.date,
                startTime: "21:15",
                endTime: "21:30",
            },
            {
                id: 87,
                date: this.date,
                startTime: "21:30",
                endTime: "21:45",
            },
            {
                id: 88,
                date: this.date,
                startTime: "21:45",
                endTime: "22:00",
            },
            {
                id: 89,
                date: this.date,
                startTime: "22:00",
                endTime: "22:15",
            },
            {
                id: 90,
                date: this.date,
                startTime: "22:15",
                endTime: "22:30",
            },
            {
                id: 91,
                date: this.date,
                startTime: "22:30",
                endTime: "22:45",
            },
            {
                id: 92,
                date: this.date,
                startTime: "22:45",
                endTime: "23:00",
            },
            {
                id: 93,
                date: this.date,
                startTime: "23:00",
                endTime: "23:15",
            },
            {
                id: 94,
                date: this.date,
                startTime: "23:15",
                endTime: "23:30",
            },
            {
                id: 95,
                date: this.date,
                startTime: "23:30",
                endTime: "23:45",
            },
            {
                id: 96,
                date: this.date,
                startTime: "23:45",
                endTime: "00:00",
            },
        ]
    },
    
}
</script>
