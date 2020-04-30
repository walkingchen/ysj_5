<template>
  <div class="app-container">
    <el-form>
      <el-form-item label="Prototype Name：">{{ prototypeName }}</el-form-item>
      <el-form-item label="People Limit：">{{ peopleLimit }}</el-form-item>
    </el-form>
    <el-table :data="friendshipList" border style="width: 100%;margin-top:20px;">
      <el-table-column label="seat ID" prop="seatId" width="300" />
      <el-table-column label="friend seat IDs" prop="friendId" />
    </el-table>
  </div>
</template>

<script>
import { getPrototypeDetail } from '@api/room.js'

export default {
  data() {
    return {
      prototypeName: '',
      peopleLimit: '',
      friendshipList: [],
      id: this.$route.params.id
    }
  },
  created() {
    getPrototypeDetail(this.id).then(res => {
      if (res.data.result_code === 2000) {
        const friendship = JSON.parse(res.data.data.friendship)
        this.friendshipList = []
        for (const i in friendship) {
          this.friendshipList.push({
            seatId: i,
            friendId: friendship[i].join(', ')
          })
        }
        this.prototypeName = res.data.data.prototype_name
        this.peopleLimit = res.data.data.people_limit
      } else {
        this.$message.error(res.data.result_msg)
      }
    })
  }
}
</script>
