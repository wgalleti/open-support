import Vue from 'vue'
import App from './App.vue'
import '@/registerServiceWorker'
import '@/plugins/devexpress'
import '@/plugins/axios'
import '@/plugins/bus'
import '@/plugins/fragment'
import '@/templates'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import '@babel/polyfill'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
import '@/assets/main.css'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
