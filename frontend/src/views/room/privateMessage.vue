<template>
  <el-card shadow="hover" class="privateMessage-layout">
    <title-com title="Private Message Feed" />

    <el-alert v-show="newCount > 0" type="info" center :closable="false" class="new-tip">
      <span slot="title">{{ newCount }} new messages, click <a href="javascript:;" @click="getNews">here</a> to update.</span>
    </el-alert>

    <div class="loading-layout" v-show="getNewPostLoading"><i class="el-icon-loading"></i></div>

    <div class="messages">
      <div class="privateMessageItem" v-if="messages.length === 0">No messages.</div>
      <div v-for="(item, index) in messages" :key="item.id" class="privateMessageItem" ref="messageItem">
        <p class="title">{{ item.post_title }}</p>
        <p>{{ item.post_content }}</p>
        <div>
          <span class="message-time">{{ item.created_at }}</span>
          <button class="share-btn" @click="share(item.id, index)"><v-icon name="share" /></button>
        </div>
      </div>
    </div>

    <div class="get-more-btn" v-show="!getPostLoading && !noMoreData">
      <el-button type="text" @click="getMessageList">see more</el-button>
    </div>

    <div class="loading-layout" v-show="getPostLoading"><i class="el-icon-loading"></i></div>

    <div class="nomore-layout" v-show="noMoreData">No more~</div>
  </el-card>
</template>

<script>
import 'vue-awesome/icons/share'
import titleCom from '@components/title'
import { getPosts, sharePost } from '@api/post'
import { formatDate } from '@assets/utils.js'

export default {
  props: ['sid'],
  data() {
    return {
      getPostLoading: true,
      messages: [],
      newCount: 0,
      getNewPostLoading: false,
      noMoreData: false
    }
  },
  components: {
    titleCom
  },
  created() {
    this.getMessageList()
  },
  methods: {
    async getMessageList() {
      this.getPostLoading = true
      getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 1,
        pull_new: 1,
        last_update: this.messages.length === 0 ? null : this.messages[this.messages.length - 1].created_at
      }).then(res => {
        if (res.data.data.length === 0) {
          this.noMoreData = true
        }

        this.messages.push(
          ...res.data.data.map(item => {
            item.created_at = formatDate(item.created_at)
            return item
          })
        )
      })
      this.getPostLoading = false
    },
    share(id, index) {
      const ele = this.$refs.messageItem[index]
      const cloneEle = ele.cloneNode(true)
      cloneEle.classList.add('movingMessage')
      cloneEle.style.top = ele.getBoundingClientRect().top + 'px'
      cloneEle.style.left = ele.getBoundingClientRect().left + 'px'
      document.body.appendChild(cloneEle)

      sharePost(id, this.sid).then(() => {
        this.$bus.$emit('share-success', id)
        const targetTop = document.getElementById('moments-ul').getBoundingClientRect().top
        const targetLeft = document.getElementById('moments-ul').getBoundingClientRect().left
        cloneEle.style.top = targetTop + 'px'
        cloneEle.style.left = targetLeft + 'px'

        this.$bus.$on('share-success-refresh', _id => {
          if (_id === id) {
            setTimeout(() => {
              cloneEle.remove()
            }, 1000)
          }
        })
      })
    },
    async getNews() {
      this.getNewPostLoading = true
      this.newCount = 0
      await getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 1,
        pull_new: 1,
        last_update: this.messages.length === 0 ? null : this.messages[0].created_at
      }).then(res => {
        this.messages.unshift(...res.data.data)
      })
      this.getNewPostLoading = false
    }
  }
}
</script>

<style lang="stylus" scoped>
.privateMessage-layout
  border 0

  .new-tip
    margin-top 10px

    a
      color #409eff
      text-decoration none

      &:hover
        text-decoration underline

  .messages
    padding 10px

  .share-btn
    float right
    margin-left 10px
    padding 0 8px
    height 24px
    color #909399

    &:hover
      color #409eff

  .loading-layout
    text-align center
    font-size 20px
    color #409eff

  .get-more-btn
    text-align center

  .nomore-layout
    text-align center
    padding-bottom 10px
    color #999
</style>
<style lang="stylus">
.privateMessageItem
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

.movingMessage
  position absolute
  z-index 10
  background-color #fff
  width 345px
  border-radius 4px
  transition top 1s, left 1s

  .share-btn
    display none
</style>
