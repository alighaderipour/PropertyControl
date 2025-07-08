// frontend/src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Login.vue";
import Dashboard from "@/views/Dashboard.vue";
import Properties from "@/views/Properties.vue";
import AddProperty from "@/views/AddProperty.vue";
import EditProperty from "@/components/EditProperty.vue";
import About from "@/views/About.vue";
import Transfers from "@/components/Transfers.vue";
import { useAuthStore } from "@/stores/auth";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/properties",
    name: "Properties",
    component: Properties,
    meta: { requiresAuth: true },
  },
    {
  path: '/departments',
  name: 'Departments',
  component: () => import('@/views/Departments.vue'),
  meta: { requiresAuth: true }
}
,
  {
    path: "/properties/add",
    name: "AddProperty",
    component: AddProperty,
    meta: { requiresAuth: true },
  },
  // ✅ Keep the more specific route BEFORE the general one
  {
    path: "/properties/:id/edit",
    name: "EditProperty",
    component: EditProperty,
    meta: { requiresAuth: true },
  },
    {
  path: '/categories',
  name: 'Categories',
  component: () => import('@/views/Categories.vue'),
  meta: { requiresAuth: true }
}
,
  // ✅ This should come after the /edit route
  {
    path: "/properties/:id",
    name: "PropertyDetail",
    component: EditProperty, // Using the same component for now
    meta: { requiresAuth: true },
  },
  {
    path: "/transfers",
    name: "Transfers",
    component: Transfers,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});

export default router;
