 <template>
  <div>
      <div id="createCarForm">
          <button class="button is-primary">Create Car</button>
          <div class="form">
                <input class="input" type="input" placeholder="License plate"/>           
                <input class="input" type="input" placeholder="Model"/>
                <input class="input" type="input" placeholder="Color"/>
          </div>
          <div id="dimensionsForm" class="form">
                <input class="input" type="input" placeholder="height"/>
                <input class="input" type="input" placeholder="width"/>
                <input class="input" type="input" placeholder="length"/>
          </div>

      </div>
        
        
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
    #createCarForm{
        display: flex;
        justify-content: column;
    }
    .input{
        padding: 10px;
        margin-bottom: 10px;
    }
    .button{
        margin: 5px;
    }
    .form{
        margin: 5px;
    }
</style>