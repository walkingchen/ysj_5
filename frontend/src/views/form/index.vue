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
    <el-table :data="roomList.slice((currentPage-1)*pageSize,currentPage*pageSize)" v-loading="loading" border>
      <el-table-column label="room ID" prop="id"></el-table-column>
      <el-table-column label="room name" prop="room_name" show-overflow-tooltip></el-table-column>
      <el-table-column label="room type">
        <template slot-scope="scope">
          <span>{{ scope.row.room_type === 1 ? 'star' : 'net' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="people limit" prop="people_limit"></el-table-column>
      <el-table-column label="room desc" prop="room_desc" show-overflow-tooltip></el-table-column>
      <el-table-column label="created time" prop="createdTime" :formatter="formatTime" show-overflow-tooltip></el-table-column>
      <el-table-column label="updated time" prop="updatedAt" :formatter="formatTime" show-overflow-tooltip></el-table-column>
      <el-table-column label="operate">
        <template slot-scope="scope">
          <el-button type="text" @click="amendShow(scope.row.id)">amend</el-button>
          <el-button type="text">delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="paging"
      background
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pageSize"
      layout="prev, pager, next"
      :total="total">
    </el-pagination>
    <d-amend ref="dam" @update="getRoomList"></d-amend>
  </div>
</template>

<script>
import { createChatRoom, getChatRoomList, amendChatRoom } from '@/api/chatRoom.js'
import { parseTime } from '@/utils/index.js'
import DEdit from './components/d-edit'

export default {
  data() {
    return {
      loading: false,
      form: {
        room_type: null,
        people_limit: null,
        room_count: null
      },
      roomList: [],
      total: null,
      pageSize: 8,
      currentPage: 1
    }
  },
  components: {
    DAmend
  },
  created() {
    this.getRoomList()
  },
  methods: {
    onSubmit() {
      console.log(this.form)
      createChatRoom(this.form).then(res => {
        if (res.code === 2000) {
          this.$message.success(res.msg)
          this.getRoomList()
          this.form.room_type = ''
          this.form.room_count = ''
          this.form.people_limit = ''
        } else {
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
      this.loading = true
      getChatRoomList().then(res => {
        if (res.code === 2000) {
          this.loading = false
          this.roomList = res.data.lists
          this.total = res.data.total
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    amendShow(id) {
      this.$refs.dam._show(id)
    },
    amendDetail() {
      amendChatRoom().then()
    },
    formatTime(row) {
      return parseTime(row.created_at)
    },
    handleCurrentChange(value) {
      this.currentPage = value
    }
  }
}
</script>

<style scoped>
.paging{
  float: right;
  margin: 15px 5px;
}
.line{
  text-align: center;
}
</style>

