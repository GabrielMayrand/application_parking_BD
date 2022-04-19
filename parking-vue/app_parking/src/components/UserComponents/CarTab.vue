 <template>
  <div>
        <div id="createCarForm">
            <button class="button is-primary" @click="postUserCar()">Create Car</button>
            
            <div class="form">
                    <input class="input" type="input" placeholder="License plate: AAAAAA" id="plaque"/>           
                    <input class="input" type="input" placeholder="Model" id="model"/>
                    <input class="input" type="input" placeholder="Color" id="color"/>
            </div>
            <div id="dimensionsForm" class="form">
                    <input class="input" type="input" placeholder="height" id="height"/>
                    <input class="input" type="input" placeholder="width" id="width"/>
                    <input class="input" type="input" placeholder="length" id="length"/>
            </div>
        </div>
        <div class="tag is-danger" v-if="infoWrong">
            Some information is missing or is incorrect.
        </div>
        <CarList :CarList="carList" v-if="!isFetching"/>
  </div>
</template>

<script>
import CarList from "./CarList.vue"
import {API} from "../../utility/api.js";

export default {
    data(){
        return {
            infoWrong: false,
            carList: [],
            api: new API(),
            isFetching: true,
            pageId : this.$route.params.id,
        }
    },

    components: {
        CarList,
    },

    methods :{
      async getCarList() {
        await this.api.getUserCars(this.pageId);
        this.carList = this.api.response;
        this.isFetching = false;
      },
      async postUserCar() {
            // if(document.getElementById("height").match("[0-9]") && document.getElementById("width").value.isdigit() && document.getElementById("length").value.isdigit()
            // && document.getElementById("height").value != "" && document.getElementById("width").value != "" && document.getElementById("length").value != ""
            // && document.getElementById("model").value != "" && document.getElementById("color").value != "" && document.getElementById("plaque").value.length == 6){
            //     console.log(document.getElementById("plaque").value);
                await this.api.postCar(this.pageId, document.getElementById("plaque").value, document.getElementById("model").value, document.getElementById("color").value, document.getElementById("length").value,  document.getElementById("width").value, document.getElementById("height").value);
                this.infoWrong = false;
                this.getCarList();
            // }
            // else{
            // this.infoWrong = true;
            // }
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