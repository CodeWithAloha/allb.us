<template>
  <div id="placard">
    <page-title :title="$t('yellow-placard-page-title')"></page-title>
    <img src="../../static/img/placard.jpg" />
    <p v-html="$t('yellow-placard-photo-credit')"></p>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
  div#placard {
    text-align:center; 
  }
</style>
