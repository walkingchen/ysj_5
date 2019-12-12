<template>
  <div>
    <el-dialog title="edit chatroom" :visible.sync="isShow">
      <el-form :model="form">
        <el-form-item label="room type" label-width="100px">
          <el-select v-model="form.room_type" placeholder="type">
            <el-option label="star" :value="1" />
            <el-option label="net" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="room name" label-width="100px">
          <el-input v-model="form.room_name" />
        </el-form-item>

        <el-form-item label="people limit" label-width="100px">
          <el-input v-model.number="form.people_limit" />
        </el-form-item>
        <el-form-item label="room desc" label-width="100px">
          <el-input v-model="form.room_desc" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="_hide">cancel</el-button>
        <el-button type="primary" @click="handleSubmit">confirm</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { amendChatRoom } from '@/api/chatRoom.js'
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
    _show(id) {
      this.form.id = id
      this.isShow = true
    },
    _hide(isChange) {
      this.isShow = false
      this.form = []
      if (isChange === true) {
        this.$emit('update')
      }
    },
    handleSubmit() {
      amendChatRoom(this.form).then(res => {
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
