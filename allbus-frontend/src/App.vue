<template>
  <div id="app">
    <header>
      <router-link :to="{ name: 'slash'}"><img src="../static/img/icon-allbus.png" height="64" width="64" /></router-link>
    </header>
    <div id="separator"></div>
    <div class="content">
      <router-view></router-view>
    </div>
    <footer>
      <router-link :to="{ name: 'about'}">About</router-link>
    </footer>
  </div>
</template>

<style lang="scss">
@import './variables.scss';

body {
  background-color: $body-bg-color;
  margin:0 auto;
  font-size: $body-font-size;
}

#app {
  font-family: $app-font-family;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  header {
    text-align:center;
    background-color:#000;
  }

  div#separator {
    border-top:.2em solid #fff;
    border-bottom:.4em solid #FCB040;
  }

  div.content {
    padding: $content-padding;
  }

  footer {
    clear: both;
    text-align:center;
    padding: $footer-padding;
    a { text-decoration: none;}
  }
}
</style>
