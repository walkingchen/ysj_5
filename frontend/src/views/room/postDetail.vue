<template>
  <el-dialog
    :visible.sync="showDetailDialog"
    width="70%"
    class="detail-dialog">
    <el-button
      v-if="detailData.timeline_type !== 0"
      size="small"
      icon="el-icon-share"
      class="share-btn"
      :disabled="detailData.timeline_type === 2"
      @click="share"
    >Share</el-button>
    <div v-loading="detailLoading">
      <h2>{{ detailData.post_title }}</h2>
      <p class="createAt">{{ detailData.created_at }}</p>
      <img v-if="detailData.photo_uri" :src="detailData.photo_uri.medium" />
      <p class="content">{{ detailData.post_content }}</p>
    </div>
  </el-dialog>
</template>

<script>
import { formatDate } from '@assets/utils.js'
import { getPost } from '@api/post'

export default {
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
      getPost(id).then(({ data }) => {
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

  .share-btn
    position absolute
    right 10px
    top 34px

  h2
    text-align center

  .createAt
    text-align center
    color #999
    font-size 14px
    padding 8px 0

  img
    margin 0 auto
    max-width 100%
    margin-bottom 10px

  .content
    font-size 16px
</style>
