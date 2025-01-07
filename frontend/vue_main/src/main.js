import { createApp } from 'vue'
import App from './App.vue'
import app_router from '../src/router'

const app = createApp(App)
app.use(app_router)
app.mount('#app')

