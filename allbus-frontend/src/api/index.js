import axios from 'axios'

export function getStopDetails (stopId) {
  return axios.get('/' + stopId)
    .then(function (response) {
      return response.data
    })
    .catch(function (error) {
      console.log(error)
      return {
        stop: {
          stop_id: stopId,
          name: '',
          arrivals: []
        },
        routes: []
      }
    })
}

export function getStopBusMap (stopId, routeId, tripId, busId) {
  var url = (busId) ? '/' + stopId + ':' + routeId + '/bus/' + busId + '/trip/' + tripId : '/' + stopId + ':' + routeId + '/trip/' + tripId
  return axios.get(url)
    .then(function (response) {
      return response.data
    })
    .catch(function (error) {
      console.log(error)
      return {}
    })
}

export function getBuses () {
  return axios.get('/buses')
    .then(function (response) {
      return response.data
    })
    .catch(function (error) {
      console.log(error)
      return {}
    })
}
