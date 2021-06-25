<template>
  <h2>{{ title }}</h2>
</template>

<script>
export default {
  props: ['title']
}
</script>

<style lang="stylus" scoped>
h2
  height 40px
  font-size 18px
  font-weight bold
  padding 10px 20px 0
</style>
