<template>
  <!-- signup template -->
  <form class="card" @submit.prevent="submitForm">
    <div class="field">
    <label class="label">First name</label>
    <div class="control">
        <input class="input" type="text" placeholder="John"  v-model="lastname">
    </div>
    </div>

    <div class="field">
    <label class="label">Last name</label>
    <div class="control">
        <input class="input" type="text" placeholder="Smith"  v-model="firstname">
    </div>
    </div>

    <div class="field">
    <label class="label">Email</label>
    <div class="control ">
        <input class="input" type="email" placeholder="john@mail.com" v-model="email">
    </div>
    <p class="help is-danger" v-if="!validEmail">This email is invalid</p>
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
        validFirstName: true,
        validLastName: true,
        validPassword: true,
        firstname: "",
        lastname: "",
        username: "",
        email: "",
        password: "",
    };
  },

  methods: {
    async submitForm(){
      if(this.validateEmail() && this.validateFirstName() && this.validateLastName() && this.validatePassword()){
        let md5 = require('md5');
        let hash = md5(this.password);
        
        await this.api.postSignUp(this.firstname, this.lastname, this.email, hash);
        if(this.api.response.message == "Utilisateur déjà existant")
        {
          this.validEmail = false;
        }
        else
        {
          Cookies.remove("token");
          this.$globalThis = this.api.response[0].token.toString();
          Cookies.set("token", this.api.response[0].token.toString());
          this.$router.push("../user/" + this.api.response.id);
          this.$router.go();
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
      if(this.password.length > 1){
        this.validPassword = true;
      }
      else{
        this.validPassword = false;
      }
      return this.validPassword;
    },

    validateFirstName(){
      var re = /^[a-zA-Z]+$/;
      if(re.test(String(this.firstname).toLowerCase())){
        this.validFirstName = true;
      }
      else{
        this.validFirstName = false;
      }
      return this.validFirstName;
    },

    validateLastName(){
      var re = /^[a-zA-Z]+$/;
      if(re.test(String(this.firstname).toLowerCase())){
        this.validLasttName = true;
      }
      else{
        this.validLastName = false;
      }
      return this.validLastName;
    }

  },

  async created(){
    console.log(Cookies.get("token"));
    await this.api.getTokenInfo(Cookies.get("token"));
  }
  
};
</script>