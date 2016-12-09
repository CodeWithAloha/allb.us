<template>
  <div>
    <page-title title="All Bus"></page-title>
    <input id="stop_or_street" name="stop_or_street" placeholder="Enter stop (e.g. 125) or street" type="text" @keydown.enter.prevent="searchStops">
    <p>
      Every Honolulu bus stop has a <router-link :to="{ name: 'yellowPlacard'}">yellow placard</router-link> that contains a unique stop number. Please enter the number above. If you can't find the placard, feel free to enter your cross street, e.g. Punchbowl and King. 
    </p>
    <p>
      If you don't know the stop number or cross streets and have a GPS-enabled phone, click here, and we'll do our best to find the closest bus stop near you. 
    </p>
  </div>
</template>

<script>
export default {
  name: 'slash',
  data () {
    return {
    }
  },
  methods: {
    searchStops (e) {
      if (/\d+/.test(e.target.value)) {
        this.$router.push({name: 'stopDetails', params: {stopId: e.target.value}})
      }
    }
  }
}
</script>

<style scoped>

input#stop_or_street {
  font-size:1em;
  padding:.5em;
  width: 100%;
  -webkit-box-sizing: border-box; /* Safari/Chrome, other WebKit */
  -moz-box-sizing: border-box;    /* Firefox, other Gecko */
  box-sizing: border-box;
}

div {
  font-size:1.4em;
}

</style>
