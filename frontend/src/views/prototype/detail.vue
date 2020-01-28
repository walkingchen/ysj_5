<template>
  <div class="app-container">
    <el-form>
      <el-form-item label="Prototype Name：">{{ prototypeName }}</el-form-item>
      <el-form-item label="People Limit：">{{ peopleLimit }}</el-form-item>
    </el-form>
    <el-table :data="friendshipList" border style="width: 100%;margin-top:20px;">
      <el-table-column label="seat ID" prop="seatId" width="300" />
      <el-table-column label="friend seat ID" prop="friendId">
        <template slot-scope="scope">{{ scope.row.friendId | filter }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getPrototypeDetail } from '@/api/room.js'

export default {
  filters: {
    filter(value) {
      return value + ''
    }
  },
  data() {
    return {
      prototypeName: '',
      peopleLimit: '',
      friendshipList: [],
      id: ''
    }
  },
  created() {
    this.id = this.$route.params.id
    this.init()
  },
  methods: {
    init() {
      getPrototypeDetail(this.id).then(res => {
        if (res.code === 2000) {
          const obj = JSON.parse(res.data.friendship)
          this.friendshipList = []
          for (const i in obj) {
            const o = { 'seatId': i, 'friendId': obj[i] }
            this.friendshipList.push(o)
          }
          this.prototypeName = res.data.prototype_name
          this.peopleLimit = res.data.people_limit
        } else {
          this.$message.error(res.msg)
        }
      })
    }
  }
}
</script>

<style scoped>
.container{
  width: 100vw
}
</style>
