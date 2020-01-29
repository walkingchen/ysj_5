<template>
  <div class="app-container">
    <FilenameOption v-model="filename" />
    <br>
    <el-button :loading="downloadLoading" style="margin: 20px;" type="primary" icon="el-icon-document" @click="handleDownload">Export Excel</el-button>
    <el-table
      v-loading="loading"
      :data="userList.slice((currentPage-1)*pageSize,currentPage*pageSize)"
      border
    >
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="username" label="Username" />
      <el-table-column prop="nickname" label="Nickname" />
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
  </div>
</template>

<script>
import { parseTime } from '@/utils/index.js'
import { getUserList } from '@/api/user.js'
import FilenameOption from './components/FilenameOption'

export default {
  components: {
    FilenameOption
  },
  data() {
    return {
      userList: [],
      loading: false,
      pageSize: 10,
      currentPage: 1,
      total: null,
      filename: ''
    }
  },
  created() {
    this.init()
  },
  methods: {
    init() {
      this.loading = true
      getUserList().then(res => {
        this.loading = false
        if (res.code === 2000) {
          this.userList = res.data.lists
          this.total = res.data.lists.length
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['Id', 'Username', 'Nickname']
        const filterVal = ['id', 'username', 'nickname']
        const list = this.userList
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
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
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
</style>
