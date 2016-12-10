import * as types from './mutation-types'

export default {
  [types.GET_STOP_DETAILS] (state, { stopDetails }) {
    state.stop.stop_id = stopDetails.stop.stop_id
    state.stop.name = stopDetails.stop.name
    state.stop.arrivals = stopDetails.arrivals
    state.stop.route_names = stopDetails.route_names
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
  }
}
