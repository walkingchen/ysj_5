<template>
  <el-card v-if="imgUrl" id="dailyPoll">
    <h2 class="module-title">Poll Digest</h2>
    <div class="img-box">
      <img ref="img" :src="imgUrl" />
    </div>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'
import { getDailyPoll } from '@api/post.js'

export default {
  data () {
    return {
      imgUrl: ''
    }
  },
  computed: mapState(['currentTopic']),
  methods: {
    updateDailyPoll () {
      getDailyPoll(localStorage.getItem('roomid'), this.currentTopic).then(({ data }) => {
        if (data.data && data.data.photo_uri) {
          this.imgUrl = data.data.photo_uri

          this.$nextTick(() => {
            this.$refs.img.onload = () => {
              this.$bus.$emit('dailyPollImgLoaded')
            }
          })
        }
      })
    }
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.imgUrl = ''
        this.updateDailyPoll()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
#dailyPoll
  border 0
  margin-bottom 20px
  border-top-right-radius 0
  border-top-left-radius 0

  .module-title
    color #fff
    background-color #5a77a1
    position fixed
    z-index 11
    width calc(22.5% - 58px) // 侧边宽度calc(22.5% - 18px) - 40px的左右内边距
    top 229px // 229px = 70px的头部高度 + 20px与头部的边距 + 119px logo的高度 + 20px与logo的边距
    border-top-right-radius 4px
    border-top-left-radius 4px

  .img-box

  img
    max-width 100%
    max-height 100%
</style>
