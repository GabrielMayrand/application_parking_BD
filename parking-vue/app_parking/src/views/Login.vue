<template>
  <!-- signup template -->
  <form class="card" @submit.prevent="submitForm">

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

export default {
  data() {
    return {
        validEmail: true,
        validPassword: true,
        email: "",
        password: "",
    };
  },

  methods: {
    submitForm(){
      if(this.validateEmail() && this.validateUserName() && this.validateFirstName() && this.validateLastName() && this.validatePassword()){
        console.log("form submitted");
        this.$router.push({ name: 'Home' });
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

  },
  
};
</script>