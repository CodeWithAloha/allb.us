import Vue from 'vue'
import Vuex from 'vuex'
import vuexI18n from 'vuex-i18n'

import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'

Vue.use(Vuex)

const state = {
  favorites: [],
  stop: {
    stop_id: '',
    name: '',
    point: {
      x: '',
      y: ''
    },
    arrivals: []
  },
  route_names: [],
  route: {
    name: '',
    stops: []
  },
  trip: {
    headsign: '',
    geojson: ''
  },
  vehicle: {
  },
  buses: [],
  language_locale: '',
  current_language: 'en'
}

var store = new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  modules: { i18n: vuexI18n.store },
  plugins: []
})

Vue.use(vuexI18n.plugin, store)

export default store
