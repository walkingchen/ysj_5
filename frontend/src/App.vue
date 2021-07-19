<template>
  <div id="app">
    <Phone v-if="isMobile" />
    <router-view v-else />
  </div>
</template>

<script>
import Phone from './views/Phone'

export default {
  components: {
    Phone
  },
  computed: {
    isMobile () {
      const ua = navigator.userAgent
      const isAndroid = /(?:Android)/.test(ua)
      const isTablet = /(?:iPad|PlayBook)/.test(ua) || (isAndroid && !/(?:Mobile)/.test(ua)) || (/(?:Firefox)/.test(ua) && /(?:Tablet)/.test(ua))
      const isIOS = /(?:iPhone)/.test(ua) && !isTablet
      return isAndroid || isIOS
    }
  }
}
</script>

<style lang="stylus">
*
  padding 0
  margin 0

#app
  color #333

  .el-card__body
    padding 0

button
  cursor pointer
  border 0
  background-color transparent
  outline none

ul, li
  list-style none

.layout
  width 90%
  min-width 1200px
  margin 0 auto
</style>
