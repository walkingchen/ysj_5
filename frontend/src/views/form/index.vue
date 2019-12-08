<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="room type">
        <!-- <el-input v-model="form.name" /> -->
        <el-select v-model="form.room_type" placeholder="请选择">
          <el-option label="star" :value="1"></el-option>
          <el-option label="net" :value="2"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="people limit">
        <el-input style="width: 18%" v-model.number="form.people_limit"></el-input>
      </el-form-item>
      <el-form-item label="room count">
        <el-input style="width: 18%" v-model.number="form.room_count"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="roomList" border>
      <el-table-column label="room ID" prop="id"></el-table-column>
      <el-table-column label="room name" prop="room_name"></el-table-column>
      <el-table-column label="room type">
        <template slot-scope="scope">
          <span>{{ scope.row.room_type === 1 ? 'star' : 'net' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="people limit" prop="people_limit"></el-table-column>
      <el-table-column label="room desc" prop="room_desc"></el-table-column>
      <el-table-column label="created time" prop="createdTime" :formatter="formatTime">
      </el-table-column>
      <el-table-column label="operate">
        <el-button type="text">amend</el-button>
        <el-button type="text">delete</el-button>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { createChatRoom, getChatRoomList } from '@/api/chatRoom.js'
import { parseTime } from '@/utils/index.js'

export default {
  data() {
    return {
      form: {
        room_type: null,
        people_limit: null,
        room_count: null
      },
      roomList: [{

      }]
    }
  },
  created () {
    this.getRoomList()
  },
  methods: {
    onSubmit() {
      console.log(this.form)
      createChatRoom(this.form).then(res => {
        if(res.code === 2000) {
          this.$message.success(res.msg)
          this.getRoomList()
          this.form.room_type = ''
          this.form.room_count = ''
          this.form.people_limit = ''
        }else{
          this.$message.error(res.msg)
        }
      })
    },
    onCancel() {
      this.form.room_type = ''
      this.form.room_count = ''
      this.form.people_limit = ''
    },
    getRoomList() {
      getChatRoomList().then(res => {
        if(res.code === 2000) {
          this.roomList = res.data.lists
          console.log(this.roomList)
        }else{
          this.$message.error(res.msg)
        }
      })
    },
    formatTime(row) {
      return parseTime(row.created_at)
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

