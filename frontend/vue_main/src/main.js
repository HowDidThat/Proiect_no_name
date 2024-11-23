import Vue from 'vue'
import App from './App.vue'
import router from './router.js'
var VueCookie = require('vue-cookie');

Vue.config.productionTip = false
Vue.use(VueCookie);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
