<template>
  <div v-if="favorited">
    <button type="button" class="rem" v-on:click="removeFavorite(currentStopId)"></button>
  </div>
  <div v-else>
    <button type="button" class="add" v-on:click="addFavorite(currentStopId, currentStopName)"></button>
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
  button {
    float:right;
    height:26px;
    width:26px;
    border:0;
  }

  .add {
    background:url('/static/img/28-star.png') no-repeat 0px 0px;
  }

  .rem {
    background:url('/static/img/28-star.png') no-repeat -26px 0px;
  }
</style>
