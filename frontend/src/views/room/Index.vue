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
            <billboard ref="billboard" />
          </el-col>
          <el-col :span="8">
            <connections />
            <messages @share-success="handleShareSuccess" />
          </el-col>
        </el-row>
      </div>
    </div>
    <el-backtop target=".room-content" />
  </div>
</template>

<script>
import 'vue-awesome/icons/sign-out-alt'
import io from 'socket.io-client'
import navigation from './navigation'
import billboard from './billboard'
import connections from './connections'
import messages from './messages'
import { getRoomInfo } from '@api/room'
import { logout } from '@api/auth'

export default {
  components: {
    navigation,
    billboard,
    connections,
    messages
  },
  data() {
    return {
      roomInfo: [],
      socket: null
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    stopLoadMoments() {
      return this.$refs.billboard.stopLoadMoments
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
          this.socket.emit('room_join', {
            room_id: this.roomInfo.id,
            username: me.username
          }, () => {
            console.log('ok')
          })

          /**
           * 注册timeline更新事件 post_pull
           * return:
           * data: {
           *     'timeline_type': 1，  // 0:public, 1:private
           *     'posts_number': 10
           * }
           */
          this.socket.on('post_pull', data => {
            console.log(data)
          })

          // 接收即时聊天消息
          this.socket.on('chat_msg', data => {
            console.log(data)
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
      this.$refs.billboard.getMomentList(0)
    },
    handleShareSuccess(id) {
      this.$refs.billboard.updateMoment(id, 0)
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
