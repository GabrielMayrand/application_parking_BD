<template>
  <div>
    <UserInfo/>
    <UserTabs/>
  </div>
</template>

<script>
import UserInfo from "../components/UserComponents/UserInfo.vue";
import UserTabs from "../components/UserComponents/UserTabs.vue"

export default {
    components: {
        UserInfo,
        UserTabs,
    },
};
</script>

<style scoped>

</style>