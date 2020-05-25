<template>
  <div>
    <div style="margin-bottom: 20px;">
      <el-button
        :loading="downloadLoading"
        type="primary"
        icon="el-icon-download"
        @click="handleDownload">
        Export Excel
      </el-button>
      <el-input
        v-model="filename"
        placeholder="Please enter the file name (default excel-list)"
        prefix-icon="el-icon-document"
        style="width: 345px;margin-left: 15px;" />
    </div>

    <el-table v-loading="loading" :data="tableData" border size="small">
      <el-table-column label="ID" prop="id" align="center" />
      <el-table-column label="Name" prop="room_name" align="center" show-overflow-tooltip />
      <el-table-column label="People limit" prop="people_limit" align="center" />
      <el-table-column label="Description" prop="room_desc" align="center" show-overflow-tooltip />
      <el-table-column
        label="Created Time"
        prop="created_at"
        :formatter="formatTime"
        align="center"
        show-overflow-tooltip
      />
      <el-table-column
        label="Updated Time"
        prop="updated_at"
        :formatter="formatTime"
        align="center"
        show-overflow-tooltip
      />
      <el-table-column label="Operate" align="center">
        <template slot-scope="scope">
          <!-- <el-button size="mini" type="primary" plain style="margin-right: 8px" @click="handleToDetail(scope.row)">Edit</el-button> -->
          <el-popconfirm
            title="Are you sure to delete this chat room?"
            confirmButtonText="Confirm"
            cancelButtonText="Cancel"
            @onConfirm="deleteRoom(scope.row.id)">
            <el-button slot="reference" size="mini" type="danger" plain>Delete</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <div class="page">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handlePageSizeChange"
        @current-change="handleCurrentChange" />
    </div>
  </div>
</template>

<script>
import { formatDate } from '@assets/utils.js'
import { getRooms, deleteRoom } from '@api/room.js'

export default {
  data() {
    return {
      loading: true,
      roomList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      filename: '',
      downloadLoading: false
    }
  },
  computed: {
    tableData() {
      return this.roomList.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    }
  },
  created() {
    this.getRoomList()
  },
  methods: {
    getRoomList() {
      this.loading = true
      getRooms().then(res => {
        this.loading = false
        if (res.data.result_code === 2000) {
          this.roomList = res.data.data
          this.total = res.data.data.length
        } else {
          this.$message.error(res.data.result_msg)
        }
      })
    },
    handleCurrentChange(page) {
      this.currentPage = value
    },
    handlePageSizeChange(size) {
      this.pageSize = size
    },
    formatTime(row, column) {
      return formatDate(row[column.property])
    },
    deleteRoom(id) {
      deleteRoom(id).then(res => {
        if (res.data.result_code === 2000) {
          this.getRoomList()
        } else {
          this.$message.error(res.data.result_msg)
        }
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@assets/Export2Excel').then(excel => {
        const tHeader = ['ID', 'Name', 'People Limit', 'Description', 'Created Time', 'Updated Time']
        const filterVal = ['id', 'room_name', 'people_limit', 'room_desc', 'created_at', 'updated_at']
        const data = this.formatJson(filterVal, this.roomList)
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
          return formatDate(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>

<style lang="stylus" scoped>
.page
  display flex
  justify-content center
  margin-top 10px
</style>
