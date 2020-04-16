<template>
  <el-card shadow="hover" class="systemMessages-layout">
    <title-com title="Personalized Message Stream" />
    <ul>
      <li v-if="messages.length === 0">No messages.</li>
      <li v-for="item in messages" :key="item.id">
        <p class="title">{{ item.post_title }}</p>
        <p>{{ item.post_content }}</p>
        <div>
          <span class="message-time">{{ item.created_at }}</span>
          <button class="share-btn" @click="share(item.id)"><v-icon name="share" /></button>
        </div>
      </li>
    </ul>
  </el-card>
</template>

<script>
import 'vue-awesome/icons/share'
import titleCom from '@components/title'
import { getPosts, sharePost } from '@api/post'
import { formatDate } from '@assets/utils.js'

export default {
  data() {
    return {
      messages: []
    }
  },
  components: {
    titleCom
  },
  created() {
    getPosts({
      room_id: localStorage.getItem('roomid'),
      timeline_type: 1,
      pull_new: 1
    }).then(res => {
      this.messages = res.data.data.map(item => {
        item.created_at = formatDate(item.created_at)
        return item
      })
    })
  },
  methods: {
    share(id) {
      sharePost(id).then(() => {
        this.$emit('share-success', id)
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.systemMessages-layout
  border 0

  ul
    padding 10px

  li
    padding 10px
    border-bottom 1px solid #e4e7ed

    &:last-child
      border-bottom 0

  p
    line-height 1.5

    &.title
      font-size 16px

  .message-time
    color #999
    font-size 14px
    line-height 24px
    display inline-block

  .share-btn
    float right
    margin-left 10px
    padding 0 8px
    height 24px
    color #909399

    &:hover
      color #409eff
</style>
