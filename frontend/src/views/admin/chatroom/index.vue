<template>
  <div class="app-container">
    <!-- <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Room type">
        <el-select v-model="form.room_type" placeholder="please choose">
          <el-option label="Star" :value="1" />
          <el-option label="Net" :value="2" />
        </el-select>
      </el-form-item>
      <el-form-item label="People limit">
        <el-input v-model.number="form.people_limit" style="width: 18%" />
      </el-form-item>
      <el-form-item label="Room count">
        <el-input v-model.number="form.room_count" style="width: 18%" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form> -->
    <FilenameOption v-model="filename" />
    <br>
    <el-button :loading="downloadLoading" style="margin: 20px;" type="primary" icon="el-icon-document" @click="handleDownload">Export Excel</el-button>
    <el-table
      v-loading="loading"
      :data="roomList.slice((currentPage-1)*pageSize,currentPage*pageSize)"
      border
      @filter-change="handleFilterChange"
    >
      <el-table-column label="Room ID" prop="id" align="center" />
      <el-table-column label="Room name" prop="room_name" align="center" show-overflow-tooltip />
      <el-table-column
        align="center"
        label="Room type"
        prop="room_type"
        :filters="[{text: 'Star', value: 1}, {text: 'Net', value: 2}]"
        column-key="room_type"
        :filter-method="()=>true"
        :filter-multiple="false"
      >
        <template slot-scope="scope">
          <el-tag :type="scope.row.room_type === 1 ? 'primary' : 'success'">{{ scope.row.room_type === 1 ? 'Star' : 'Net' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="People limit" prop="people_limit" align="center" />
      <el-table-column label="Room desc" prop="room_desc" align="center" show-overflow-tooltip />
      <el-table-column label="Created time" prop="createdTime" :formatter="formatTime" align="center" show-overflow-tooltip />
      <el-table-column label="Updated time" prop="updatedAt" :formatter="formatTime" align="center" show-overflow-tooltip />
      <el-table-column label="Operate" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="editShow(scope.row)">edit</el-button>
          <el-button type="text" @click="delShow(scope.row.id)">delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="paging"
      background
      :current-page="currentPage"
      :page-size="pageSize"
      layout="prev, pager, next"
      :total="total"
      @current-change="handleCurrentChange"
    />
    <d-edit ref="edit" @update="getRoomList" />
    <d-del ref="del" @update="getRoomList" />
  </div>
</template>

<script>
import { createChatRoom, getChatRoomList } from '@/api/room.js'
import { parseTime } from '@/utils/index.js'
import DEdit from './components/d-edit'
import DDel from './components/d-del'
import FilenameOption from './components/FilenameOption'

export default {
  components: {
    DEdit,
    DDel,
    FilenameOption
  },
  data() {
    return {
      chatroomList: [],
      loading: false,
      form: {
        room_type: null,
        people_limit: null,
        room_count: null
      },
      roomList: [],
      total: null,
      pageSize: 10,
      currentPage: 1,
      downloadLoading: false,
      filename: ''
    }
  },
  created() {
    this.getRoomList()
  },
  methods: {
    onSubmit() {
      createChatRoom(this.form).then(res => {
        if (res.code === 2000) {
          this.$message.success(res.msg)
          this.getRoomList()
          this.form = []
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
        this.loading = false
        if (res.code === 2000) {
          this.roomList = res.data.lists
          this.chatroomList = res.data.lists
          this.total = res.data.lists.length
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    handleFilterChange(obj) {
      this.roomList = this.chatroomList
      const keys = obj[Object.keys(obj)][0]
      const ROOM_TYPE_STAR = 1
      const ROOM_TYPE_NET = 2
      let roomStar = []
      let roomNet = []
      switch (keys) {
        case ROOM_TYPE_STAR:
          roomStar = this.roomList.filter((item) => {
            return item.room_type === ROOM_TYPE_STAR
          })
          this.roomList = roomStar
          this.total = roomStar.length
          break
        case ROOM_TYPE_NET:
          roomNet = this.roomList.filter((item) => {
            return item.room_type === ROOM_TYPE_NET
          })
          this.roomList = roomNet
          this.total = roomNet.length
          break
        default:
          this.roomList = this.chatroomList
          this.total = this.roomList.length
          break
      }
      const CURRENT_PAGE = 1
      this.handleCurrentChange(CURRENT_PAGE)
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['Room Id', 'Room name', 'Room type', 'People limit', 'Room desc', 'Created time', 'Updated time']
        const filterVal = ['id', 'room_name', 'room_type', 'people_limit', 'room_desc', 'created_at', 'updated_at']
        const list = this.roomList
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.filename,
          bookType: 'csv'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'created_at' || j === 'updated_at') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    editShow(data) {
      this.$refs.edit._show(data)
    },
    delShow(id) {
      this.$refs.del._show(id)
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

