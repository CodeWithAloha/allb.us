import * as types from './mutation-types'

export default {
  [types.GET_STOP_DETAILS] (state, { stopDetails }) {
    var newStop = {
      'stop_id': stopDetails.stop.stop_id,
      'name': stopDetails.stop.name,
      'arrivals': stopDetails.arrivals,
      'route_names': stopDetails.route_names
    }
    state.stop = newStop
  },
  [types.GET_STOP_BUS_MAP] (state, { stopBusMap }) {
    state.stop.stop_id = stopBusMap.stop.stop_id
    state.stop.name = stopBusMap.stop.name
    state.stop.point.x = stopBusMap.stop.longitude
    state.stop.point.y = stopBusMap.stop.latitude
    state.route.stops = stopBusMap.stops
    state.trip = stopBusMap.trip
    state.vehicle = stopBusMap.vehicle
  },
  [types.GET_BUSES] (state, { allBuses }) {
    state.buses = allBuses
  },
  [types.GET_FAVORITES] (state, { favorites }) {
    state.favorites = favorites
  },
  [types.ADD_FAVORITE] (state, { favorite }) {
  },
  [types.REMOVE_FAVORITE] (state, { stopId }) {
  },
  [types.SET_CURRENT_LANGUAGE] (state, { locale }) {
    state.current_language = locale
  }
}
