<template>
  <el-dialog
    :visible.sync="showDetailDialog"
    width="70%"
    class="detail-dialog">
    <div v-loading="detailLoading">
      <div class="header">
        <div class="title">
          <h2 class="nyt-title">
            <highlight :content="detailData.post_title" />
          </h2>
          <p class="createAt">{{ detailData.created_at }}</p>
        </div>

        <!-- <el-button
          v-if="detailData.timeline_type === 1"
          size="mini"
          @click="share">
          Share
        </el-button> -->
      </div>

      <img v-if="detailData.photo_uri" :src="detailData.photo_uri.medium" />
      <p class="nyt-content">
        <highlight :content="detailData.post_content" />
      </p>
    </div>
  </el-dialog>
</template>

<script>
import highlight from '@components/highlight'
import { formatDate } from '@assets/utils.js'
import { getPrivatePostDetail } from '@api/post'

export default {
  components: {
    highlight
  },
  data () {
    return {
      showDetailDialog: false,
      detailLoading: true,
      detailData: {}
    }
  },
  methods: {
    showDetail (id) {
      this.showDetailDialog = true
      this.detailLoading = true
      getPrivatePostDetail(id).then(({ data }) => {
        this.detailLoading = false
        this.detailData = data.data
        Object.assign(this.detailData, {
          created_at: formatDate(data.data.created_at)
        })
      })
    },
    share () {
      this.showDetailDialog = false
      this.$bus.$emit('share', this.detailData.id)
    }
  },
  mounted () {
    this.$bus.$on('show-post-detail', id => {
      this.showDetail(id)
    })
  },
  watch: {
    showDetailDialog (show) {
      if (!show) {
        this.detailData = {}
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
