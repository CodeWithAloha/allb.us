<template>
  <div v-if="buses && !loading">
    <h1>All Bus(es)</h1>
    <div id="map"></div>
  </div>
  <div v-else-if="loading">
    <p>Finding ze Buses</p>
    <div id="map"></div>
  </div>
</template>

<style src="../../static/leaflet/leaflet.css"></style>

<script>
import L from 'leaflet'
import 'leaflet-polylinedecorator'

export default {
  name: 'all-bus',
  metaInfo: {
    title: 'All Bus(es) | All Bus',
    meta: [
      { name: 'description', content: 'All Bus(es)' }
    ]
  },
  data () {
    return {
      loading: true,
      map: null,
      markers: []
    }
  },
  computed: {
    buses () {
      return this.$store.state.buses
    }
  },
  methods: {
    initializeMap (latitude, longitude) {
      var vm = this
      return new Promise(function (resolve, reject) {
        vm.map = L.map('map')
        vm.map.setView(L.latLng(latitude, longitude), 16)
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
          attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
          maxZoom: 18
        }).addTo(vm.map)
        resolve()
      })
    },
    createVehicleMarker (routeId, latlng) {
      var busIcon = L.icon({
        iconUrl: '/static/img/maps/bus.png',
        shadowUrl: '/static/img/maps/bus-shadow.png',
        iconSize: [48, 40], // size of the icon
        shadowSize: [48, 40], // size of the shadow
        iconAnchor: [13, 40], // point of the icon which will correspond to marker's location
        shadowAnchor: [13, 40]  // the same for the shadow
      })

      L.marker(latlng, {icon: busIcon}).bindTooltip(routeId, {permanent: true, direction: 'top', offset: L.point(5, -32), className: 'route-tooltip'}).addTo(this.map)
    }
  },
  beforeMount () {
    var vm = this
    this.$store.dispatch('getBuses').then(() => {
      vm.loading = false
      var randoBus = vm.$store.state.buses[0]
      this.initializeMap(randoBus.latitude, randoBus.longitude).then(function (response) {
        for (var i = 0; i < vm.$store.state.buses.length; i++) {
          var bus = vm.$store.state.buses[i]
          vm.createVehicleMarker(vm.$route.params.routeId, new L.LatLng(bus.latitude, bus.longitude))
        }
      })
    })
  }
}
</script>

<style lang="scss" scoped>

  div#map {
    width: 1074px;
    height: 768px;
  }

  .route-tooltip {
    border:0;
    background-color: #FCB040;
    color:#000;
    padding:0;
    width:28px;
    text-align:center;
    font-weight:bold;
  }

  .leaflet-tooltip-top {
    padding:0;
  }
  .leaflet-tooltip-top::before {
    content: none;
  }

</style>
