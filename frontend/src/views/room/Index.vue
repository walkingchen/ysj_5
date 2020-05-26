<template>
  <div class="room-layout">
    <div class="room-head">
      <span>{{ roomInfo.room_name }}</span>
      <el-avatar :size="35" :src="user.avatar ? user.avatar : ''" class="user-portrait">
        {{ user.avatar ? '' : user.nickname }}
      </el-avatar>
      <el-button type="text" class="logout-btn" @click="handleLogout"><v-icon name="sign-out-alt" /></el-button>
    </div>
    <div
      class="room-content"
      v-infinite-scroll="updateMoments"
      infinite-scroll-disabled="stopLoadMoments">
      <div>
        <el-row :gutter="20">
          <el-col :span="5">
            <navigation />
          </el-col>
          <el-col :span="11">
            <billboard ref="billboard" :sid="sid" />
          </el-col>
          <el-col :span="8">
            <connections @start-chat="startChart" />
            <messages ref="messages" :sid="sid" @share-success="handleShareSuccess" />
          </el-col>
        </el-row>
      </div>
    </div>

    <el-backtop target=".room-content" :bottom="chatShow ? 420 : 40" />

    <instant-chat
      ref="instantChat"
      :show="chatShow"
      :start-chat-user="startChatUser"
      @on-close="chatShow = false"
      @send-chat-message="sendChatMsg" />
  </div>
</template>

<script>
import 'vue-awesome/icons/sign-out-alt'
import io from 'socket.io-client'
import navigation from './navigation'
import billboard from './billboard'
import connections from './connections'
import messages from './messages'
import instantChat from './instantChat'
import { formatDate } from '@assets/utils.js'
import { getRoomInfo } from '@api/room'
import { logout } from '@api/auth'

export default {
  components: {
    navigation,
    billboard,
    connections,
    messages,
    instantChat
  },
  data() {
    return {
      roomInfo: [],
      socket: null,
      sid: '',
      chatShow: false,
      startChatUser: {}
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    stopLoadMoments() {
      return this.$refs.billboard.stopLoadMoments
    },
    members() {
      return this.$store.state.room_members
    }
  },
  async created() {
    const loading = this.$loading({ lock: true })

    await getRoomInfo(localStorage.getItem('roomid')).then(res => {
      const resdata = res.data
      if (resdata.result_code === 2000) {
        const { friends, me } = resdata.data.members
        this.$store.commit('setRoomMembers', [...[me], ...friends])
        this.roomInfo = resdata.data.room

        this.socket = io({ reconnection: false })
        this.socket.on('connect', () => {
          this.sid = this.socket.io.engine.id

          this.socket.emit('room_join', { // 加入房间
            room_id: this.roomInfo.id,
            username: me.username
          })

          this.socket.on('post_pull', data => {
            if (data.timeline_type === 0) { // 有新的public timeline
              this.$refs.billboard.newCount = data.posts_number
            } else { // 有新的private timeline
              this.$refs.messages.newCount = data.posts_number
            }
          })

          // 接收即时聊天消息
          this.socket.on('chat_msg', data => {
            console.log(data)
            const username = this.members.find(ele => ele.id === data.user_from).nickname
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
    handleLogout() {
      logout()
      localStorage.removeItem('roomid')
      this.socket.emit('room_leave', {
        room_id: this.roomInfo.id,
        username: this.user.username
      }, () => {
        this.socket.close()
      })
      this.$router.push({ name: 'Login' })
    },
    updateMoments() {
      this.$refs.billboard.getMomentList()
    },
    handleShareSuccess(id) {
      this.$refs.billboard.updateMoment(id, 0)
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
    }
  }
}
</script>

<style lang="stylus" scoped>
.room-layout
  height 100vh
  overflow hidden

.room-head
  background-color #f0fdda
  height 60px
  text-align center
  line-height 60px
  font-size 26px
  color #67C23A
  position relative

  .user-portrait
    position absolute
    top 12px
    right 45px

  .logout-btn
    position absolute
    top 8px
    right 20px

.room-content
  background-color #fffaf0
  padding 20px 0
  height calc(100vh - 100px)
  width 100%
  overflow auto

  & > div
    width 1200px
    margin 0 auto

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
</style>
