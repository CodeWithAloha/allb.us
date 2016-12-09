import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'

Vue.use(Vuex)

const state = {
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
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  plugins: []
})
