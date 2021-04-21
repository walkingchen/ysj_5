<template>
  <header>
    <div>
      <div class="topics-box">
        <el-tag>Topics 1</el-tag>
        <el-tag>Topics 2</el-tag>
        <el-tag>Topics 3</el-tag>
        <el-tag>Topics 4</el-tag>
      </div>

      <el-input
        placeholder="Search..."
        prefix-icon="el-icon-search"
        size="small"
        v-model="searchKey">
      </el-input>

      <div>
        <el-dropdown trigger="click" placement="bottom">
          <el-badge :value="12" :hidden="false">
            <span class="el-icon-message-solid"></span>
          </el-badge>
          <el-dropdown-menu slot="dropdown">
            <div class="notification-box">
              Notification
            </div>
          </el-dropdown-menu>
        </el-dropdown>
        <span class="separator">|</span>
        <el-button type="text" @click="handleLogout"><v-icon name="sign-out-alt" /></el-button>
      </div>
    </div>
  </header>
</template>

<script>
import { logout } from '@api/auth'

export default {
  data () {
    return {
      searchKey: ''
    }
  },
  methods: {
    handleLogout() {
      logout()
      localStorage.removeItem('roomid')
      this.socket.emit('room_leave', {
        room_id: this.roomInfo.id,
        username: this.user.username
      }, () => {
        this.socket.close()
      })
      this.$router.push({ name: 'Login' })
    }
  }
}
</script>

<style lang="stylus" scoped>
header
  background-color #f0fdda
  height 60px

  & > div
    width 1000px
    margin 0 auto
    height 60px
    display flex
    align-items center
    justify-content space-between

.topics-box
  width 400px

  .el-tag
    width 90px
    margin-right 10px
    text-align center

.el-input
  width 200px

.el-badge
  color #409eff
  cursor pointer
  font-size 16px

  &:hover
    color #66b1ff

  & >>> span
    position relative
    top -1px

.separator
  margin 0 20px
  color #999

.el-button >>> span
  position relative
  top 3px

.notification-box
  width 320px
</style>
