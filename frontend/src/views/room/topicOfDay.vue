<template>
  <el-card id="topicOfDay">
    <h2
      class="module-title topic-title"
      :class="{ fixed: titleFixed }"
      :style="{ width: titleWidth }"
      @click="handleSkip"
    >Topic of the Day</h2>

    <div v-for="(item, index) in topicList" :key="item.id" class="topic-item">
      <private-post-item :item="item">
        <template #actions>
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
        </template>
      </private-post-item>

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
import privatePostItem from '@components/privatePostItem'
import comments from '@components/comments'
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
    privatePostItem,
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
    handleSkip () {
      document.getElementsByClassName('room-content')[0].scrollTop = 180
    },
    updateTopicList () {
      getTopicContent(localStorage.getItem('roomid'), this.currentTopic).then(({ data }) => {
        this.topicList = data.data

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
    erd.listenTo(document.getElementById('topicOfDay'), element => {
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
#topicOfDay
  border 0

  >>> .el-card__body
    padding-top 59px
    min-height 15px
    position relative

  .topic-title
    position absolute
    top 0
    box-sizing border-box
    padding-bottom 15px

    &.fixed
      background-color #fff
      cursor pointer
      border-bottom 1px solid #ddd
      position fixed
      top 70px
      z-index 10

      &:hover
        box-shadow rgb(192, 192, 192, 0.1) 0px 0px 10px

.topic-item
  padding 0 10px
  border-bottom 1px solid #dcdfe6

  &:last-child
    border-bottom 0
</style>
