<template>
  <div id="placard">
    <img src="../../static/img/placard.jpg" />
    <p v-html="$t('yellow-placard-photo-credit')"></p>
  </div>
</template>

<script>
export default {
  name: 'yellow-placard',
  metaInfo: {
    // title: "$t('yellow-placard-page-title')",
    title: 'Hello World',
    meta: [
      { name: 'description', content: 'Yellow Placard' }
    ]
  }
}
</script>

<style lang="scss" scoped>
  div#placard {
    text-align:center; 
  }
</style>
