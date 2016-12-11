<template>
  <div v-if="favorites.length === 0">
    <p> You have no favorite stops </p>
  </div>
  <div v-else>
    <h1>Your Favs</h1>
    <ul>
      <li v-for="(fav, index) in favorites" class="favorite">
        <router-link :to="{ name: 'stopDetails', params: { stopId: fav.stopId }}">
          Stop {{ fav.stopId }} @ {{ fav.stopName }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'favorites',
  props: {
    'favorites': {
      type: Array,
      required: true
    }
  },
  data () {
    return {
    }
  }
}
</script>

<style lang="scss" scoped>
  ul {
    list-style-type:none;
    li.favorite {
      a {
        text-decoration:none;
      } 
    }
  }
</style>
