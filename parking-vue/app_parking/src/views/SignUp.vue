<template>
  <!-- signup template -->
  <div class="card">
    <div class="field">
    <label class="label">First name</label>
    <div class="control">
        <input class="input" type="text" placeholder="John">
    </div>
    </div>

    <div class="field">
    <label class="label">Last name</label>
    <div class="control">
        <input class="input" type="text" placeholder="Smith">
    </div>
    </div>

    <div class="field">
    <label class="label">Username</label>
    <div class="control ">
        <input class="input" type="text" placeholder="johnsmith">
    </div>
    <p class="help is-danger" v-if="validUserName">This username is already taken</p>
    </div>

    <div class="field">
    <label class="label">Email</label>
    <div class="control ">
        <input class="input" type="email" placeholder="john@mail.com">
    </div>
    <p class="help is-danger" v-if="validEmail">This email is invalid</p>
    </div>
  </div>
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
        validUserName: false,
        validEmail: false,
        firstname: "",
        lastname: "",
        email: "",
        password: "",
        inputsValid: false,
    };
  },
  
};
</script>