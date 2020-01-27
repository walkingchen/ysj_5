<template>
  <div>
    <el-form style="margin: 20px auto 10px 30px">
      <el-form-item label="Prototype Name：">{{ prototypeName }}</el-form-item>
      <el-form-item label="People Limit：">{{ peopleLimit }}</el-form-item>
    </el-form>
    <el-table :data="friendshipList" border style="width: 100%; margin: 20px auto 20px 30px;">
      <el-table-column label="seat ID" prop="seatId" width="300" />
      <el-table-column label="friend seat ID" prop="friendId">
        <template slot-scope="scope">{{ scope.row.friendId | filter }}
          <!-- <div v-for="{item, index} in scope.row.friendId" :key="index">
          <span>{{item}}</span>
          </div> -->
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
          console.log(this.friendshipList)
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
