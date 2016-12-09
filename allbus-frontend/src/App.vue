<template>
  <div id="app">
    <header>
      <h1>
        <router-link :to="{ name: 'slash'}"><img src="../static/img/icon-allbus.png" height="64" width="64" /></router-link>
      </h1>
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
    h1 {
      margin: 0 auto;
      padding: 0;
      a { border:0; margin:0; padding:0; display:inline-block;}
    }
  }

  div#separator {
    border-top:.2em solid #fff;
    border-bottom:.4em solid #FCB040;
  }

  div.content {
    padding: 1em;
  }

  footer {
    clear: both;
    text-align:center;
    padding:1em;
    a { text-decoration: none;}
  }
}
</style>
