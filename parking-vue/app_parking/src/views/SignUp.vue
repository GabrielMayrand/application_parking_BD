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
    <label class="label">Username</label>
    <div class="control ">
        <input class="input" type="text" placeholder="johnsmith" v-model="username">
    </div>
    <p class="help is-danger" v-if="!validUserName">This username is already taken or invalid</p>
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
        <input class="input" type="password" required v-model="password">
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
export default {
  data() {
    return {
        api : new API(),
        validUserName: true,
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
      if(this.validateEmail() && this.validateUserName() && this.validateFirstName() && this.validateLastName() && this.validatePassword()){
        await this.api.postSignUp(this.firstname, this.lastname, this.email, this.password);
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
        console.log(this.email);
        console.log(this.validEmail);
        return this.validEmail;
    },

    validatePassword(){
      if(this.password.length > 5){
        this.validPassword = true;
      }
      else{
        this.validPassword = false;
      }
      console.log(this.password);
      console.log(this.validPassword);
      return this.validPassword;
    },

    validateUserName(){
      var re = /^[a-zA-Z0-9]+$/;
      if(re.test(String(this.username).toLowerCase())){
        this.validUserName = true;
      }
      else{
        this.validUserName = false;
      }
      console.log(this.username);
      console.log(this.validUserName);
      return this.validUserName;
    },

    validateFirstName(){
      var re = /^[a-zA-Z]+$/;
      if(re.test(String(this.firstname).toLowerCase())){
        this.validFirstName = true;
      }
      else{
        this.validFirstName = false;
      }
      console.log(this.firstname);
      console.log(this.validFirstName);
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
      console.log(this.lastname);
      console.log(this.validLastName);
      return this.validLastName;
    }

  },
  
};
</script>