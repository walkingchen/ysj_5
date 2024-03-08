<template>
  <div>
    <div style="margin-bottom: 20px;">
      <el-button type="primary" @click="emergencyShow = true">Emergency Mail</el-button>
      <el-button
        type="primary"
        icon="el-icon-plus"
        plain
        style="float: right"
        @click="create">
        Create
      </el-button>
    </div>

    <el-table v-loading="loading" :data="tableData" border size="small">
      <el-table-column label="Template Title" prop="title" show-overflow-tooltip />
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
      <el-table-column label="Actions" align="center" width="150">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" plain style="margin-right: 8px" @click="edit(scope.row)">Edit</el-button>
          <el-popconfirm
            title="Are you sure to delete this mail template?"
            confirmButtonText="Ok"
            cancelButtonText="Cancel"
            @confirm="deleteMail(scope.row.id)">
            <el-button slot="reference" size="mini" type="danger" plain>Delete</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <form-dialog :show.sync="formShow" :init-data="editRow" @success="setTableData" />
    <emergency-dialog :show.sync="emergencyShow"/>
  </div>
</template>

<script>
import { getMails, deleteMail } from '@api/mail.js'
import formDialog from './form'
import emergencyDialog from './emergency'

export default {
  components: {
    formDialog,
    emergencyDialog
  },
  data() {
    return {
      loading: true,
      tableData: [],
      formShow: false,
      editRow: {},
      emergencyShow: false
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
    create() {
      this.formShow = true
      this.editRow = null
    },
    edit(row) {
      this.formShow = true
      this.editRow = row
    },
    async deleteMail(id) {
      try {
        const res = deleteMail(id)
        if (res.data.result_code === 2000) this.setTableData()
        else this.$message.error(res.data.result_msg)
      } catch (error) {
        this.$message.error('Failed!')
      }
    }
  }
}
</script>
