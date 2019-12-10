<template>
  <div>
    <el-dialog
      title="delete chatroom"
      :visible.sync="isShow"
      width="30%">
      <span>Are you sure to delete this chat room ?</span>
      <span slot="footer">
        <el-button @click="_hide">cancel</el-button>
        <el-button type="primary" @click="handleSubmit">confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { delChatRoom } from '@/api/chatRoom.js'

export default {
  data() {
    return {
      isShow: false,
      id: null
    }
  },
methods: {
    _show(id) {
      this.id = id
      this.isShow = true
    },
    _hide(isChange) {
      this.isShow = false
      this.id = null
      if (isChange == true) {
        this.$emit('update')
      }
    },
    handleSubmit() {
      delChatRoom({id: this.id}).then(res => {
        if (res.code === 2000) {
          this.$message.success(res.msg)
        } else {
          this.$message.error(res.msg)
        }
        this._hide(true)
      })
    }
  }
}
</script>
