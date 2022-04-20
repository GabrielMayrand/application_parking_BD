<template>
<nav class="navbar navigation box" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
        <router-link class="navbar-item title is-2" to="/"> Home </router-link>
    </div>
    <div class="navbar-end">
        <div class="navbar-item">
            <div class="buttons" v-if="!LoggedIn">
                <router-link  :to="{path:`/signup`}">
                <a class="button is-primary" ><strong>Sign up</strong></a>
                </router-link>
                <router-link :to="{path:`/login`}">
                <a class="button is-light" ><strong>Login</strong></a>
                </router-link>
            </div>
            <div>
                <button class="button is-light" v-if="LoggedIn" @click="signOut">SignOut</button>
                
                <a class="button is-primary" @click="changePage()" v-if="LoggedIn"><strong>Profile</strong></a>
                
            </div>
        </div>
    </div>
</nav>
</template>

<script>
import {API} from "../utility/api.js";
import Cookies from "js-cookie";
export default {
    name : "Navigation",
    data() {
        return {
            api : new API(),
            LoggedIn: false,
            userId: "",
        };
    },
    methods: {
        signOut() {
            Cookies.remove("token");
            this.$router.push("/");
            this.$router.go();
        },
        changePage() {
        this.$router.push(`/user/${this.userId}`);
        this.$router.go();
        },
    },
    async created() {

        if (Cookies.get("token") != undefined) {
            this.LoggedIn = true;
            await this.api.getTokenInfo(Cookies.get("token"));
            this.userId = this.api.response[0].id_utilisateur;
        }
        
    },
    
};
</script>

<style scoped>
nav {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    list-style-type: none;
    height: 5em;
    margin: 0;
    padding: 1em;
    z-index: 10;
}

</style>