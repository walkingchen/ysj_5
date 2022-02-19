<template>
  <i :style="{ 'font-size': size + 'px', color }">
    <svg class="icon" aria-hidden="true">
      <use :xlink:href="'#icon-' + name"></use>
    </svg>
  </i>
</template>

<script>
import '@/assets/icon.js'

export default {
  props: {
    name: {
      type: String,
      required: true
    },
    size: {
      type: Number,
      default: 14
    },
    color: {
      type: String,
      default: 'inherit'
    }
  }
}
</script>

<style lang="stylus" scoped>
.icon
  width 1em
  height 1em
  vertical-align -0.2em
  fill currentColor
  overflow hidden
</style>
