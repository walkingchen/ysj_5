import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Icon from 'vue-awesome/components/Icon'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'

locale.use(lang)

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.component('v-icon', Icon)

Vue.prototype.$bus = new Vue()

axios.defaults.baseURL = '/api'
axios.interceptors.response.use(res => {
  if (res.data.result_code === 4001) {
    router.push({ name: 'Login' })
  }
  return res
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
