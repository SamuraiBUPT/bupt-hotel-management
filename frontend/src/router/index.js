import { createRouter, createWebHashHistory } from "vue-router";
import store from "../store";

// 在createRouter中需要导入页面的相关信息
const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/home/HomeView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/login/LoginView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: "/manager",
    name: "Manager",
    component: () => import("../views/manager_panel/PanelView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/ac",
    name: "AC",
    component: () => import("../views/ac_panel/ACView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/componentDemo",
    name: "ComponentDemo",
    component: () => import("../views/error/404.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/client",
    name: "Client",
    component: () => import("../views/client_panel/client_panel.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/ac_panel",
    name: "AC_Panel",
    component: () => import("../views/air_mana_panel/air_mana_panel.vue"),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn && !localStorage.getItem('user')) {
      // 如果用户未登录，重定向到登录页面
      next({ path: '/login',
            query: { redirect: to.fullPath } });
    } else {
      // 如果用户已登录，允许访问
      next();
    }
  } else {
    // 如果路由不需要认证，直接前往
    next();
  }
});

export default router;