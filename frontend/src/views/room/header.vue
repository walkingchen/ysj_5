<template>
  <header>
    <div class="layout">
      <div>
        <div class="topics-box">
          <el-badge v-for="item in topic" :key="item" :is-dot="false">
            <el-tag
              :effect="item === currentTopic ? 'light' : 'plain'"
              @click="changeTopic(item)"
            >Topic {{ item }}</el-tag>
          </el-badge>
        </div>

        <el-input
          placeholder="Search..."
          prefix-icon="el-icon-search"
          size="small"
          v-model="searchKey">
        </el-input>

        <el-button type="text" @click="handleLogout">
          <v-icon name="sign-out-alt" />
        </el-button>
      </div>
    </div>
  </header>
</template>

<script>
import { mapState } from 'vuex'
import 'vue-awesome/icons/sign-out-alt'
import { logout } from '@api/auth'

export default {
  data () {
    return {
      searchKey: ''
    }
  },
  computed: mapState([
    'topic',
    'currentTopic'
  ]),
  methods: {
    changeTopic (topic) {
      this.$store.commit('setCurrentTopic', topic)
    },
    handleLogout() {
      logout()
      localStorage.removeItem('roomid')
      this.$emit('logout')
      this.$router.push({ name: 'Login' })
    }
  }
}
</script>

<style lang="stylus" scoped>
header
  background-color #fff
  height 60px
  box-shadow 0 2px 3px rgba(0,0,0,.08)
  position relative
  z-index 1

  .layout > div
    padding 0 100px
    height 60px
    display flex
    align-items center
    justify-content space-between

.topics-box
  width 670px
  display flex
  justify-content space-between

  .el-tag
    width 75px
    text-align center
    cursor pointer

.el-input
  width 200px
</style>
