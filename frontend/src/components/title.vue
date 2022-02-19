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
  font-size 36px
  font-weight bold
  padding 15px 20px 0
</style>
