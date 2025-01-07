import { createRouter, createWebHistory } from 'vue-router';
import c1 from "../views/c1.vue";
import c2 from "../views/c2.vue";
import login from '../views/login.vue';
import register from '../views/register.vue';
import account from '../views/account.vue';
import quiz from '../views/quiz.vue';
import takeQuiz from '../views/takeQuiz.vue';
const routes = [
  {
    path: "/login",
    component : login
  },
  {
    path: "/account",
    component : account
  },
  {
    path: "/register",
    component : register
  },
  {
    path: "/quiz",
    component : quiz 
  },
  {
    path: "/c1",
    component: c1
  },
  {
    path: "/c2",
    component: c2
  },
  {
    path: '/takeQuiz/:id',
    component: takeQuiz
  }
];
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;