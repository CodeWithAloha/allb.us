import Vue from 'vue'
import Router from 'vue-router'

import AboutView from '../components/AboutView'
import SlashView from '../components/SlashView'
import StopDetailsView from '../components/StopDetailsView'
import StopBusTrackerMapView from '../components/StopBusTrackerMapView'
import YellowPlacardView from '../components/YellowPlacardView'

Vue.use(Router)

export default new Router({
  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    { path: '/', name: 'slash', component: SlashView },
    { path: '/about', name: 'about', component: AboutView },
    { path: '/placard', name: 'yellowPlacard', component: YellowPlacardView },
    { path: '/:stopId', name: 'stopDetails', component: StopDetailsView },
    { path: '/:stopId/route/:routeId/bus/:busId/trip/:tripId', name: 'stopBusTrackerMap', component: StopBusTrackerMapView },
    { path: '/:stopId/route/:routeId/trip/:tripId', name: 'stopMap', component: StopBusTrackerMapView }
  ]
})
