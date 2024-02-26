<template>
    <el-dialog
      title="Send Mail"
      :visible="show"
      width="80%"
      @close="close">
      <el-form ref="form" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="recipients" prop="recipients">
          <el-input v-model="formData.recipients" />
        </el-form-item>
        <el-form-item label="subject" prop="subject">
          <el-input v-model="formData.subject" />
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
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="close">Cancel</el-button>
        <el-button type="primary" :loading="loading" @click="submit">send</el-button>
      </span>
    </el-dialog>
  </template>
  
  <script>
  import { VueEditor } from 'vue2-editor'
  import { editMail } from '@api/mail.js'
  
  export default {
    components: {
      VueEditor
    },
    props: ['show', 'initData'],
    data() {
      return {
        formData: {
          content: '',
          recipients: '',
          subject: ''
        },
        rules: {
          recipients: [{ required: true, message: 'This field is required.', trigger: 'blur' }],
          subject: [{ required: true, message: 'This field is required.', trigger: 'blur' }],
          content: [{ required: true, message: 'This field is required.', trigger: 'blur' }]
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

            const submitData = JSON.parse(JSON.stringify(this.formData))
            // await editMail(this.initData.id, submitData).then(res => {
            //   if (res.data.result_code === 2000) {
            //     this.$message.success('post mail succeeded!')
            //     this.close()
            //   } else {
            //     this.$message.error(res.data.result_msg)
            //   }
            // }).catch(() => {
            //   this.$message.error('Failed!')
            // })
  
            this.loading = false
          }
        })
      }
    },
    watch: {
      show(val) {
        if (val) {
          const { mail_type, title, content, send_hour } = this.initData
          const _send_hour = send_hour ? ((send_hour > 9 ? send_hour : ('0' + send_hour)) + ':00') : '00:00'
          this.formData = {
            mail_type,
            title,
            content,
            send_hour: _send_hour
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
  