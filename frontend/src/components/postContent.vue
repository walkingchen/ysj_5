<template>
  <div>
    <p>
      {{ _content }}
      <span v-if="long" class="seeMore" @click="showDetail">See More</span>
    </p>

    <el-dialog
      v-if="long"
      :visible.sync="showDetailDialog"
      center
      width="70%"
      class="detail-dialog">
      <div v-loading="detailLoading">
        <h2>{{ detailData.post_title }}</h2>
        <p class="createAt">{{ detailData.created_at }}</p>
        <div v-if="detailData.photo_uri" class="image-box">
          <img :src="detailData.photo_uri.medium" />
        </div>
        <p class="content">{{ detailData.post_content }}</p>
      </div>
      <span v-if="detailData.timeline_type === 1 && !isTopic" slot="footer" class="dialog-footer">
        <el-button size="small" icon="el-icon-share" @click="$emit('share')">Share</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { formatDate } from '@assets/utils.js'
import { getPost } from '@api/post'

export default {
  props: {
    content: {
      type: Object,
      required: true
    },
    id: Number,
    isTopic: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      showDetailDialog: false,
      detailLoading: true,
      detailData: {}
    }
  },
  computed: {
    long () {
      return this.content.length > 130
    },
    _content () {
      return this.long ? this.content.substring(0, 130) + '...' : this.content
    }
  },
  methods: {
    showDetail () {
      this.showDetailDialog = true
      this.detailLoading = true
      getPost(this.id).then(({ data }) => {
        this.detailLoading = false
        this.detailData = data.data
        Object.assign(this.detailData, {
          created_at: formatDate(data.data.created_at)
        })
      })
    }
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
p
  font-size 14px
  line-height 1.5
  white-space pre-wrap

  .seeMore
    cursor pointer
    font-weight 700
    margin-left 5px

    &:hover
      text-decoration underline

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

  h2
    text-align center

  .createAt
    text-align center
    color #999
    font-size 14px
    padding 8px 0

  .image-box
    display flex
    justify-content center
    align-items center
    padding 8px 0
    margin-bottom 10px

    img
      width auto
      max-width 100%
      max-height 300px
      display block
      margin 0 auto

  .content
    font-size 16px
</style>
