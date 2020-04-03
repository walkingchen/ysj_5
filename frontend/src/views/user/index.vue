<template>
  <div class="user-content">
    <el-row class="user-content-head">
      <span>28号房间</span>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="7">
        <navigation />
        <priTimeline />
      </el-col>
      <el-col :span="9">
        <pubTimeline />
      </el-col>
      <el-col :span="8">
        <portrait />
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
// import { getRoomInf } from '@/api/chatroom'
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
    }
  },
  created() {
  },
  methods: {
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
