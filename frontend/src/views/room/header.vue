<template>
  <header style="z-index: 999">
    <div class="layout">
      <div>
        <el-button type="text" @click="handleLogout">
          <v-icon name="sign-out-alt" />
        </el-button>

        <!-- <el-input
          placeholder="Search..."
          prefix-icon="el-icon-search"
          v-model="searchKey"
          @change="handleChangeSearchKey">
        </el-input> -->

        <div class="topics-box">
          <el-badge v-for="(item, index) in _topics" :key="item" :is-dot="item !== currentTopic && hasNew[index]">
            <span
              class="day-tag"
              :class="{ actived: item === currentTopic }"
              @click="changeTopic(item, index)"
            >Day {{ item }}</span>
          </el-badge>
        </div>
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
    _topics () {
      return this.topics.map(ele => ele.topic)
    },
    ...mapState([
      'topics',
      'currentTopic'
    ])
  },
  methods: {
    changeTopic (topic, index) {
      this.$store.commit('setCurrentTopic', topic)
      this.hasNew.splice(index, 1, false)
    },
    handleChangeSearchKey () {
      this.$store.commit('setSearchKey', this.searchKey)
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
        this.hasNew.splice(this._topics.indexOf(data.topic), 1, true)
      }
    })
    this.$bus.$on('new_comment', data => {
      if (data.topic !== this.currentTopic) {
        this.hasNew.splice(this._topics.indexOf(data.topic), 1, true)
      }
    })
  },
  watch: {
    topics: {
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
  height 70px
  box-shadow 0 2px 3px rgba(0,0,0,.08)
  position relative
  z-index 1

  .layout > div
    height 70px
    display flex
    align-items center
    justify-content space-between

.topics-box
  flex 1
  display flex
  justify-content space-between

  .day-tag
    display inline-block
    text-align center
    cursor pointer
    font-size 20px
    height 38px
    line-height 38px
    padding 0 25px
    background-color #ecf5ff
    border-radius 19px
    color #409eff
    transition .2s

    &:hover, &.actived
      background-color #409eff
      color #fff

.el-input
  width 250px
  margin 0 50px 0 20px
</style>
