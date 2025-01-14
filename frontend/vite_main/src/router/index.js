import { createRouter, createWebHistory } from 'vue-router';
import login from '../views/login.vue';
import register from '../views/register.vue';
import account from '../views/account.vue';
import quiz from '../views/quiz.vue';
import takeQuiz from '../views/takeQuiz.vue';
import home from '../views/home.vue';
const routes = [
  {
    path: "",
    component : home
  },
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
    path: '/takeQuiz/:id',
    component: takeQuiz
  }
];
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;