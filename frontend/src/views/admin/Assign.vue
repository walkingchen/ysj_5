<template>
  <div>
    <el-divider>
      <v-icon name="download" />
      &nbsp;Download
    </el-divider>
    <div class="btns" style="margin-bottom: 50px">
      <el-button type="primary" plain @click="download('rooms')">
        <v-icon name="comments" />&nbsp;Rooms
      </el-button>
      <el-button type="primary" plain @click="download('users')">
        <v-icon name="users" />&nbsp;Users
      </el-button>
      <el-button type="primary" plain @click="download('privateMessage')">
        <v-icon name="envelope-open-text" />&nbsp;Private Message Template
      </el-button>
      <el-button type="primary" plain @click="download('template')">
        <v-icon name="file-csv" />&nbsp;Assign Template
      </el-button>
    </div>

    <el-divider>
      <v-icon name="upload" />
      &nbsp;Upload
    </el-divider>
    <div class="btns">
      <el-button type="primary" plain @click="upload('privateMessage')">
        <v-icon name="envelope" />&nbsp;Private Message
      </el-button>
      <el-button type="primary" plain @click="upload('assign')">
        <v-icon name="bezier-curve" />&nbsp;Assign
      </el-button>
    </div>
    <input ref="fileInput" type="file" accept=".csv" hidden @change="uploadFile" />
    <div class="uploadList">
      <ul>
        <li v-for="item in uploadList" :key="item.id">
          {{ item.name }}
          <el-progress :percentage="item.percentage" :status="item.status" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import 'vue-awesome/icons/download'
import 'vue-awesome/icons/upload'
import 'vue-awesome/icons/comments'
import 'vue-awesome/icons/users'
import 'vue-awesome/icons/envelope-open-text'
import 'vue-awesome/icons/file-csv'
import 'vue-awesome/icons/envelope'
import 'vue-awesome/icons/bezier-curve'
import { importPrivate, importAssignFile } from '@api/post.js'
const path = require('path')

export default {
  data () {
    return {
      uploadType: '',
      uploadList: []
    }
  },
  methods: {
    download (type) {
      let href = ''
      switch (type) {
        case 'rooms':
          href = '/api/room/export_room'
          break
        case 'users':
          href = '/api/room/export_room'
          break
        case 'privateMessage':
          href = 'https://ysj_5.soulfar.com/static/templates/private_message.csv'
          break
        case 'template':
          href = 'https://ysj_5.soulfar.com/static/templates/user_with_room_message_upload.csv'
          break
      }
      window.location.href = href
    },
    upload (type) {
      this.uploadType = type
      this.$refs.fileInput.click()
    },
    async uploadFile (e) {
      const file = e.target.files[0]

      if (path.extname(file.name) === '.csv') {
        const fileForm = new FormData()
        fileForm.append('file', file)

        const id = this.uploadList.length
        this.uploadList.push({
          id,
          name: file.name,
          percentage: 0,
          status: ''
        })

        const index = this.uploadList.findIndex(ele => ele.id === id)
        const item = this.uploadList[index]
        const onUploadProgress = progressEvent => {
          const percentage = Number(((progressEvent.loaded / progressEvent.total) * 100).toFixed(2))
          this.uploadList.splice(index, 1, Object.assign(item, { percentage }))
        }

        try {
          let res = null
          switch (this.uploadType) {
            case 'privateMessage':
              res = await importPrivate(fileForm, { onUploadProgress })
              break
            case 'assign':
              res = await importAssignFile(fileForm, { onUploadProgress })
              break
            default:
              break
          }

          if (res.data.result_code === 2000) {
            this.uploadList.splice(index, 1, Object.assign(item, { status: 'success' }))
          } else {
            this.uploadList.splice(index, 1, Object.assign(item, { status: 'warning' }))
          }
        } catch {
          this.uploadList.splice(index, 1, Object.assign(item, { status: 'exception' }))
        }
      } else {
        this.$message.error('Please upload CSV file.')
      }
      this.$refs.fileInput.value = null
    }
  }
}
</script>

<style lang="stylus" scoped>
.btns
  display flex
  justify-content center

.uploadList
  width 350px
  margin 15px auto 0

  li
    margin-bottom 8px
    font-size 14px
</style>
