import Vue from 'vue'
import Router from 'vue-router'
import HomeTemp from './components/HomeTemp.vue'
import LoginTemplate from './components/LoginTemplate.vue'
import RegisterTemplate from './components/RegisterTemplate.vue'
import ProfileTemplate from './components/ProfileTemplate.vue'
import QuizTemplate from './components/QuizTemplate.vue'
import PlaygroundTemp from './components/playground.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes:[
        {path: '/login', component: LoginTemplate},
        {path: '/register', component: RegisterTemplate},
        {path: '/profile', component: ProfileTemplate},
        {path: '/quiz', component: QuizTemplate},
        {path: '/playground', component: PlaygroundTemp},
        {path: '*', component: HomeTemp}
    ]
})