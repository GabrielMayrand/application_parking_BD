import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import User from "../views/User";
import Parking from "../views/Parking"

import Login from "../views/Login"
import SignUp from "../views/SignUp"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/user/:id",
    name: "User",
    component: User,
    props: true,
  },
  {
    path: "/parking/:id",
    name: "Parking",
    component: Parking,
    props: true,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",
    component: SignUp,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
