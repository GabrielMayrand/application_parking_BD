/<template>
    <div>
        <ParkingInfo v-if="!isFetching" :parking="parking[0]" :owner="owner[0]"/>
        <Agenda v-if="!isFetching" :plagesHorairesReservation="plagesHorairesReservation" :plagesHorairesInoccupable="plagesHorairesInoccupable" :finalDate="parking[0].date_fin"/>
        <!-- <ParkingHoraire :parking="this.parking[0]" :plagesHoraire="this.plagesHoraire"/> -->
    </div>
</template>

<script>
import ParkingInfo from "../components/ParkingComponents/ParkingInfo.vue";
import Agenda from "../components/AgendaComponents/Agenda.vue";
// import ParkingHoraire from "../components/ParkingComponents/ParkingHoraire.vue";
import {API} from "../utility/api.js";
export default {
    name : "Parking",
    data(){
        return {
            pageId : this.$route.params.id,
            api : new API(),
            parking: [],
            owner: [],
            plagesHorairesReservation: [],
            plagesHorairesInoccupable: [],
            isFetching: true,
        }
    },
    components: {
        ParkingInfo,
        Agenda,
        // ParkingHoraire,
    },
    methods: {
        async getParking() {
            await this.api.getParkingById(this.pageId);
            this.parking = this.api.response;
            this.getOwner();
        },
        async getOwner() {
            await this.api.getUserById(this.parking[0].id_utilisateur);
            this.owner = this.api.response;
            this.getPlagesHorairesReservation();
        },
        async getPlagesHorairesReservation() {
            await this.api.getPlagesHorairesReservation(this.pageId);
            this.plagesHorairesReservation = this.api.response;
            this.getPlagesHorairesInoccupable();
        },
        async getPlagesHorairesInoccupable() {
            await this.api.getPlagesHorairesInoccupable(this.pageId);
            this.plagesHorairesInoccupable = this.api.response;
            this.isFetching = false;
        },
    },
    async created() {
        this.$root.$refs.Parking = this;
        this.getParking();
    },
}
</script>