<template>
  <div v-if="stops && !loading">
    <page-title :title="'Bus Tracker ' + this.$route.params.busId + ' | Route ' + this.$route.params.routeId + ' | Stop ' + stop.stop_id + ' Map'" v-if="this.$route.params.busId"></page-title>
    <page-title :title="'Route ' + this.$route.params.routeId + ' | Stop ' + stop.stop_id + ' Map'" v-else></page-title>
    <h1>Stops along Route {{ this.$route.params.routeId }}</h1>
    <div id="stops">
      <ul>
        <li v-for="(s, index) in stops" class="stop">
          <router-link :to="{ name: 'stopDetails', params: { stopId: s.stop_id }}">
            <div class="current_stop_id" v-if="s.stop_id == stop.stop_id">{{ s.stop_id }}</div>
            <div class="stop_id" v-else>{{ s.stop_id }}</div>
            <div class="stop_name">{{ s.name }}</div>
          </router-link>
        </li>
      </ul>
    </div>
    <div id="map"></div>
  </div>
  <div v-else-if="loading">
    <p> Loading Stops along Route {{ this.$route.params.routeId }}</p>
    <div id="map"></div>
  </div>
</template>

<style src="../../static/leaflet/leaflet.css"></style>

<script>
import L from 'leaflet'
import 'leaflet-polylinedecorator'

export default {
  name: 'stop-bus-tracker-map',
  data () {
    return {
      loading: true,
      map: null,
      markers: []
    }
  },
  computed: {
    stop () {
      return this.$store.state.stop
    },
    stops () {
      return this.$store.state.route.stops
    }
  },
  methods: {
    initializeMap (latitude, longitude, geojson) {
      var vm = this
      return new Promise(function (resolve, reject) {
        vm.map = L.map('map')
        vm.map.setView(L.latLng(latitude, longitude), 16)
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
          attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
          maxZoom: 18
        }).addTo(vm.map)

        var geoJsonStyle = {
          'color': '#ff7800',
          'weight': 2,
          'opacity': 0.6
        }
        L.geoJson(geojson, { style: geoJsonStyle }).addTo(vm.map)

        /* eslint-disable */
        var latlngs = L.GeoJSON.coordsToLatLngs(geojson['coordinates'], 0)
        /* eslint-enable */

        var arrows = L.polyline(latlngs, {})
        L.polylineDecorator(arrows, {
          patterns: [{
            repeat: 100,
            symbol: L.Symbol.arrowHead({pixelSize: 12, pathOptions: {color: '#000', fillOpacity: 0.7, weight: 0}})}
          ]}).addTo(vm.map)

        resolve()
      })
    },
    createStopMarker (markers, stopId, stopUrl, latlng) {
      var vm = this
      var iconPointX = stopId.toString().length * 8
      var ele = document.createElement('a')
      var linkText = document.createTextNode(stopId)
      ele.appendChild(linkText)
      ele.href = '#'
      ele.id = stopId
      ele.class = 'stop-link'
      var iconHtml = ele.outerHTML
      var iconClassName = (stopId === this.stop.stop_id) ? 'current-stop-icon' : 'stop-icon'
      var divIcon = L.divIcon({className: iconClassName, iconSize: new L.Point(iconPointX, 18), html: iconHtml})
      var markerOptions = { icon: divIcon }
      var marker = L.marker(latlng, markerOptions)
      marker.addTo(this.map).on('click', function (e) {
        vm.$router.push({name: 'stopDetails', params: {stopId: e.target._icon.firstChild.id}})
      })
      markers.push(marker)
    },
    createVehicleMarker (latlng) {
      var busIcon = L.icon({
        iconUrl: '/static/img/maps/bus.png',
        shadowUrl: '/static/img/maps/bus-shadow.png',
        iconSize: [48, 40], // size of the icon
        shadowSize: [48, 40], // size of the shadow
        iconAnchor: [13, 40], // point of the icon which will correspond to marker's location
        shadowAnchor: [13, 40]  // the same for the shadow
      })
      L.marker(latlng, {icon: busIcon}).addTo(this.map)
    }
  },
  beforeMount () {
    var vm = this
    this.$store.dispatch('getStopBusMap', { stopId: vm.$route.params.stopId, routeId: vm.$route.params.routeId, tripId: vm.$route.params.tripId, busId: vm.$route.params.busId }).then(() => {
      vm.loading = false
      this.initializeMap(vm.$store.state.stop.point.y, vm.$store.state.stop.point.x, vm.$store.state.trip.geojson).then(function (response) {
        vm.createStopMarker(vm.markers, vm.$store.state.stop.stop_id, '', new L.LatLng(vm.$store.state.stop.point.y, vm.$store.state.stop.point.x))
        for (var i = 0; i < vm.$store.state.route.stops.length; i++) {
          vm.createStopMarker(vm.markers, vm.$store.state.route.stops[i].stop_id, '', new L.LatLng(vm.$store.state.route.stops[i].point.y, vm.$store.state.route.stops[i].point.x))
        }

        if (vm.$store.state.vehicle) {
          vm.createVehicleMarker(new L.LatLng(vm.$store.state.vehicle.latitude, vm.$store.state.vehicle.longitude))
          var bounds = []
          bounds.push(new L.LatLng(vm.$store.state.stop.point.y, vm.$store.state.stop.point.x))
          bounds.push(new L.LatLng(vm.$store.state.vehicle.latitude, vm.$store.state.vehicle.longitude))
          vm.map.fitBounds(bounds)
        }
      })
    })
  }
}
</script>

<style lang="scss">
  div#stops {
    float:left;
    text-align:left;
    ul {
      margin:0;
      padding:0;
      list-style:none;
      a { text-decoration:none; color: #000; }
      li.stop {
        border-bottom:1px solid #ddd;
        div.stop_id, div.current_stop_id { 
          text-align:center;
          display:inline-block;
          font-weight:bold; 
          font-size:2em;
          width:3em;
          background-color: #ffd9a1; 
        }
        div.current_stop_id {
          background-color: #FCB040; 
        }
        div.stop_name {
          margin-left:1em;
          font-size:1.25em;
          display:inline-block;
          color: #000;
        }
      }
    }
  }

  div#map {
    float:left;
    margin-left:2em;
    width: 1074px;
    height: 768px;
  }

  div.stop-icon, div.current-stop-icon {
    background-color: #ffd9a1;
    border:1px solid #000;
    text-align:center;
  }
  div.current-stop-icon {
    background-color: #FCB040;
  }

</style>
