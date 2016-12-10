import * as api from '../api'
import * as types from './mutation-types'

export function getStopDetails ({ commit }, stopId) {
  return api.getStopDetails(stopId).then((stopDetails) => {
    commit(types.GET_STOP_DETAILS, { stopDetails })
  })
}

export function getStopBusMap ({ commit }, { stopId, routeId, tripId, busId }) {
  return api.getStopBusMap(stopId, routeId, tripId, busId).then((stopBusMap) => {
    commit(types.GET_STOP_BUS_MAP, { stopBusMap })
  })
}

export function getBuses ({ commit }) {
  return api.getBuses().then((allBuses) => {
    commit(types.GET_BUSES, { allBuses })
  })
}
