<template>
  <div class="title-box">
    <h2>{{ title }}</h2>
    <i></i>
    <i></i>
  </div>
</template>

<script>
export default {
  props: ['title']
}
</script>

<style lang="stylus" scoped>
$height = 40px
$bgcolor = rgb(217, 236, 255)

.title-box
  height $height

  h2
    height $height
    float left
    line-height $height
    padding-left 15px
    font-size 18px
    color #409EFF
    position relative
    z-index 2
    margin-left 12px
    padding 0 20px

    &::before
      content ''
      position absolute
      top 0
      right 0
      bottom 0
      left 0
      z-index -1
      background-color $bgcolor
      transform skew(-30deg)

  i
    float left
    width 10px
    height $height
    transform skew(-30deg)
    margin-left 8px
    background-color $bgcolor
</style>
