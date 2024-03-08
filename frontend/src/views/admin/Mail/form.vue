<template>
  <el-dialog
    :visible="show"
    :title="initData ? 'Edit Template' : 'Add Mail Template'"
    width="80%"
    @close="close"
  >
    <el-form ref="form" :model="formData" :rules="rules" label-width="100px">
      <el-form-item label="Room" prop="room_id">
        <el-select v-model="formData.room_id" placeholder="Select Room" style="width: 100%"> 
          <el-option
            v-for="item in rooms"
            :key="item.id"
            :label="item.room_name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Title" prop="title">
        <el-input v-model="formData.title" />
      </el-form-item>
      <el-form-item label="Content" prop="content">
        <div class="content-editor">
          <vue-editor
            :editor-toolbar="[
              [{ header: [false, 1, 2, 3, 4, 5, 6] }],
              ['bold', 'italic', 'underline', 'strike'],
              [{ align: '' }, { align: 'center' }, { align: 'right' }],
              [{ list: 'ordered' }, { list: 'bullet' }],
              [{ indent: '+1' }, { indent: '-1' }],
              [{'background':[]}, {'color':[]}],
              ['link', 'blockquote', 'code-block'],
              ['clean']
            ]"
            v-model="formData.content" />
        </div>
      </el-form-item>
      <el-form-item label="Type">
        <el-radio v-model="formData.mail_type" :label="1">morning mail</el-radio>
        <el-radio v-model="formData.mail_type" :label="2">night mail</el-radio>
      </el-form-item>
      <el-form-item label="Send Hour">
        <el-time-select v-model="formData.send_hour" :picker-options="{ start: '00:00', step: '01:00', end: '23:00' }" />
      </el-form-item>
      <el-form-item label="Day">
        <el-select v-model="formData.day" placeholder="Select Day">
          <el-option
            v-for="item in options"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="close">Cancel</el-button>
      <el-button type="primary" :loading="loading" @click="submit">Ok</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { VueEditor } from 'vue2-editor'
import { getRooms } from '@api/room.js'
import { createMail, editMail } from '@api/mail.js'

export default {
  components: {
    VueEditor
  },
  props: ['show', 'initData'],
  data() {
    return {
      rooms: [],
      formData: {
        room_id: '',
        content: '',
        mail_type: 1,
        title: '',
        send_hour: '',
        day: 1
      },
      rules: {
        room_id: [{ required: true, message: 'This field is required.', trigger: 'blur' }],
        title: [{ required: true, message: 'This field is required.', trigger: 'blur' }],
        content: [{ required: true, message: 'This field is required.', trigger: 'blur' }]
      },
      loading: false,
      options: [1, 2, 3, 4, 5, 6, 7, 8]
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

          const submitData = JSON.parse(JSON.stringify(this.formData))
          submitData.send_hour = Number(this.formData.send_hour.split(':')[0])

          try {
            const res = this.initData
              ? await editMail(this.initData.id, submitData)
              : await createMail(submitData)
              
            if (res.data.result_code === 2000) {
              this.$message.success((this.initData ? 'Edit' : 'Add') + ' template succeeded!')
              this.close()
              this.$emit('success')
            } else {
              this.$message.error(res.data.result_msg)
            }
          } catch (error) {
            this.$message.error('Failed!')
          }

          this.loading = false
        }
      })
    }
  },
  watch: {
    show(val) {
      if (val) {
        getRooms().then(res => {
          if (res.data.result_code === 2000) {
            this.rooms = res.data.data
          } else {
            this.$message.error(res.data.result_msg)
          }
        })

        if (this.initData) {
          const { room_id, mail_type, title, content, send_hour, day } = this.initData
          const _send_hour = send_hour ? ((send_hour > 9 ? send_hour : ('0' + send_hour)) + ':00') : '00:00'
          this.formData = {
            room_id,
            mail_type,
            title,
            content,
            send_hour: _send_hour,
            day: day === null ? 1 : day
          }
        } else {
          this.formData = {
            room_id: '',
            content: '',
            mail_type: 1,
            title: '',
            send_hour: '',
            day: 1
          }
        }
      } else {
        this.$refs.form.resetFields()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.content-editor
  line-height normal

  >>> .ql-toolbar.ql-snow
    border-color #dcdfe6
    border-top-left-radius 4px
    border-top-right-radius 4px

  >>> .ql-container.ql-snow
    border-color #dcdfe6
    border-bottom-left-radius 4px
    border-bottom-right-radius 4px
</style>
