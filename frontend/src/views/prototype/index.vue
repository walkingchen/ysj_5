<template>
  <div class="app-container">
    <upload-excel-component ref="upload" :on-success="handleSuccess" :before-upload="beforeUpload" :upload-prototype="handleUpload" :clear-file="clearFileDetail" />
    <!-- <el-table :data="tableData" border highlight-current-row style="width: 100%;margin-top:20px;">
      <el-table-column v-for="item of tableHeader" :key="item" :prop="item" :label="item" />
    </el-table> -->
    <el-table :data="prototypeList" border style="width: 100%;margin-top:20px;">
      <el-table-column type="index" label="No." align="center" width="100" />
      <el-table-column prop="prototype_name" label="Prototype Name" align="center" />
      <el-table-column prop="people_limit" label="People Limit" align="center" />
      <!-- <el-table-column prop="created_at" label="Created At" :formatter="formatTime" align="center" />
      <el-table-column prop="updated_at" label="Updated At" :formatter="formatTime" align="center" /> -->
      <el-table-column label="Operate" align="center">
        <template slot-scope="scope">
          <el-button size="mini">view</el-button>
          <el-button size="mini" type="danger" @click="delDetail(scope.row.id)">delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import UploadExcelComponent from '@/components/UploadExcel/index.vue'
import { addPrototype, getPrototypeList, delPrototypeDetail } from '@/api/chatRoom.js'
import { parseTime } from '@/utils/index.js'

export default {
  name: 'UploadExcel',
  components: { UploadExcelComponent },
  data() {
    return {
      // tableData: [],
      // tableHeader: [],
      prototypeList: [],
      listParams: {
        prototype_name: '',
        people_limit: '',
        friendship: {}
      }
    }
  },
  created() {
    this.getPrototypeListDate()
  },
  methods: {
    getPrototypeListDate() {
      getPrototypeList().then(res => {
        if (res.code === 2000) {
          this.prototypeList = res.data.lists
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 1
      if (isLt1M) {
        return true
      }
      this.$message({
        message: 'Please do not upload files larger than 1m in size.',
        type: 'warning'
      })
      return false
    },
    handleSuccess({ results, header }) {
      // this.tableData = results
      // this.tableHeader = header
      const obj = {}
      results.forEach(item => {
        const key = item.seat_id
        const value = String(item.friend_seat_ids).split('|')
        obj[key] = value
      })
      const friendship = Object.assign({}, obj)
      this.listParams.friendship = JSON.stringify(friendship)
      this.listParams.people_limit = results.length
      this.listParams.prototype_name = this.$refs.upload.prototype_name
      // console.log(this.listParams)
    },
    handleUpload() {
      addPrototype(this.listParams).then(res => {
        if (res.code === 2000) {
          this.$message.success(res.msg)
          this.getPrototypeListDate()
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    formatTime(row) {
      return parseTime(row.created_at)
    },
    delDetail(id) {
      delPrototypeDetail(id).then(res => {
        if (res.code === 2000) {
          this.$message.success(res.msg)
          this.getPrototypeListDate()
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    clearFileDetail() {
      this.listParams = {}
    }
  }
}
</script>
