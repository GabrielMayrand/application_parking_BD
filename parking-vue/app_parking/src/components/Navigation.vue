<template>
<nav class="navbar navigation box" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
        <router-link class="navbar-item title is-2" to="/"> Home </router-link>
    </div>
    <div class="navbar-end">
        <div class="navbar-item">
            <div class="buttons">
                <router-link  :to="{path:`/signup`}">
                <a class="button is-primary" ><strong>Sign up</strong></a>
                </router-link>
                <a class="button is-light"> Log in </a>
            </div>
        </div>
    </div>
</nav>
</template>

<script>

export default {

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