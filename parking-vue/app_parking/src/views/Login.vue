<template>
  <!-- signup template -->
  <form class="card" @submit.prevent="submitForm">

    <div class="field">
    <label class="label">Email</label>
    <div class="control ">
        <input class="input" type="email" placeholder="john@mail.com" v-model="email">
    </div>
    <p class="help is-danger" v-if="!validEmail">{{invalidMessage}}</p>
    </div>

    <div class="field">
    <label class="label">Password</label>
    <div class="control ">
        <input class="input" type="password" required v-model="password" placeholder="password">
    </div>
    </div>
    <button type="submit" class="button is-primary">Submit</button>
  </form>
</template>
<style scoped>
    .card {
        max-width: 50%;
        padding: 10px;
        margin: auto;
        position: relative;
    }
</style>


<script>
import {API} from "../utility/api.js";
import Cookies from "js-cookie";
export default {
  data() {
    return {
      api : new API(),
        validEmail: true,
        validPassword: true,
        email: "",
        password: "",
        invalidMessage: "",
    };
  },

  methods: {
    async submitForm(){
      if(this.validateEmail() && this.validatePassword()){
        let md5 = require('md5');
        let hash = md5(this.password);
        await this.api.postLogin(this.email, hash);
        if(this.api.response.message == "Utilisateur non trouvé" || this.api.response.message == "Mot de passe incorrect")
        {
          this.validEmail = false;
          this.invalidMessage = this.api.response.message;
        }
        else if (this.api.response[0].courriel == this.email )
        {
          Cookies.set('user', this.api.response[0].id_utilisateur);
          Cookies.set('user_type', this.api.response[0].type_utilisateur);
          this.$router.push('/user/' + this.api.response[0].id_utilisateur);
        }
        
      }

    },

    validateEmail(){
        var re = /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
        if(re.test(String(this.email).toLowerCase())){
          this.validEmail = true;
        }
        else{
          this.validEmail = false;
        }
        return this.validEmail;
    },

    validatePassword(){
      if(this.password.length > 5){
        this.validPassword = true;
      }
      else{
        this.validPassword = false;
      }
      return this.validPassword;
    },

  },
  
};
</script>