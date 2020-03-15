<template>
  <div class="app-container">
    <FilenameOption v-model="filename" />
    <br>
    <el-button :loading="downloadLoading" style="margin: 20px;" type="primary" icon="el-icon-document" @click="handleDownload">Export CSV</el-button>
    <el-table
      v-loading="loading"
      :data="userList"
      border
    >
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="username" label="Username" />
      <el-table-column prop="nickname" label="Nickname" />
    </el-table>
    <el-pagination
      class="paging"
      background
      :current-page="params.page"
      :page-size="params.size"
      layout="prev, pager, next"
      :total="total"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
import { getUserList } from '@/api/user.js'
import FilenameOption from './components/FilenameOption'

export default {
  components: {
    FilenameOption
  },
  data() {
    return {
      userList: [],
      totalUserList: [],
      loading: false,
      total: null,
      downloadLoading: false,
      filename: '',
      params: {
        page: 1,
        size: 10
      }
    }
  },
  created() {
    this.init()
  },
  methods: {
    init() {
      this.loading = true
      getUserList(this.params).then(res => {
        this.loading = false
        if (res.code === 2000) {
          this.userList = res.data.lists
          this.total = res.data.total
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    handleDownload() {
      getUserList({ page: 0, size: 0 }).then(res => {
        if (res.code === 2000) {
          this.totalUserList = res.data.lists
          this.downloadLoading = true
          import('@/vendor/Export2Excel').then(excel => {
            const tHeader = ['Id', 'Username', 'Nickname']
            const filterVal = ['id', 'username', 'nickname']
            const list = this.totalUserList
            const data = this.formatJson(filterVal, list)
            excel.export_json_to_excel({
              header: tHeader,
              data,
              filename: this.filename,
              bookType: 'csv'
            })
            this.downloadLoading = false
          })
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    handleCurrentChange(value) {
      this.params.page = value
      this.init()
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
