// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import axios from 'axios'
import Vue from 'vue'
import router from './router'
import store from './store'
import App from './App'

import TitleComponent from './components/TitleComponent'
import FavoritesComponent from './components/FavoritesComponent'
import FavoritesListComponent from './components/FavoritesListComponent'

import Raven from 'raven-js'
import RavenVue from 'raven-js/plugins/vue'

Vue.config.debug = true

axios.defaults.baseURL = 'http://localhost:8008'
Vue.prototype.$http = axios

Vue.component('page-title', TitleComponent)
Vue.component('favorites-list', FavoritesListComponent)
Vue.component('favorites-button', FavoritesComponent)

Raven.config(process.env.SENTRY_DSN).addPlugin(RavenVue, Vue).install()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  template: '<App/>',
  components: { App },
  router: router
})
