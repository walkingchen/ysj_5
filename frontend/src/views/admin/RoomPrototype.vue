<template>
  <div>
    <upload-excel-component @on-success="handleSuccess" @upload="handleUpload" />
    <el-table :data="prototypeList" border style="width:100%;margin-top:20px;">
      <el-table-column label="ID" prop="id" align="center" width="50" />
      <el-table-column prop="prototype_name" label="Prototype Name" align="center" />
      <el-table-column prop="people_limit" label="People Limit" align="center" />
      <el-table-column label="Operate" align="center" width="160">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" plain @click="handleToDetail(scope.row.id)">view</el-button>
          <el-button size="mini" type="danger" plain @click="deletePrototype(scope.row.id)">delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import UploadExcelComponent from '@components/uploadExcel.vue'
import { addPrototype, getPrototypeList, deletePrototype } from '@api/room.js'

export default {
  components: { UploadExcelComponent },
  data() {
    return {
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
        if (res.data.result_code === 2000) {
          this.prototypeList = res.data.data
        }
      })
    },
    handleSuccess({ results, header }) {
      const obj = {}
      results.forEach(item => {
        const key = item.seat_id
        const value = String(item.friend_seat_ids).split('|')
        obj[key] = value
      })
      console.log(results)
      const friendship = Object.assign({}, obj)
      this.listParams.friendship = JSON.stringify(friendship)
      this.listParams.people_limit = results.length
      this.listParams.prototype_name = results[0].prototype_name
    },
    handleUpload() {
      addPrototype(this.listParams).then(res => {
        if (res.data.result_code === 2000) {
          this.getPrototypeListDate()
        } else {
          this.$message.error(res.data.result_msg)
        }
      })
    },
    deletePrototype(id) {
      deletePrototype(id).then(res => {
        if (res.data.result_code === 2000) {
          this.getPrototypeListDate()
        } else {
          this.$message.error(res.data.result_msg)
        }
      })
    },
    handleToDetail(id) {
      this.$router.push({ name: 'RoomPrototypeDetail', params: { id } })
    }
  }
}
</script>
