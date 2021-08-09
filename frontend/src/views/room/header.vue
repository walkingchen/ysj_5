<template>
  <header>
    <div class="layout">
      <div>
        <div class="topics-box">
          <el-badge v-for="(item, index) in _topic" :key="item" :is-dot="item !== currentTopic && hasNew[index]">
            <el-tag
              :effect="item === currentTopic ? 'light' : 'plain'"
              @click="changeTopic(item, index)"
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
      hasNew: [],
      searchKey: ''
    }
  },
  computed: {
    _topic () {
      return this.topic.map(ele => ele.topic)
    },
    ...mapState([
      'topic',
      'currentTopic'
    ])
  },
  methods: {
    changeTopic (topic, index) {
      this.$store.commit('setCurrentTopic', topic)
      this.hasNew.splice(index, 1, false)
    },
    handleLogout() {
      logout()
      this.$store.commit('setCurrentTopic', null)
      localStorage.removeItem('roomid')
      this.$emit('logout')
      this.$router.push({ name: 'Login' })
    }
  },
  mounted () {
    this.$bus.$on('new_post', data => {
      if (data.topic !== this.currentTopic) {
        this.hasNew.splice(this.topic.indexOf(data.topic), 1, true)
      }
    })
    this.$bus.$on('new_comment', data => {
      if (data.topic !== this.currentTopic) {
        this.hasNew.splice(this.topic.indexOf(data.topic), 1, true)
      }
    })
  },
  watch: {
    topic: {
      handler (val) {
        this.hasNew = val.map(ele => ele.redspot)
      },
      immediate: true
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
