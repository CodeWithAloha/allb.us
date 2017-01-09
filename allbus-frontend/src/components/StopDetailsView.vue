<template>
  <div v-if="stop.name && !loading">
    <div id="stop">
      <h1>
        Stop {{ stop.stop_id }} @ {{ stop.name }}
      </h1>
      <favorites-button :favorites="favorites" :currentStopId="parseInt(stop.stop_id)" :currentStopName="stop.name" v-on:favorite-updated="updateFavorites"></favorites-button>
    </div>
    <ul id="routes">
      <li v-for="(route_name, index) in sortedRouteNames" class="route">
        {{ route_name }}
      </li>
    </ul>
    <ul id="arrivals">
      <li v-for="(arrival, index) in stop.arrivals" class="arrival">
      <template v-if="arrival.vehicle !== '???'">
        <router-link :to="{ name: 'stopBusTrackerMap', params: { stopId: stop.stop_id, routeId: arrival.route, busId: arrival.vehicle, tripId: arrival.trip }}">
          <div class="route">
            <div class="route_number_small" v-if="arrival.route.length > 2">{{arrival.route}}</div>
            <div class="route_number" v-else>{{arrival.route}}</div>
            <div class="bus" v-if="arrival.vehicle === '???'">No GPS</div>
            <div class="bus" v-else>Bus {{ arrival.vehicle}}</div>
          </div>
          <div class="info">
            <p class="headsign">{{ arrival.headsign }}</p>
            <p class="arrival_time">{{ arrival.stopTime }}</p>
          </div>
        </router-link>
      </template>
      <template v-else>
        <router-link :to="{ name: 'stopMap', params: { stopId: stop.stop_id, routeId: arrival.route, tripId: arrival.trip }}">
          <div class="route">
            <div class="route_number_small" v-if="arrival.route.length > 2">{{arrival.route}}</div>
            <div class="route_number" v-else>{{arrival.route}}</div>
            <div class="bus" v-if="arrival.vehicle === '???'">No GPS</div>
            <div class="bus" v-else>Bus {{ arrival.vehicle}}</div>
          </div>
          <div class="info">
            <p class="headsign">{{ arrival.headsign }}</p>
            <p class="arrival_time">{{ arrival.stopTime }}</p>
          </div>
        </router-link>
      </template>
      </li>
    </ul>
  </div>
  <div v-else-if="!loading">
    <p> Unable to find Stop {{ this.$route.params.stopId }}. Please try again! </p>
  </div>
  <div v-else-if="loading">
    <p> Loading Stop {{ this.$route.params.stopId }}</p>
  </div>
</template>

<script>
export default {
  name: 'stop-details',
  metaInfo () {
    return {
      title: 'Stop ' + this.stop.stop_id + ' @ ' + this.stop.name,
      meta: [
        { name: 'description', content: 'Stop Details' }
      ]
    }
  },
  data () {
    return {
      loading: true,
      favorites: this.$store.state.favorites
    }
  },
  computed: {
    stop () {
      return this.$store.state.stop
    },
    sortedRouteNames () {
      return this.$store.getters.sortedRouteNames
    }
  },
  methods: {
    updateFavorites () {
      this.favorites = this.$store.state.favorites
    }
  },
  beforeMount () {
    this.$store.dispatch('getStopDetails', this.$route.params.stopId).then(() => {
      this.loading = false
    })
  },
  watch: {
    '$route' (to, from) {
      if (to.params.stopId !== from.params.stopId) {
        this.loading = true
        this.$store.dispatch('getStopDetails', to.params.stopId).then(() => {
          this.loading = false
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  div#stop {
    h1 {
      margin:0;
      padding:0;
      font-weight:bold;
      font-size:2em;
      display:inline;
      float:left;
    }
    button {
      float:right;
    }
    overflow: auto;
    width: 100%;
    border-bottom:1px solid black;
  }
  ul#routes {
    margin:0;
    padding:.6em 0;
    list-style:none;
    border-bottom:1px solid black;
    font-size:1.5em;
    li {
      padding:0;
      padding-right:1em;
      display:inline-block;
    }
  }
  ul#arrivals {
    margin:0;
    padding:0;
    list-style:none;
    li.arrival {
      a { text-decoration:none; color:#000;}
      border-bottom:1px solid #ddd;
      div.route {
        display:inline-block;
        .route_number { font-size:3em; font-weight:bold; }
        .route_number_small { font-size:2em; font-weight:bold; }
        .bus { font-size:1em; color:#555;}
        width:4em;
      }
      div.info {
        overflow:hidden;
        vertical-align:top;
        padding-top:1em;
        margin-left: 1em;
        display:inline-block;
        p {
          margin:0 auto;
          padding:0 auto;
          &.headsign { font-weight:bold; font-size:1.6em;}
          &.arrival_time { background-color:#eee; display:inline; padding:.25em;} 
        }
      }
    }
  }
</style>
