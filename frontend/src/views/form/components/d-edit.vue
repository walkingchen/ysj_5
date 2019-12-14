<template>
  <div>
    <el-dialog title="edit chatroom" :visible.sync="isShow">
      <el-form :model="form">
        <el-form-item label="Room type" label-width="100px">
          <el-select v-model="form.room_type" placeholder="please choose">
            <el-option label="Star" :value="1" />
            <el-option label="Net" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="Room name" label-width="100px">
          <el-input v-model="form.room_name" />
        </el-form-item>

        <el-form-item label="People limit" label-width="100px">
          <el-input v-model.number="form.people_limit" />
        </el-form-item>
        <el-form-item label="Room desc" label-width="100px">
          <el-input v-model="form.room_desc" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="_hide">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Confirm</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { editChatRoom } from '@/api/chatRoom.js'
export default {
  data() {
    return {
      isShow: false,
      form: {
        id: null,
        room_name: '',
        room_type: null,
        room_desc: '',
        people_limit: null
      }
    }
  },
  methods: {
    _show(data) {
      this.form = data
      this.isShow = true
    },
    _hide(isChange) {
      this.isShow = false
      this.form = {}
      if (isChange === true) {
        this.$emit('update')
      }
    },
    handleSubmit() {
      console.log(this.form)
      editChatRoom(this.form).then(res => {
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
