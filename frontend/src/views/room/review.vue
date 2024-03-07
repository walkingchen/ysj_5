<template>
  <div>
    <el-card id="review">
    <h2
      class="module-title topic-title"
      :class="{ fixed: titleFixed }"
      :style="{ width: titleWidth }"
      @click="handleSkip"
    >COVID Flashbacks: Top Shares</h2>

    <div v-for="(item, index) in postList" :key="item.id + index" class="trend-item">
      <div class="flag-box">
        <button @click="flag(item)" style="display: flex; align-items: center;">
          <!-- <v-icon name="regular/flag" v-if="!item.flagged" style="fill:#409eef; margin-right: 5px;" height="12" width="12"/> -->
          <!-- {{ item.flagged ? 'unflag this post' : 'Report' }}  -->
          <v-icon :name="item.flagged ? 'flag' : 'regular/flag'" style="fill:#409eef; margin-right: 5px;" height="12" width="12"/>
          <span>{{ item.flagged ? 'Reported' : 'Report' }}</span>
        </button>
      </div>

      <p class="message-title serif-font">
        <highlight :content="item.post_title" />
      </p>
      <p class="message-content serif-font">
        <highlight :content="item.abstract" />
      </p>
      <img v-if="item.photo_uri" :src="item.photo_uri.small" class="post-photo" />

      <div class="actions">
        <span class="message-time">{{ formatDate(item.created_at) }}</span>
        <div class="moment-actions">
          <button @click="toggleShowMoreComments(index)"><v-icon name="comment-dots" /></button>
          <span class="count" v-if="item.comments.length > 0">{{ item.comments.length }}</span>
          <button @click="like(item)" :class="{ done: item.liked }">
            <v-icon :name="item.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
          </button>
          <span class="count">{{ item.likes.count }}</span>
        </div>
      </div>

      <comments ref="comments" :comments="item.comments" :post-id="item.id" @action-success="updateTopic" />
    </div>
  </el-card>
    <flag-dialog ref="flagDialog" @handleSubmit="handleSubmit" :selectItem="selectItem"/>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import elementResizeDetectorMaker from 'element-resize-detector'
import 'vue-awesome/icons/flag'
import 'vue-awesome/icons/regular/flag'
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
import 'vue-awesome/icons/comment-dots'
import highlight from '@components/highlight'
import comments from '@components/comments'
import { formatDate } from '@assets/utils.js'
import FlagDialog from '../../components/flagDialog.vue'
import {
  getTopicContent,
  getPost,
  flagPost,
  deleteFlag,
  likePost,
  deleteLike
} from '@api/post'

export default {
  components: {
    highlight,
    comments,
    FlagDialog
  },
  data () {
    return {
      postList: [],
      titleFixed: false,
      titleWidth: '100%',
      selectItem: {}
    }
  },
  computed: mapState(['currentTopic']),
  methods: {
    formatDate (date) {
      return formatDate(date)
    },
    handleSkip () {
      document.getElementsByClassName('room-content')[0].scrollTop = 180
    },
    updateTopicList () {
      getTopicContent(localStorage.getItem('roomid'), this.currentTopic).then(({ data }) => {
        this.postList = data.data.filter(item => item.topic === this.currentTopic)
      })
    },
    updateTopic (id) {
      const index = this.postList.findIndex(ele => ele.id === id)
      if (index > -1) {
        getPost(id).then(res => {
          this.postList.splice(index, 1, res.data.data)
        })
      }
    },
    flag(item) {
      // this.$confirm(`Are you sure to ${item.flagged ? 'unflag ' : 'flag'} this post?`, '', {
      //   confirmButtonText: 'OK',
      //   cancelButtonText: 'Cancel',
      //   type: 'warning'
      // }).then(async () => {
      //   if (item.flagged) {
      //     await deleteFlag(item.flagged.id)
      //   } else {
      //     await flagPost(item.id).then(res => {
      //       if (res.data.result_code === 2000) {
      //         this.$message.success('You\'ve flagged the post, you can cancel it by reclicking the flag button.')
      //       }
      //     })
      //   }
      //   this.updateTopic(item.id)
      // }).catch(_ => {})

      if (item.flagged) {
        // this.$confirm(`Are you sure to ${item.flagged ? 'unflag ' : 'flag'} this post?`, '', {
        // confirmButtonText: 'OK',
        // cancelButtonText: 'Cancel',
        // type: 'warning'
        // }).then(async () => {
        //   await deleteFlag(item.flagged.id)
        //   this.updateTopic(item.id)
        // }).catch(_ => {})
      } else {
        this.$refs.flagDialog.dialogVisible = true
        this.selectItem = item
      }
    },
    async handleSubmit (data) {
      let params = {
        post_id: data.item.id,
        flag_content: data.selectTag
      }
      await flagPost(params).then(res => {
        if (res.data.result_code === 2000) {
          // this.$message.success('You\'ve flagged the post, you can cancel it by reclicking the flag button.')
          this.$message.success('You\'ve reported the post.')
        }
      })
      this.updateTopic(data.item.id)
    },
    async like(item) {
      if (item.liked) { // 已经赞了
        await deleteLike(item.liked.id)
      } else {
        await likePost({
          like_or_not: 1,
          post_id: item.id
        })
      }
      this.updateTopic(item.id)
    },
    toggleShowMoreComments (index) {
      if (this.postList[index].comments.length > 2) {
        this.$refs.comments[index].toggleShowMoreComments()
      }
    }
  },
  mounted () {
    this.$bus.$on('new_comment', data => {
      if (data.topic === this.currentTopic) {
        this.updateTopic(data.post_id)
      }
    })

    // 处理标题栏宽度
    const erd = elementResizeDetectorMaker()
    erd.listenTo(document.getElementById('review'), element => {
      this.titleWidth = window.getComputedStyle(element).getPropertyValue('width')
    })

    this.$bus.$on('room-content-scroll', top => {
      // 滚动到标题位置时，将标题定位
      if (top >= 183) {
        this.titleFixed = true
      } else {
        this.titleFixed = false
      }
    })
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.postList = []
        this.updateTopicList()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
#review
  border 0

  >>> .el-card__body
    padding-top var(--module-title-height)
    position relative

  .topic-title
    background-color #5a77a1
    color #fff
    box-sizing border-box
    position absolute
    top 0

    &.fixed
      top 70px

.trend-item
  padding 20px
  border-bottom 1px solid #dcdfe6

  &:last-child
    border-bottom 0

  .flag-box
    display flex
    justify-content end
    margin-bottom 15px

    button
      background-color #eef0f3
      color #409eef
      height 30px
      padding 0 30px
      border-radius 15px

      &:hover
        opacity .8

  .actions
    display flex
    align-items center
    justify-content space-between
    padding 10px 0

  .message-time
    color #999
    font-size 14px
    line-height 24px
    display inline-block
</style>
