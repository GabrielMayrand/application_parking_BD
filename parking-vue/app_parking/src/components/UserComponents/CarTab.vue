 <template>
  <div>
    <CarList :CarList="carList"/>
  </div>
</template>

<script>
import CarList from "./CarList.vue"

export default {
    data(){
        return {
            carList: Array
        }
    },

    components: {
        CarList,
    },

    methods :{
      getCarList() {
        this.carList = [
                {
                    id: 1,
                    Model: "Audi",
                    Couleur: "rouge",
                    Dimensions: [1,2,3],
                },
                {
                    id: 2,
                    Model: "BMW",
                    Couleur: "bleu",
                    Dimensions: [1,2,3],
                },
                {
                    id: 3,
                    Model: "Mercedes",
                    Couleur: "noir",
                    Dimensions: [1,2,3],
                },
        ];
      },
    },

    created() {
        this.getCarList();
    },
};
</script>

<style scoped>

</style>