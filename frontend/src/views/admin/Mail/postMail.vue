<template>
    <el-dialog
      title="Emergency Mail"
      :visible="show"
      width="80%"
      @close="close">
      <el-form ref="form" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="Room" prop="room">
          <el-select v-model="formData.room" placeholder="Select Room" @change="handleSelectRoom" style="width: 100%"> 
            <el-option
              v-for="item in roomList"
              :key="item.room_id"
              :label="item.room_name"
              :value="item.room_id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Member" prop="member">
          <el-select v-model="formData.member" placeholder="Select Member" style="width: 100%" clearable>
            <el-option
              v-for="item in membersList"
              :key="item.user_id"
              :label="item.user_info.email"
              :value="item.user_id">
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
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="close">Cancel</el-button>
        <el-button type="primary" :loading="loading" @click="submit">send</el-button>
      </span>
    </el-dialog>
  </template>
  
  <script>
  import { VueEditor } from 'vue2-editor'
  import { emergencyMail  } from '@api/mail.js'
  import { getRooms, getRoomMembers  } from '@api/room.js'
  
  export default {
    components: {
      VueEditor
    },
    props: ['show'],
    data() {
      return {
        formData: {
          content: '',
          title: '',
          room: '',
          member: ''
        },
        rules: {
          room: [{ required: true, message: 'This field is required.', trigger: 'change' }],
          title: [{ required: true, message: 'This field is required.', trigger: 'blur' }],
          content: [{ required: true, message: 'This field is required.', trigger: 'blur' }]
        },
        loading: false,
        roomList: [],
        membersList: []
      }
    },
    methods: {
      getRoomList () {
        getRooms().then(res => {
          if (res.data.result_code === 2000) {
            this.roomList = res.data.data
          } else {
            this.$message.error(res.data.result_msg)
          }
        })
      },
      handleSelectRoom (val) {
        getRoomMembers(val).then(res => {
          if (res.data.result_code === 2000) {
            this.membersList = res.data.data
          } else {
            this.$message.error(res.data.result_msg)
          }
        })
      },
      close() {
        this.$emit('update:show', false)
      },
      submit() {
        this.$refs.form.validate(async valid => {
          if (valid) {
            this.loading = true
            const submitData = {
              content: this.formData.content,
              member_id: this.formData.member,
              room_id: this.formData.room,
              title: this.formData.title
            }
            emergencyMail(submitData).then(res => {
              this.loading = false
              if (res.data.result_code === 2000) {
                this.$message.success('post mail succeeded!')
                this.close()
              } else {
                this.$message.error(res.data.result_msg)
              }
            }).catch(() => {
              this.$message.error('Failed!')
            })
          }
        })
      }
    },
    watch: {
      show(val) {
        if (val) {
          this.formData = {
            content: '',
            title: '',
            room: '',
            member: ''
          },
          this.getRoomList()
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
  