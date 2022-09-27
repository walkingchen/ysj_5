<template>
  <el-dialog
    :visible.sync="showDetailDialog"
    width="70%"
    class="detail-dialog">
    <div v-loading="getPostDetailLoading">
      <div class="header">
        <div class="title">
          <h2 class="nyt-title">
            <highlight :content="postDetailData.post_title" />
          </h2>
          <p class="createAt">{{ postDetailData.created_at }}</p>
        </div>

        <!-- <el-button
          v-if="postDetailData.timeline_type === 1"
          size="mini"
          @click="share">
          Share
        </el-button> -->
      </div>

      <img v-if="postDetailData.photo_uri" :src="postDetailData.photo_uri.medium" />
      <p class="nyt-content">
        <highlight :content="postDetailData.post_content" />
      </p>
    </div>
  </el-dialog>
</template>

<script>
import { mapState } from 'vuex'
import highlight from '@components/highlight'

export default {
  components: {
    highlight
  },
  data () {
    return {
      showDetailDialog: false
    }
  },
  computed: mapState([
    'getPostDetailLoading',
    'postDetailData'
  ]),
  methods: {
    share () {
      this.showDetailDialog = false
      this.$bus.$emit('share', this.postDetailData.id)
    }
  },
  mounted () {
    this.$bus.$on('show-post-detail', () => {
      this.showDetailDialog = true
    })
  },
  watch: {
    showDetailDialog (show) {
      if (!show) {
        this.$store.commit('setPostDetail', {})
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.detail-dialog
  >>> .el-dialog
    padding-bottom 20px

  >>> .el-dialog__header
    padding 0

  >>> .el-dialog__headerbtn
    top 10px
    right 10px

  >>> .el-dialog__body
    padding-bottom 10px

  >>> .el-dialog__footer
    padding-bottom 0

  .header
    display flex
    align-items flex-start

    .title
      flex 1
      width 0

    h2
      text-align center

    .createAt
      text-align center
      color #999
      font-size 14px
      padding 8px 0

  img
    display block
    margin 0 auto
    max-width 100%
    margin-bottom 10px
</style>
