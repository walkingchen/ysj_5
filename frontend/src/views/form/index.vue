<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="room type">
        <!-- <el-input v-model="form.name" /> -->
        <el-select v-model="form.room_type" placeholder="请选择">
          <el-option label="aa" value="1"></el-option>
          <el-option label="bb" value="2"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="people limit">
        <el-input style="width: 18%" v-model="form.people_limit"></el-input>
      </el-form-item>
      <el-form-item label="room count">
        <el-input style="width: 18%" v-model="form.room_count"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
    <el-table v-model="roomList" border>
      <el-table-column label="room ID" prop="id"></el-table-column>
      <el-table-column label="room type" prop="type"></el-table-column>
      <el-table-column label="people limit" prop="limit"></el-table-column>
      <el-table-column label="operate">
        <el-button type="text">amend</el-button>
        <el-button type="text">delete</el-button>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { createChatRoom, getChatRoomList } from '@/api/chatRoom.js'

export default {
  data() {
    return {
      form: {
        room_type: '',
        people_limit: '',
        room_count: '',
      },
      roomList: [{
        id: 1,
        type: 'a',
        limit: 1
      }],
    }
  },
  methods: {
    onSubmit() {
      // createChatRoom(this.form).then(res => {
      //   if(res.code === 200) {
      //     this.$message.success('res.msg')
      //   }else{
      //     this.$message.error('res.msg')
      //   }
      // })
    },
    onCancel() {
      this.form.room_type = '',
      this.form.room_count = '',
      this.form.people_limit = ''
    },
    getRoomList() {
      // getChatRoomList().then(res => {
      //   if(res.code === 200) {
      //     this.roomList = res.data;
      //   }else{
      //     this.$message.error('res.msg')
      //   }
      // })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

