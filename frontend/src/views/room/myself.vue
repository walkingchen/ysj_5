<template>
  <div class="myself-box" :style="{ height: height + 'px' }">
    <el-avatar
      :size="45"
      :src="user.avatar ? user.avatar : ''"
      :icon="user.avatar ? '' : 'el-icon-user-solid'"
    />
    <p>{{ user.nickname }}</p>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import elementResizeDetectorMaker from 'element-resize-detector'

export default {
  data() {
    return {
      height: 158
    }
  },
  computed: mapState(['user']),
  mounted () {
    this.height = document.getElementById('addDiscussion').offsetHeight

    // 监听 add discussion dom 高度变化
    elementResizeDetectorMaker().listenTo(document.getElementById('addDiscussion'), el => {
      this.height = el.offsetHeight
    })
  }
}
</script>

<style lang="stylus" scoped>
.myself-box
  background-color #658864
  color #fff
  border-radius 4px
  display flex
  align-items center
  justify-content center
  margin-bottom 20px

  .el-avatar
    // box-shadow 5px 0 5px #333

  p
    font-size 24px
    margin-left 15px
    // text-shadow 4px 0 5px #333
</style>
