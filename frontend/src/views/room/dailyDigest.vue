<template>
  <el-card class="dailyDigest-layout">
    <title-com title="Daily poll results" />
    <div class="img-box">
      <img :src="imgUrl" />
    </div>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'
import titleCom from '@components/title'
import { getDailyPoll } from '@api/post.js'

export default {
  components: {
    titleCom
  },
  data () {
    return {
      imgUrl: ''
    }
  },
  computed: mapState(['currentTopic']),
  methods: {
    updateDailyPoll () {
      getDailyPoll(localStorage.getItem('roomid'), this.currentTopic).then(({ data }) => {
        this.imgUrl = data.data.photo_uri
      })
    }
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.topicList = []
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
