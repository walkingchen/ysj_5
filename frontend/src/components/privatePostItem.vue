<template>
  <div class="privateMessageItem" :class="{unread: !item.read_status}">
    <div v-if="item.photo_uri" class="privateMessage-titleWithImage">
      <img :src="item.photo_uri.small" class="post-photo" />
      <p class="message-title">
        <highlight :content="item.post_title" />
      </p>
    </div>
    <p v-else class="message-title">
      <highlight :content="item.post_title" />
    </p>
    <p class="message-content">
      <highlight :content="item.abstract" />
      <span class="seeMore-btn" @click="showDetail">See more</span>
    </p>
    <!-- <span class="message-time">{{ date }}</span>
    <div class="actions">
      <slot name="actions"></slot>
    </div> -->
    <slot></slot>
  </div>
</template>

<script>
import highlight from './highlight'
import { formatDate } from '@assets/utils.js'
import { getPrivatePostDetail } from '@api/post'

export default {
  props: ['item'],
  components: {
    highlight
  },
  computed: {
    date () {
      return formatDate(this.item.created_at)
    }
  },
  methods: {
    showDetail () {
      this.$bus.$emit('show-post-detail')
      this.$store.commit('setGetPostDetailLoading', true)
      getPrivatePostDetail(this.item.id).then(({ data }) => {
        this.$store.commit('setGetPostDetailLoading', false)
        const detailData = data.data
        Object.assign(detailData, {
          created_at: formatDate(data.data.created_at)
        })
        this.$store.commit('setPostDetail', detailData)
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.privateMessageItem
  position relative
  overflow hidden

  .actions
    position absolute
    bottom 10px
    right 10px
</style>
<style lang="stylus">
.privateMessageItem
  border-radius 4px
  padding 10px
  background-color #fff

  .message-title,
  .message-content
    font-family Milo

  // .message-time
  //   color #999
  //   font-size 14px
  //   line-height 24px
  //   display inline-block

.privateMessage-titleWithImage
  position relative

  .message-title
    position absolute
    bottom 0
    width 100%
    color #fff

.movingMessage
  position absolute !important
  z-index 10
  background-color #fff
  border-radius 4px
  transition top 1s, left 1s

  .actions
    display none
</style>
