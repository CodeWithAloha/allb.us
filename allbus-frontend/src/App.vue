<template>
  <div id="app">
    <header>
      <router-link :to="{ name: 'slash'}"><img src="../static/img/icon-allbus.png" height="64" width="64" /></router-link>
      <button type="submit" @click="setLanguage(getOtherLanguage())">Set language</button>
    </header>
    <div id="separator"></div>
    <div class="content">
      <router-view></router-view>
    </div>
    <footer>
      <a href="http://thebus.org" rel="external nofollow" target="_blank">thebus</a> · <a href="tel:8088485555">(808) 848-5555</a> · <router-link :to="{ name: 'about'}">{{ $t('footer-about') }}</router-link>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
    }
  },
  computed: {
  },
  methods: {
    getOtherLanguage () {
      if (this.$store.getters.getCurrentLanguage === 'en') {
        return 'ja'
      } else {
        return 'en'
      }
    },
    setLanguage (language) {
      this.$store.dispatch('setLanguage', {'store': this, 'locale': language})
    }
  },
  beforeMount () {
    this.setLanguage(this.$store.getters.getCurrentLanguage)
  }
}
</script>

<style lang="scss">
@import './variables.scss';

html {
  height: 100%;
}

body {
  background-color: $body-bg-color;
  margin:0 auto;
  font-size: $body-font-size;
  min-height: 100%;
  display: flex;
  display: -webkit-flex;
  flex-direction: column;
}

#app {
  font-family: $app-font-family;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  header {
    text-align:center;
    background-color:#000;
    button {
      position:absolute;
      right:0;
    }
  }

  div#separator {
    border-top:.2em solid #fff;
    border-bottom:.4em solid #FCB040;
  }

  div.content {
    padding: $content-padding;
    flex: 1;
  }

  footer {
    clear: both;
    text-align:center;
    padding: $footer-padding;
    a { text-decoration: none;}
  }
}
</style>
