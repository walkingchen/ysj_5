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
      <el-button
        type="primary"
        icon="el-icon-plus"
        plain
        @click="createShow = true"
        style="float: right">
        Create
      </el-button>
    </div>

    <el-table v-loading="loading" :data="tableData" border size="small" @filter-change="handleFilterChange">
      <el-table-column label="ID" prop="id" align="center" />
      <el-table-column label="Name" prop="room_name" align="center" show-overflow-tooltip />
      <el-table-column
        align="center"
        label="Type"
        prop="type_name"
        :formatter="formatType"
        column-key="room_type"
        :filters="typeFilters"
      />
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
      <el-table-column label="Operate" align="center" width="150">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" plain style="margin-right: 8px" @click="edit(scope.row)">Edit</el-button>
          <el-popconfirm
            title="Are you sure to delete this chat room?"
            confirmButtonText="Ok"
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
        :total="filteredList.length"
        @size-change="handlePageSizeChange"
        @current-change="handleCurrentChange" />
    </div>

    <create-dialog :show.sync="createShow" :prototypes="prototypes" @success="getRoomList" />
    <edit-dialog :show.sync="editShow" :prototypes="prototypes" :init-data="editRow" @success="getRoomList" />
  </div>
</template>

<script>
import { formatDate } from '@assets/utils.js'
import { getRooms, deleteRoom, getPrototypeList } from '@api/room.js'
import createDialog from './create'
import editDialog from './edit'

export default {
  components: {
    createDialog,
    editDialog
  },
  data() {
    return {
      loading: true,
      prototypes: [],
      allRooms: [],
      filters: {},
      currentPage: 1,
      pageSize: 10,
      filename: '',
      downloadLoading: false,
      createShow: false,
      editShow: false,
      editRow: {}
    }
  },
  computed: {
    filteredList() {
      return this.allRooms.filter(item => {
        let flag = true
        for (const key in this.filters) {
          if (this.filters[key].length > 0 && this.filters[key].findIndex(ele => ele === item[key]) === -1) {
            flag = false
          }
        }
        return flag
      })
    },
    tableData() {
      return this.filteredList.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    typeFilters() {
      return this.prototypes.map(item => {
        return {
          text: item.prototype_name,
          value: item.id
        }
      })
    }
  },
  created() {
    this.getRoomList()
    getPrototypeList().then(res => {
      if (res.data.result_code === 2000) {
        this.prototypes = res.data.data
      } else {
        this.$message.error(res.data.result_msg)
      }
    })
  },
  methods: {
    getRoomList() {
      this.loading = true
      getRooms().then(res => {
        this.loading = false
        if (res.data.result_code === 2000) {
          this.allRooms = res.data.data
        } else {
          this.$message.error(res.data.result_msg)
        }
      })
    },
    handleCurrentChange(page) {
      this.currentPage = page
    },
    handlePageSizeChange(size) {
      this.pageSize = size
    },
    formatTime(row, column) {
      return formatDate(row[column.property])
    },
    formatType(row) {
      return this.getPrototypeName(row.room_type)
    },
    handleFilterChange(filters) {
      this.filters = filters
      this.currentPage = 1
    },
    edit(row) {
      this.editShow = true
      this.editRow = row
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
    getPrototypeName(id) {
      const index = this.prototypes.findIndex(ele => ele.id === id)
      return index > -1 ? this.prototypes[index].prototype_name : `(${id})`
    },
    handleDownload() {
      this.downloadLoading = true
      import('@assets/Export2Excel').then(excel => {
        const tHeader = ['ID', 'Name', 'Type', 'People Limit', 'Description', 'Created Time', 'Updated Time']
        const filterVal = ['id', 'room_name', 'room_type', 'people_limit', 'room_desc', 'created_at', 'updated_at']
        const data = this.formatJson(filterVal, this.allRooms)
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
        switch (j) {
          case 'created_at':
          case 'updated_at':
            return formatDate(v[j])
          case 'room_type':
            return this.getPrototypeName(v[j])
          default:
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
