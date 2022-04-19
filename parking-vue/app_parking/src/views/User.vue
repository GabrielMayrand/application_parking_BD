<template>
  <div>
    <UserInfo :user="user" v-if="!isFetching"/>
    <UserTabs/>
  </div>
</template>

<script>
import UserInfo from "../components/UserComponents/UserInfo.vue";
import UserTabs from "../components/UserComponents/UserTabs.vue"
import {API} from "../utility/api.js";

export default {
    data(){
      return {
        api: new API(),
          isFetching: true,
          user: Object,
          pageId : this.$route.params.id,
      }
    },
    components: {
        UserInfo,
        UserTabs,
    },
    methods: {
      async getUser() {
        await this.api.getUserById(this.pageId);
        this.user = this.api.response[0];
        this.isFetching = false;
      },
    },
    beforeMount(){
      this.getUser();
    }
};
</script>

<style scoped>

</style>