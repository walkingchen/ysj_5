<template>
  <el-card v-if="imgUrl" id="dailyPoll">
    <h2 class="module-title">Daily poll</h2>
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
              console.log(22)
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
  position fixed
  z-index 10
  width calc(22.5% - 15px)
  top 90px
  right calc(5% + 5px)
  border 0

  .module-title
    border-bottom 1px solid #ebeef5

  .img-box
    padding 10px

  img
    max-width 100%
    max-height 100%
</style>
