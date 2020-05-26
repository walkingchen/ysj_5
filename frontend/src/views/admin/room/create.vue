<template>
  <el-dialog
    title="Create rooms"
    :visible="show"
    width="500px"
    @close="close">
    <el-form ref="form" :model="formData" :rules="rules" label-width="100px">
      <el-form-item label="Count">
        <el-input-number v-model="formData.room_count" controls-position="right" :min="1" />
      </el-form-item>
      <el-form-item label="People Limit">
        <el-input-number v-model="formData.people_limit" controls-position="right" :min="1" />
      </el-form-item>
      <el-form-item label="Type">
        <el-select v-model="formData.room_type" prop="room_type">
          <el-option v-for="item in prototypes" :key="item.id" :value="item.id" :label="item.prototype_name" />
        </el-select>
      </el-form-item>
      <el-form-item label="Description">
        <el-input type="textarea" v-model="formData.room_desc"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="close">Cancel</el-button>
      <el-button type="primary" :loading="loading" @click="submit">Ok</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { createRoom } from '@api/room.js'

export default {
  props: ['show', 'prototypes'],
  data() {
    return {
      formData: {
        room_count: 1,
        people_limit: 1,
        room_type: '',
        room_desc: ''
      },
      rules: {
        room_type: [{ required: true, message: 'This field is required.', trigger: 'change' }]
      },
      loading: false
    }
  },
  methods: {
    close() {
      this.$emit('update:show', false)
    },
    submit() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          await createRoom(this.formData).then(res => {
            if (res.data.result_code === 2000) {
              this.$message.success('Edit room succeeded!')
              this.close()
              this.$emit('success')
            } else {
              this.$message.error(res.data.result_msg)
            }
          }).catch(() => {
            this.$message.error('Failed!')
          })
          this.loading = false
        }
      })
    }
  },
  watch: {
    show(val) {
      if (!val) {
        this.$refs.form.resetFields()
      }
    }
  }
}
</script>
