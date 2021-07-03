<template>
  <div id="app">
    <router-view/>
  </div>
</template>

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
