<template>
  <el-card v-if="imgUrl" class="dailyDigest-layout">
    <h2 class="module-title">Daily poll results</h2>
    <div class="img-box">
      <img :src="imgUrl" />
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
          this.$emit('has-data')
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
.dailyDigest-layout
  border 0
  margin-bottom 20px

  .img-box
    padding 10px

  img
    max-width 100%
    max-height 100%
</style>
