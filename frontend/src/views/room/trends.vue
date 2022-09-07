<template>
  <el-card id="trends">
    <h2
      class="module-title topic-title"
      :class="{ fixed: titleFixed }"
      :style="{ width: titleWidth }"
      @click="handleSkip"
    >Trends</h2>

    <div v-for="(item, index) in topicList" :key="item.id" class="topic-item">
      <p class="message-title">
        <highlight :content="item.post_title" />
      </p>
      <p class="message-content">
        <highlight :content="item.abstract" />
        <span class="seeMore-btn" @click="showDetail(item.id)">See more</span>
      </p>
      <img v-if="item.photo_uri" :src="item.photo_uri" class="post-photo" />
      <div class="actions">
        <span class="message-time">{{ formatDate(item.created_at) }}</span>
        <div class="moment-actions">
          <span class="count" v-if="item.comments.length > 0">{{ item.comments.length }}</span>
          <button @click="toggleShowMoreComments(index)"><v-icon name="comment-dots" /></button>
          <span class="count">{{ item.flags.count }}</span>
          <button @click="flag(item)" :class="{ done: item.flagged }">
            <v-icon :name="item.flagged ? 'flag' : 'regular/flag'" />
          </button>
          <span class="count">{{ item.likes.count }}</span>
          <button @click="like(item)" :class="{ done: item.liked }">
            <v-icon :name="item.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
          </button>
        </div>
      </div>

      <comments ref="comments" :comments="item.comments" :post-id="item.id" @action-success="updateTopic" />
    </div>
  </el-card>
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
    comments
  },
  data () {
    return {
      topicList: [],
      titleFixed: false,
      titleWidth: '100%'
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
        this.topicList = data.data.filter(item => item.topic === this.currentTopic)

        if (this.topicList.length === 0) {
          this.titleFixed = false
        }
      })
    },
    updateTopic (id) {
      const index = this.topicList.findIndex(ele => ele.id === id)
      if (index > -1) {
        getPost(id).then(res => {
          this.topicList.splice(index, 1, res.data.data)
        })
      }
    },
    showDetail (id) {
      this.$bus.$emit('show-post-detail', id)
    },
    flag(item) {
      this.$confirm(`Are you sure to ${item.flagged ? 'unflag ' : 'flag'} this post?`, '', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async () => {
        if (item.flagged) {
          await deleteFlag(item.flagged.id)
        } else {
          await flagPost(item.id).then(res => {
            if (res.data.result_code === 2000) {
              this.$message.success('You\'ve flagged the post, you can cancel it by reclicking the flag button.')
            }
          })
        }
        this.updateTopic(item.id)
      }).catch(_ => {})
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
      if (this.topicList[index].comments.length > 2) {
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
    erd.listenTo(document.getElementById('trends'), element => {
      this.titleWidth = element.offsetWidth + 'px'
    })

    this.$bus.$on('room-content-scroll', top => {
      // 滚动到标题位置时，将标题定位
      if (this.topicList.length > 0 && top >= 183) {
        this.titleFixed = true
      } else {
        this.titleFixed = false
      }
    })
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.topicList = []
        this.updateTopicList()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
#trends
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

.topic-item
  padding 20px
  border-bottom 1px solid #dcdfe6

  &:last-child
    border-bottom 0

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
