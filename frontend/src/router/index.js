import { createRouter, createWebHashHistory } from "vue-router";


// 在createRouter中需要导入页面的相关信息
const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/home/HomeView.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/login/LoginView.vue"),
  },
  {
    path: "/manager",
    name: "Manager",
    component: () => import("../views/manager_panel/PanelView.vue"),
  },
  {
    path: "/ac",
    name: "AC",
    component: () => import("../views/ac_panel/ACView.vue"),
  },
  {
    path: "/componentDemo",
    name: "ComponentDemo",
    component: () => import("../views/error/404.vue"),
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;