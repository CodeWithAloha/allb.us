<template>
  <div v-if="favorited">
    <button type="button" v-on:click="removeFavorite(currentStopId)">Remove Favorite</button>
  </div>
  <div v-else>
    <button type="button" v-on:click="addFavorite(currentStopId, currentStopName)">Add Favorite</button>
  </div>
</template>

<script>
export default {
  name: 'favorites-button',
  props: {
    'favorites': {
      type: Array,
      required: true
    },
    'currentStopId': {
      type: Number,
      required: true
    },
    'currentStopName': {
      type: String,
      required: true
    }
  },
  data () {
    return {
    }
  },
  computed: {
    favorited () {
      return this.isFavorited()
    }
  },
  methods: {
    isFavorited () {
      for (var i = 0; i < this.favorites.length; i++) {
        var fav = this.favorites[i]
        if (this.currentStopId === fav.stopId) {
          return true
        }
      }
      return false
    },
    addFavorite (stopId, stopName) {
      this.$store.dispatch('addFavorite', { stopId: stopId, stopName: stopName }).then(() => {
        this.$emit('favorite-updated')
      })
    },
    removeFavorite (stopId) {
      this.$store.dispatch('removeFavorite', stopId).then(() => {
        this.$emit('favorite-updated')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
