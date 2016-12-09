// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import axios from 'axios'
import Vue from 'vue'
import router from './router'
import store from './store'
import App from './App'

import TitleComponent from './components/TitleComponent'

Vue.config.debug = true

axios.defaults.baseURL = 'http://localhost:8008'
Vue.prototype.$http = axios

Vue.component('page-title', TitleComponent)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  template: '<App/>',
  components: { App },
  router: router
})
