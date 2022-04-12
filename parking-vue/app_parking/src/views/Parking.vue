/<template>
    <div>
        <ParkingInfo :parking="this.parking"/>
        <ParkingHoraire :parking="this.parking" :plagesHoraire="this.plagesHoraire"/>
    </div>
</template>

<script>
import ParkingInfo from "../components/ParkingComponents/ParkingInfo.vue";
import ParkingHoraire from "../components/ParkingComponents/ParkingHoraire.vue";
export default {
    name : "Parking",
    components: {
        ParkingInfo,
        ParkingHoraire,
    },
    data(){
        return {
            parking: Object,
            plagesHoraire: Array,
        }
    },
    methods: {
        getParking() {
           this.parking = {
                id: 1,
                advanceDays: 10,
                finalDate: "2019-12-12",
                dimensions:[10,30,40],
                address: "155 rue de la gare, Québec, QC, Canada",
                landlordId: 45,
            }
        },
        getPlagesHoraire() {
            this.plagesHoraire = [
                {
                    id: 0,
                    startTime: "10:00",
                    endTime: "10:15",
                    price: 10,
                    date: "2022-03-20",
                },
                {
                    id: 1,
                    startTime: "10:00",
                    endTime: "10:15",
                    price: 10,
                    date: "2022-03-25",
                },
                {
                    id: 2,
                    startTime: "13:00",
                    endTime: "13:15",
                    price: 10,
                    date: "2022-03-25",
                },
                {
                    id: 3,
                    startTime: "14:00",
                    endTime: "14:15",
                    price: 10,
                    date: "2022-03-25",
                },
                {
                    id: 4,
                    startTime: "14:00",
                    endTime: "14:15",
                    price: 10,
                    date: "2022-03-30",
                },
            ]
        },
    },
    created() {
        this.getParking();
        this.getPlagesHoraire();

    },
};
</script>