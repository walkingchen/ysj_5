<template>
  <div class="user-content">
    <el-row class="user-content-head">
      <span>{{ roomInfor.room_name }}</span>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="7">
        <navigation />
        <priTimeline />
      </el-col>
      <el-col :span="9">
        <pubTimeline :id="roomInfor.id" />
      </el-col>
      <el-col :span="8">
        <portrait :members="members" />
        <chatroom />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import chatroom from './components/chatroom'
import navigation from './components/navigation'
import portrait from './components/portrait'
import priTimeline from './components/privateTimeline'
import pubTimeline from './components/publicTimeline'
import { chatLogin, getRoomInf } from '@/api/chatroom'
export default {
  components: {
    chatroom,
    navigation,
    portrait,
    priTimeline,
    pubTimeline
  },
  data() {
    return {
      members: [],
      roomInfor: []
    }
  },
  created() {
    this.login()
  },
  methods: {
    login() {
      const params = { username: 'user14', password: '123456' }
      chatLogin(params).then(res => {
        getRoomInf(28).then(res => {
          if (res.result_code === 2000) {
            const friends = res.data.members.friends
            const me = res.data.members.me
            friends.unshift(me)
            this.members = friends
            this.roomInfor = res.data.room[0]
          }
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.user-content{
  width: 100%;
  height: 100%;
  .user-content-head{
    width: 100%;
    height: 8vh;
    background-color: white;
    display: table;
    span{
      display: table-cell;
      vertical-align: middle;
      text-align: center;
    }
  }
}
</style>
