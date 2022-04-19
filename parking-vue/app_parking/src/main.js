import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "bulma/css/bulma.css";

Vue.config.productionTip = false;
Vue.prototype.$globalThis = "";

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
