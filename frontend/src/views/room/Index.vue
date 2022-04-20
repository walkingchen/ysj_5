<template>
  <div class="room-layout">
    <header-com @logout="logout" />
    <div class="room-content">
      <div class="layout">
        <el-row :gutter="20">
          <el-col :span="showLeftCol ? 8 : 0">
            <el-card class="myself-box">
              <el-avatar
                :size="80"
                :src="user.avatar ? user.avatar : ''"
                :icon="user.avatar ? '' : 'el-icon-user-solid'" />
              <p>{{ user.nickname }}</p>
            </el-card>
            <private-message @has-data="showLeftCol = true" />
          </el-col>
          <el-col :span="showLeftCol ? 11 : 19">
            <add-public @on-success="addPostSuccess" />
            <topic-of-day :showLeftCol="showLeftCol" />
            <public-timeline ref="publicTimeline" />
          </el-col>
          <el-col :span="5">
            <daily-digest @has-data="showLeftCol = true" />
            <connections @start-chat="startChart" />
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
import { formatDate } from '@assets/utils.js'
import { getRoomInfo } from '@api/room'
import { getTopic } from '@api/post'
import headerCom from './header'
import dailyDigest from './dailyDigest'
import privateMessage from './privateMessage'
import addPublic from './addPublic'
import topicOfDay from './topicOfDay'
import publicTimeline from './publicTimeline'
import connections from './connections'
import postDetail from './postDetail'
import instantChat from './instantChat'

export default {
  components: {
    headerCom,
    dailyDigest,
    addPublic,
    topicOfDay,
    privateMessage,
    publicTimeline,
    connections,
    postDetail,
    instantChat
  },
  data() {
    return {
      roomInfo: [],
      socket: null,
      showLeftCol: false,
      chatShow: false,
      startChatUser: {}
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
    addPostSuccess (id) {
      this.$refs.publicTimeline.updatePost(id, 0)
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
    }
  },
  watch: {
    currentTopic () {
      this.showLeftCol = false
    }
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

.myself-box
  border 0
  padding 20px
  .el-card__body
    display flex
    flex-direction column
    align-items center
  p
    margin-top 15px

</style>
