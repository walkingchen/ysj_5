<template>
  <div>
    <el-button type="primary" size="medium" style="margin-bottom: 10px;" @click="handleClick">Emergency Mail</el-button>
    <el-table v-loading="loading" :data="tableData" border size="small">
      <el-table-column label="Title" prop="title" show-overflow-tooltip />
      <el-table-column
        label="Type"
        prop="mail_type"
        :formatter="(row, column, cellValue) => cellValue === 1 ? 'morning mail' : 'night mail'"
      />
      <el-table-column label="Content" prop="content" show-overflow-tooltip />
      <el-table-column
        label="Send Hour"
        prop="send_hour"
        align="center"
        :formatter="(row, column, cellValue) => (cellValue > 9 ? cellValue : ('0' + cellValue)) + ':00'"
      />
      <el-table-column label="Actions" align="center" width="90">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" plain @click="edit(scope.row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>

    <edit-dialog :show.sync="editShow" :init-data="editRow" @success="setTableData" />
    <post-mail-dialog :show.sync="sendShow"/>
  </div>
</template>

<script>
import { getMails } from '@api/mail.js'
import editDialog from './edit'
import postMailDialog from './postMail.vue'

export default {
  components: {
    editDialog,
    postMailDialog
  },
  data() {
    return {
      loading: true,
      tableData: [],
      editShow: false,
      editRow: {},
      sendShow: false
    }
  },
  created() {
    this.setTableData()
  },
  methods: {
    setTableData() {
      this.loading = true
      getMails().then(res => {
        this.loading = false
        if (res.data.result_code === 2000) {
          this.tableData = res.data.data
        } else {
          this.$message.error(res.data.result_msg)
        }
      })
    },
    edit(row) {
      this.editShow = true
      this.editRow = row
    },
    handleClick () {
      this.sendShow = true
    }
  }
}
</script>
