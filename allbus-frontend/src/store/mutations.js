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
    var newStop = {
      'stop_id': stopBusMap.stop.stop_id,
      'name': stopBusMap.stop.name,
      'point': {
        'x': stopBusMap.stop.longitude,
        'y': stopBusMap.stop.latitude
      }
    }
    state.stop = newStop
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
