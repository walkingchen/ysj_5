<template>
  <div>
    <el-divider>
      <v-icon name="download" />
      &nbsp;Download
    </el-divider>
    <div class="btns" style="margin-bottom: 50px">
      <el-button type="primary" plain @click="download('rooms')">
        <v-icon name="comments" />&nbsp;Rooms Generated
      </el-button>
      <el-button type="primary" plain @click="download('users')">
        <v-icon name="users" />&nbsp;Users Registered
      </el-button>
    </div>

    <el-divider>
      <v-icon name="upload" />
      &nbsp;Upload
    </el-divider>
    <div class="uploadBtns">
      <div class="uploadType">Private Message</div>
      <div class="btns">
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('privateMessage')">
            <v-icon name="envelope-open-text" />&nbsp;Message Pool
          </el-button>
          <br />
          template: <a @click="download('privateMessage')">click here to download</a>
        </div>
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('privateMessagePictures')">
            <v-icon name="images" />&nbsp;Message Pool Pictures (*.zip)
          </el-button>
        </div>
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('privateMessageAssign')">
            <v-icon name="bezier-curve" />&nbsp;Message Assign
          </el-button>
          <br />
          template: <a @click="download('privateMessageAssign')">click here to download</a>
        </div>
      </div>
    </div>
    <div class="uploadBtns">
      <div class="uploadType">System Message</div>
      <div class="btns">
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('systemMessage')">
            <v-icon name="envelope-open-text" />&nbsp;Message Pool
          </el-button>
          <br />
          template: <a @click="download('systemMessage')">click here to download</a>
        </div>
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('systemMessagePictures')">
            <v-icon name="images" />&nbsp;Message Pool Pictures (*.zip)
          </el-button>
        </div>
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('systemMessageAssign')">
            <v-icon name="bezier-curve" />&nbsp;Message Assign
          </el-button>
          <br />
          template: <a @click="download('systemMessageAssign')">click here to download</a>
        </div>
      </div>
    </div>
    <div class="uploadBtns">
      <div class="uploadType">Daily Poll</div>
      <div class="btns">
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('dailyPictures')">
            <v-icon name="images" />&nbsp;Message Pool Pictures (*.zip)
          </el-button>
        </div>
        <div class="btn-box">
          <el-button type="primary" plain @click="upload('dailyAssign')">
            <v-icon name="bezier-curve" />&nbsp;Message Assign
          </el-button>
          <br />
          template: <a @click="download('dailyAssign')">click here to download</a>
        </div>
      </div>
    </div>

    <input ref="fileInput" type="file" :accept="accept" hidden @change="uploadFile" />
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
import 'vue-awesome/icons/images'
import 'vue-awesome/icons/bezier-curve'
import {
  importPrivateMessage,
  importPrivateMessagePictures,
  importPrivateMessageAssign,
  importSystemMessage,
  importSystemMessagePictures,
  importSystemMessageAssign,
  importDailyPictures,
  importDailyAssign
} from '@api/post.js'
const path = require('path')

export default {
  data () {
    return {
      uploadType: '',
      uploadList: []
    }
  },
  computed: {
    accept () {
      switch (this.uploadType) {
        case 'privateMessage':
        case 'privateMessageAssign':
        case 'systemMessage':
        case 'systemMessageAssign':
        case 'dailyAssign':
          return '.csv'
        case 'privateMessagePictures':
        case 'systemMessagePictures':
        case 'dailyPictures':
          return '.zip'
        default:
          return ''
      }
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
          href = '/api/user/export_user'
          break
        case 'privateMessage':
          href = 'http://ysj_5.soulfar.com/static/templates/private_message_pool.csv'
          break
        case 'privateMessageAssign':
          href = 'http://ysj_5.soulfar.com/static/templates/private_message_assign.csv'
          break
        case 'systemMessage':
          href = 'http://ysj_5.soulfar.com/static/templates/system_message_pool.csv'
          break
        case 'systemMessageAssign':
          href = 'http://ysj_5.soulfar.com/static/templates/system_message_assign.csv'
          break
        case 'dailyAssign':
          href = 'http://ysj_5.soulfar.com/static/templates/daily_poll_assign.csv'
          break
        default:
          break
      }
      window.location.href = href
    },
    upload (type) {
      this.uploadType = type
      this.$nextTick(() => {
        this.$refs.fileInput.click()
      })
    },
    async uploadFile (e) {
      const file = e.target.files[0]

      if (path.extname(file.name) === this.accept) {
        const fileForm = new FormData()
        fileForm.append('file', file)

        const id = new Date().getTime()
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
              res = await importPrivateMessage(fileForm, { onUploadProgress })
              break
            case 'privateMessagePictures':
              res = await importPrivateMessagePictures(fileForm, { onUploadProgress })
              break
            case 'privateMessageAssign':
              res = await importPrivateMessageAssign(fileForm, { onUploadProgress })
              break
            case 'systemMessage':
              res = await importSystemMessage(fileForm, { onUploadProgress })
              break
            case 'systemMessagePictures':
              res = await importSystemMessagePictures(fileForm, { onUploadProgress })
              break
            case 'systemMessageAssign':
              res = await importSystemMessageAssign(fileForm, { onUploadProgress })
              break
            case 'dailyPictures':
              res = await importDailyPictures(fileForm, { onUploadProgress })
              break
            case 'dailyAssign':
              res = await importDailyAssign(fileForm, { onUploadProgress })
              break
            default:
              break
          }

          if (res.data.result_code === 2000) {
            this.uploadList.splice(index, 1, Object.assign(item, { status: 'success' }))
          } else {
            this.uploadList.splice(index, 1, Object.assign(item, { status: 'warning' }))
            this.$message.error(res.data.result_msg)
          }
        } catch {
          this.uploadList.splice(index, 1, Object.assign(item, { status: 'exception' }))
        }
      } else {
        this.$message.error(`Please upload ${this.accept} file.`)
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

.el-button
  height 40px
  padding 0 20px

  .fa-icon
    margin-right 5px
    height 14px

.uploadBtns
  display flex
  width 850px
  margin 0 auto 25px

  .el-button
    margin-bottom 8px

.uploadType
  width 150px
  line-height 40px

.btn-box
  margin-right 10px

  a
    color #409eff

    &:hover
      cursor pointer
      text-decoration underline

.uploadList
  width 350px
  margin 35px auto 0

  li
    margin-bottom 8px
    font-size 14px
</style>
