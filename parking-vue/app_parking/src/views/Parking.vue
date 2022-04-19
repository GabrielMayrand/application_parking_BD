/<template>
    <div>
        <ParkingInfo :parking="this.parking[0]"/>
        <ParkingHoraire :parking="this.parking[0]" :plagesHoraire="this.plagesHoraire"/>
    </div>
</template>

<script>
import ParkingInfo from "../components/ParkingComponents/ParkingInfo.vue";
import ParkingHoraire from "../components/ParkingComponents/ParkingHoraire.vue";
import {API} from "../utility/api.js";
export default {
    name : "Parking",
    components: {
        ParkingInfo,
        ParkingHoraire,
    },
    data(){
        return {
            pageId : this.$route.params.id,
            api : new API(),
            parking: Array,
            plagesHoraire: Array,
        }
    },
    methods: {
        async getParking() {
            await this.api.getParkingById(this.pageId);
            this.parking = this.api.response;
            console.log(this.parking[0]);
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