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

export function getFavorites () {
  return new Promise(function (resolve, reject) {
    return resolve(JSON.parse(window.localStorage.getItem('favorites') || '[]'))
  })
}

export function addFavorite (stopId, stopName) {
  return new Promise(function (resolve, reject) {
    var favorites = JSON.parse(window.localStorage.getItem('favorites') || '[]')
    var favorite = {'stopId': stopId, 'stopName': stopName}
    favorites.push(favorite)
    window.localStorage.setItem('favorites', JSON.stringify(favorites))
    return resolve(favorite)
  })
}

export function removeFavorite (stopId) {
  return new Promise(function (resolve, reject) {
    var favorites = JSON.parse(window.localStorage.getItem('favorites') || '[]')
    var favoritesFiltered = (favorites) ? favorites.filter(function (el) {
      return el.stopId !== stopId
    }) : []
    window.localStorage.setItem('favorites', JSON.stringify(favoritesFiltered))
    return resolve(stopId)
  })
}
