<template>
  <div class="room-layout">
    <header-com @logout="logout" />

    <div class="room-content" ref="content-div">
      <div class="layout">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card>
              <div class="right-top">
                <div class="myself-box">
                  <el-avatar
                    :size="45"
                    :src="user.avatar ? user.avatar : ''"
                    :icon="user.avatar ? '' : 'el-icon-user-solid'"
                  />
                  <p>{{ user.nickname }}</p>
                </div>
                <h2
                  class="module-title feed-title"
                  :class="{ fixed: feedTitleFixed }"
                  :style="{ width: feedTitleWidth }"
                  @click="handleSkip"
                >Your Feed</h2>
              </div>

              <private-message />
            </el-card>
          </el-col>

          <el-col :span="12">
            <add-public @on-success="addPostSuccess" />
            <trends />
            <public-forum ref="publicForum" />
          </el-col>
          <el-col :span="6">
            <div class="right-wrapper">
              <daily-digest />
              <connections @start-chat="startChart" />
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <el-backtop target=".room-content" :bottom="chatShow ? 420 : 40" />

    <post-detail />

    <instant-chat
      ref="instantChat"
      :show="chatShow"
      :start-chat-user="startChatUser"
      @on-close="chatShow = false"
      @send-chat-message="sendChatMsg" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import io from 'socket.io-client'
import elementResizeDetectorMaker from 'element-resize-detector'
import { formatDate } from '@assets/utils.js'
import { getRoomInfo } from '@api/room'
import { getTopic } from '@api/post'
import headerCom from './header'
import dailyDigest from './dailyDigest'
import privateMessage from './privateMessage'
import addPublic from './addPublic'
import trends from './trends'
import publicForum from './publicTimeline'
import connections from './connections'
import postDetail from './postDetail'
import instantChat from './instantChat'

export default {
  components: {
    headerCom,
    dailyDigest,
    addPublic,
    trends,
    privateMessage,
    publicForum,
    connections,
    postDetail,
    instantChat
  },
  data() {
    return {
      roomInfo: [],
      socket: null,
      chatShow: false,
      startChatUser: {},
      feedTitleFixed: false,
      feedTitleWidth: '100%'
    }
  },
  computed: mapState([
    'user',
    'friends',
    'currentTopic'
  ]),
  async created() {
    const rid = localStorage.getItem('roomid')
    getTopic(rid).then(({ data }) => {
      if (data.result_code === 2000) {
        this.$store.commit('setTopic', data.data)
      }
    })

    const loading = this.$loading({ lock: true })

    await getRoomInfo(rid).then(res => {
      const resdata = res.data
      if (resdata.result_code === 2000) {
        const { friends, me } = resdata.data.members
        this.$store.commit('setUser', me)
        this.$store.commit('setFriends', friends)
        this.roomInfo = resdata.data.room

        this.socket = io({ reconnection: false })
        this.socket.on('connect', () => {
          this.$store.commit('setSid', this.socket.io.engine.id)

          this.socket.emit('room_join', { // 加入房间
            room_id: this.roomInfo.id,
            username: me.username
          })

          this.socket.on('post_pull', data => { // 有新的post
            console.log(data)
            this.$bus.$emit('new_post', data)
          })

          this.socket.on('comment_pull', data => { // 有新的comment
            this.$bus.$emit('new_comment', data)
          })

          // 接收即时聊天消息
          this.socket.on('chat_msg', data => {
            const username = this.friends.find(ele => ele.id === data.user_from).nickname
            this.$notify.info({
              message: `【${username}】${data.message_content}`,
              customClass: 'new-message',
              onClick: () => {
                this.startChart(data.user_from)
              }
            })
            this.refs.instantChat.addMessage(data.user_from, data.user_from, data.message_content, data.message_timestamp)
          })
        })
      }
    })

    loading.close()
  },
  methods: {
    handleSkip () {
      document.getElementsByClassName('room-content')[0].scrollTop = 105
    },
    addPostSuccess (id) {
      this.$refs.publicForum.updatePost(id, 0)
    },
    startChart(user) {
      this.chatShow = true
      this.startChatUser = user
    },
    sendChatMsg({ to, content }) {
      this.socket.emit('chat_msg', {
        room_id: this.roomInfo.id,
        user_from: this.user.id,
        user_to: to,
        message_content: content,
        message_timestamp: formatDate(new Date(), 'yyyy-MM-ddThh:mm:ss')
      })
    },
    logout() {
      this.socket.emit('room_leave', {
        room_id: this.roomInfo.id,
        username: this.user.username
      }, () => {
        this.socket.close()
      })
    },
    onScroll() {
      const scrollTop = this.$refs['content-div'].scrollTop
      this.$bus.$emit('room-content-scroll', scrollTop)

      // 滚动到Feed标题位置时，将标题定位
      if (scrollTop >= 108) {
        this.feedTitleFixed = true
      } else {
        this.feedTitleFixed = false
      }
    }
  },
  mounted() {
    this.$refs['content-div'].addEventListener('scroll', this.onScroll)

    // 处理Feed标题栏宽度
    const erd = elementResizeDetectorMaker()
    erd.listenTo(document.getElementById('feed'), element => {
      this.feedTitleWidth = element.offsetWidth + 'px'
    })
  },
  beforeDestroy() {
    this.$refs['content-div'].removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style lang="stylus" scoped>
.room-layout
  height 100vh
  overflow hidden

.room-content
  position relative
  background-color #f0f2f5
  padding 20px 0
  height calc(100vh - 100px)
  width 100%
  overflow auto

  &::-webkit-scrollbar
    width 6px
    height 6px

  &::-webkit-scrollbar-track
    background-color transparent

  &::-webkit-scrollbar-thumb
    background-color transparent
    border-radius 6px

  &:hover
    &::-webkit-scrollbar-thumb
      background-color #ccc

.right-top
  background-color #5a77a1
  color #fff
  position relative
  padding-bottom var(--module-title-height)

.myself-box
  padding 20px
  display flex
  align-items center
  justify-content center

  p
    font-size 24px
    margin-left 15px

.feed-title
  background-color #5a77a1
  box-sizing border-box
  position absolute
  bottom 0

  &.fixed
    top 70px

.right-wrapper
  position fixed
  width calc(22.5% - 15px)
  top 90px
  right calc(5% + 5px)
</style>
<style lang="stylus">
.new-message
  cursor pointer

  &:hover .el-icon-info
    color #409eff

  .el-notification__content
    margin-top 0

  p
    width 244px
    line-height 24px
    overflow hidden
    text-overflow ellipsis
    white-space nowrap

.post-photo
  max-width 100%
  max-height 300px
  display block
  margin 5px 0

.moment-actions
  display flex
  flex-direction row-reverse

  button
    padding 0 8px
    height 24px
    color #909399

    &:hover
      color #409eff

    &.done
      color #409eff

  .count
    margin-right 8px

.unread
  background-color #ff9
</style>
