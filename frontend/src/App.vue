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
  font-family: 'nyt-cheltenham';
  src: url('./assets/cheltenham-italic-700.woff2') format('woff2');
  font-style: italic;
  font-weight: 700;
  font-display: swap;
}
@font-face {
  font-family: 'nyt-cheltenham';
  src: url('./assets/cheltenham-normal-300.woff2') format('woff2');
  font-style: normal;
  font-weight: 300;
  font-display: swap;
}
@font-face {
  font-display: swap;
  font-family: EconSans;
  font-style: normal;
  font-weight: 400;
  src: url('./assets/econsans-primary-subset-rg.woff2') format('woff2');
}
@font-face {
  font-display: swap;
  font-family: EconSans;
  font-style: normal;
  font-weight: 700;
  src: url(./assets/econsans-primary-subset-bd.woff2) format('woff2');
}
@font-face {
  font-display: swap;
  font-family: Milo;
  font-style: normal;
  font-weight: 400;
  src: url('./assets/milo-primary-subset-rg.woff2') format('woff2');
}
@font-face {
  font-display: swap;
  font-family: Milo;
  font-style: normal;
  font-weight: 700;
  src: url(./assets/milo-primary-subset-bd.woff2) format('woff2');
}

:root {
  --module-title-height: 62px;
}

*
  padding 0
  margin 0

#app
  color #333
  font-family Calibri, Arial, Helvetica, sans-serif

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
  font-size 26px
  font-weight bold
  padding 0 20px
  height var(--module-title-height)
  line-height var(--module-title-height)

  &.fixed
    cursor pointer
    position fixed !important
    z-index 10
    border-top-left-radius 4px
    border-top-right-radius 4px

    &:hover
      box-shadow rgba(0, 0, 0, .5) 0px 0px 10px
      z-index 11

.nyt-title
  font-size 40px
  font-weight 700
  line-height 48px
  font-family nyt-cheltenham, georgia, 'times new roman', times, serif
  margin-bottom 16px
  font-style italic

.nyt-content
  font-size 23px
  font-weight 300
  line-height 30px
  font-family nyt-cheltenham, georgia, 'times new roman', times, serif
  white-space pre-wrap
  word-break break-word

.message-title
  font-size 26px
  line-height 30px
  font-weight 700

.message-content
  font-size 16px
  font-weight 400
  line-height 1.4
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
