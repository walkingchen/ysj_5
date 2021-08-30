<template>
  <span v-html="_content"></span>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: ['content'],
  computed: {
    _content () {
      return this.searchKey ? (this.content ? this.content.split(this.searchKey).join(`<b class="highlight">${this.searchKey}</b>`) : '') : this.content
    },
    ...mapState(['searchKey'])
  }
}
</script>

<style lang="stylus">
.highlight
  background-color #e6a23c
</style>
