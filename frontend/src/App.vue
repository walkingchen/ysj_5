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
@font-face {
  font-display: swap;
  font-family: Georgia;
  font-style: normal;
  font-weight: 400;
  src: url('./assets/georgia-normal.ttf');
}
@font-face {
  font-display: swap;
  font-family: Georgia;
  font-style: normal;
  font-weight: 700;
  src: url('./assets/georgia-bold.ttf');
}
@font-face {
  font-display: swap;
  font-family: Apple;
  font-style: normal;
  src: url('./assets/apple.ttf');
}

:root {
  --module-title-height: 62px;
}

*
  padding 0
  margin 0

#app
  color #333
  font-family Apple, Calibri, Arial, Helvetica, sans-serif

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

.fa-icon
  width auto

.module-title
  font-size 20px
  font-weight bold
  padding 0 20px
  height var(--module-title-height)
  line-height var(--module-title-height)
  text-overflow ellipsis
  overflow hidden
  white-space nowrap

  &.fixed
    cursor pointer
    position fixed !important
    z-index 10
    border-top-left-radius 4px
    border-top-right-radius 4px

    &:hover
      box-shadow rgba(0, 0, 0, .5) 0px 0px 10px
      z-index 11

.serif-font
  font-family Georgia, 'times new roman', times, serif

.message-title
  font-size 24px
  line-height 30px
  font-weight 700

.message-content
  font-size 16px
  font-weight 400
  line-height 20px
  white-space pre-wrap

.seeMore-btn
  margin-left 10px
  color #409eff
  text-decoration underline
  cursor pointer

  &:hover
    color #66b1ff

.loading-layout
  text-align center
  font-size 20px
  color #409eff

.nomore-layout
  text-align center
  padding 10px 0
</style>
