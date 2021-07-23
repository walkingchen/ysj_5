<template>
  <div class="privateMessageItem" :class="{unread: !item.read_status}">
    <p class="title">{{ item.post_title }}</p>
    <p class="content">
      {{ item.abstract }}
      <el-button size="mini" class="seeMore-btn" @click="showDetail">See More</el-button>
    </p>
    <img v-if="item.photo_uri" :src="item.photo_uri.small" class="post-photo" />
    <span class="message-time">{{ date }}</span>
    <div class="actions">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { formatDate } from '@assets/utils.js'

export default {
  props: ['item'],
  computed: {
    date () {
      return formatDate(this.item.created_at)
    }
  },
  methods: {
    showDetail () {
      this.$bus.$emit('show-post-detail', this.item.id)
    }
  }
}
</script>

<style lang="stylus" scoped>
.privateMessageItem
  position relative

  .actions
    position absolute
    bottom 10px
    right 10px
</style>
<style lang="stylus">
.privateMessageItem
  padding 10px

  p
    line-height 1.5

    &.title
      font-size 16px
      font-weight 600

    &.content
      font-size 14px
      white-space pre-wrap

      .seeMore-btn
        margin-left 5px
        padding 4px 8px

  .message-time
    color #999
    font-size 14px
    line-height 24px
    display inline-block

.movingMessage
  position absolute !important
  z-index 10
  background-color #fff
  border-radius 4px
  transition top 1s, left 1s

  .actions
    display none
</style>
