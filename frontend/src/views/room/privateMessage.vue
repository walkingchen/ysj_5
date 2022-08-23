<template>
  <el-card v-show="messages.length > 0" class="privateMessage-layout">
    <h2 class="module-title">Private Message Feed</h2>

    <el-alert v-show="newCount > 0" type="info" center :closable="false" class="new-tip">
      <span slot="title">{{ newCount }} new messages, click <a href="javascript:;" @click="getNews">here</a> to update.</span>
    </el-alert>

    <div class="loading-layout" v-show="getNewPostLoading"><i class="el-icon-loading"></i></div>

    <div class="messages">
      <private-post-item
        v-for="item in messages"
        :key="item.id"
        ref="messageItem"
        :item="item"
      >
        <span v-if="item.timeline_type === 2" class="shared-tag">shared</span>
        <template v-if="item.timeline_type !== 2" #actions>
          <el-button size="mini" class="share-btn" @click="share(item.id)">share</el-button>
        </template>
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
  </el-card>
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
        timeline_type: 0,
        topic: this.currentTopic
      }
      if (this.moments.length > 0) {
        params.pull_new = 1
        params.last_update = this.moments[0].created_at
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
      cloneEle.style.width = (document.getElementsByClassName('topic-layout')[0].offsetWidth - 20) + 'px'
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
          const targetLeft = document.getElementById('moments-ul').getBoundingClientRect().left
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
  margin-top 20px
  background-color #f5f5f5
  border 3px solid #d3d3d3

  .new-tip
    margin-top 10px

    a
      color #409eff
      text-decoration none

      &:hover
        text-decoration underline

  .messages
    padding 0 10px

    .privateMessageItem
      border-bottom 1px solid #e4e7ed

      &:last-child
        border-bottom 0

  .shared-tag
    position absolute
    right -22px
    top 8px
    transform rotate(45deg)
    padding 3px 20px
    background-color #ecf5ff
    color #409eff
    border 1px solid #a0cfff

  .share-btn
    height 24px
    padding 0 8px
    line-height 22px

  .nomore-layout
    text-align center
    padding-bottom 10px
    color #999

.share-dialog
  >>> .el-dialog__body
    padding 10px 10px 0

  >>> .el-dialog__footer
    padding 0 0 15px
</style>
