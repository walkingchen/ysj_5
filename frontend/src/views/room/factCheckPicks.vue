<template>
  <div id="factCheckPicks" class="privateMessage-layout">
    <el-alert v-show="newCount > 0" type="info" center :closable="false" class="new-tip">
      <span slot="title">{{ newCount }} new messages, click <a href="javascript:;" @click="getNews">here</a> to update.</span>
    </el-alert>

    <div v-show="getNewPostLoading" class="loading-layout"><i class="el-icon-loading"></i></div>

    <div class="messages">
      <private-post-item
        v-for="item in messages"
        :key="item.id"
        ref="messageItem"
        :item="item"
      >
        <span v-if="item.timeline_type === 2" class="shared-tag">Shared</span>
        <el-button v-else round class="share-btn" size="small" @click="share(item.id)">Share with Group</el-button>
      </private-post-item>
    </div>

    <div class="nomore-layout">no more</div>

    <el-dialog
      :visible.sync="showShareDialog"
      center
      class="share-dialog">
      <div class="moments-item">
        <div class="moments-item-content">
          <el-avatar
            :size="40"
            :src="user.avatar ? user.avatar : ''"
            :icon="user.avatar ? '' : 'el-icon-user-solid'"
            class="user-portrait" />
          <div class="moment-text">
            <div>
              <span class="user-name">{{ user.nickname }}</span>
              <span class="shared-tip">shared:</span>
            </div>
            <div>
              <el-input
                size="small"
                placeholder="Say something..."
                ref="shareInput"
                v-model="shareContent" />
              <div class="shared-box">
                <private-post-item :item="sharedPost" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <el-button slot="footer" size="small" @click="submitShare">Post</el-button>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import 'vue-awesome/icons/share'
import privatePostItem from '@components/privatePostItem'
import { getPosts, createPost } from '@api/post'

export default {
  data() {
    return {
      messages: [],
      newCount: 0,
      getNewPostLoading: false,
      showShareDialog: false,
      sharedPost: {},
      shareContent: ''
    }
  },
  computed: mapState([
    'sid',
    'user',
    'currentTopic'
  ]),
  components: {
    privatePostItem
  },
  methods: {
    async getMessageList() {
      getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 1,
        topic: this.currentTopic
      }).then(res => {
        this.messages.push(...res.data.data.filter(item => item.topic === this.currentTopic))
      })
    },
    async getNews() {
      this.getNewPostLoading = true
      this.newCount = 0

      const params = {
        room_id: localStorage.getItem('roomid'),
        timeline_type: 1,
        topic: this.currentTopic
      }
      if (this.messages.length > 0) {
        params.pull_new = 1
        params.last_update = this.messages[0].created_at
      }
      await getPosts(params).then(res => {
        this.messages.unshift(...res.data.data.filter(item => item.topic === this.currentTopic))
      })
      this.getNewPostLoading = false
    },
    share (id) {
      this.shareContent = ''
      this.showShareDialog = true
      this.sharedPost = this.messages.find(ele => ele.id === id)
      this.$nextTick(() => {
        this.$refs.shareInput.focus()
      })
    },
    submitShare () {
      const { id, message_id } = this.sharedPost
      const index = this.messages.findIndex(ele => ele.id === id)

      const parentEle = document.getElementsByClassName('room-content')[0]
      const ele = this.$refs.messageItem[index].$el
      const cloneEle = ele.cloneNode(true)
      cloneEle.classList.add('movingMessage')
      cloneEle.style.width = (document.getElementById('groupDiscussion').offsetWidth - 32) + 'px'
      cloneEle.style.top = (ele.getBoundingClientRect().top + parentEle.scrollTop - 60) + 'px'
      cloneEle.style.left = ele.getBoundingClientRect().left + 'px'
      parentEle.appendChild(cloneEle)

      this.showShareDialog = false

      createPost({
        sid: this.sid,
        room_id: Number(localStorage.getItem('roomid')),
        timeline_type: 0,
        post_type: 1,
        topic: this.currentTopic,
        post_shared_id: id,
        post_content: this.shareContent,
        message_id
      }).then(({ data }) => {
        if (data.result_code === 2000) {
          const newPostId = data.data.id
          this.$bus.$emit('share-success', newPostId)

          const targetTop = document.getElementById('moments-ul').getBoundingClientRect().top + parentEle.scrollTop - 60
          const targetLeft = document.getElementById('moments-ul').getBoundingClientRect().left + 16
          cloneEle.style.top = targetTop + 'px'
          cloneEle.style.left = targetLeft + 'px'

          this.$bus.$on('share-success-refresh', _id => {
            if (_id === newPostId) {
              setTimeout(() => {
                cloneEle.remove()
              }, 1000)
            }
          })

          this.messages[index].timeline_type = 2
        } else {
          cloneEle.remove()
          this.$message.error('Failed!')
        }
      })
    }
  },
  mounted () {
    this.$bus.$on('new_post', data => {
      if (data.topic === this.currentTopic && data.timeline_type === 1) {
        this.newCount = data.posts_number
      }
    })
    this.$bus.$on('share', id => {
      this.share(id)
    })
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.messages = []
        this.getMessageList()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.privateMessage-layout
  padding 10px 6px
  box-sizing border-box

  .new-tip
    margin-top 10px

    a
      color #409eff
      text-decoration none

      &:hover
        text-decoration underline

  .loading-layout
    padding-top 10px
    color #fff

  .messages .privateMessageItem
    margin-top 10px

  .shared-tag
    position absolute
    right -25px
    top 11px
    transform rotate(45deg)
    padding 3px 25px
    background-color #fff
    color #409eff
    border 1px solid #a0cfff

  .share-btn
    position absolute
    right 10px
    top 10px
    background-color #fff
    color #409eff
    border 1px solid #409eff

    &:hover
      background-color #409eff
      color #fff

  .nomore-layout
    color #fff

.share-dialog
  >>> .el-dialog__body
    padding 10px 10px 0

  >>> .el-dialog__footer
    padding 0 0 15px
</style>
