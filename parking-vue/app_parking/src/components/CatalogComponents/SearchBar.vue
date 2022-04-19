<template>
    <div id="wrapper">
        <input class="input " type="text" id="SearchBar" placeholder="Search an address">
        <button class="button is-primary " id="SearchButton">Search</button>
        <button class="button is-primary " id="Filters" @click="this.$root.$ref.Filters.filterToggleClicked()">Filters</button>
    </div>
    
</template>
<style scoped>
#SearchBar {
    margin: 10px;
    padding: 10px;
    max-width: 300px;
}
#wrapper {
    display: flex;
    flex-direction: row;
}
.button {
    margin: 10px;
    padding: 10px;
}
</style>