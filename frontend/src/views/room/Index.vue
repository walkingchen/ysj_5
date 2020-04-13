<template>
  <div class="room-layout">
    <div class="room-head">
      <span>{{ roomInfo.room_name }}</span>
      <el-button type="text" class="logout-btn" @click="handleLogout"><v-icon name="sign-out-alt" /></el-button>
    </div>
    <div class="room-content">
      <div>
        <el-row :gutter="20">
          <el-col :span="5">
            <navigation />
          </el-col>
          <el-col :span="11">
            <billboard />
          </el-col>
          <el-col :span="8">
            <connections />
            <messages />
          </el-col>
        </el-row>
      </div>
    </div>
    <el-backtop target=".room-content" />
  </div>
</template>

<script>
import 'vue-awesome/icons/sign-out-alt'
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
      roomInfo: []
    }
  },
  created() {
    const roomid = localStorage.getItem('roomid')
    if (roomid) {
      getRoomInfo(roomid).then(res => {
        const resdata = res.data
        switch (resdata.result_code) {
          case 2000: {
            const { friends, me } = resdata.data.members
            this.$store.commit('setRoomMembers', [...[me], ...friends])
            this.roomInfo = resdata.data.room[0]
            break
          }
          case 4001:
            this.$router.push({ name: 'Login' })
            break
        }
      })
    } else {
      this.$router.push({ name: 'Login' })
    }
  },
  methods: {
    handleLogout() {
      logout()
      localStorage.removeItem('roomid')
      this.$router.push({ name: 'Login' })
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
