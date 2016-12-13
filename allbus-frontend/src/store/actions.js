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

export function getFavorites ({ commit }) {
  return api.getFavorites().then((favorites) => {
    commit(types.GET_FAVORITES, { favorites })
  })
}

export function addFavorite ({ commit, dispatch }, { stopId, stopName }) {
  return api.addFavorite(stopId, stopName).then(() => {
    commit(types.ADD_FAVORITE, { stopId, stopName })
    dispatch('getFavorites')
  })
}

export function removeFavorite ({ commit, dispatch }, stopId) {
  return api.removeFavorite(stopId).then(() => {
    commit(types.REMOVE_FAVORITE, { stopId })
    dispatch('getFavorites')
  })
}

export function setLanguage ({ commit }, { store, locale }) {
  if (store.$i18n.exists(locale)) {
    store.$i18n.set(locale)
    commit(types.SET_CURRENT_LANGUAGE, { locale })
  } else {
    return api.getLanguage(locale).then((data) => {
      store.$i18n.add(locale, data)
      store.$i18n.set(locale)
      commit(types.SET_CURRENT_LANGUAGE, { locale })
    })
  }
}
