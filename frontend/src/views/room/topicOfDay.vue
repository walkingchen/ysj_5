<template>
  <el-card class="topic-layout" id="topic-layout">
    <!-- <affix relative-element-selector="#opicLayout" :offset="{ top: 30, bottom: 40 }" :scroll-affix="false"> -->
    <h2 class="module-title" ref="moduleTitle" @click="handleSkip">Topic of the Day</h2>
    <!-- </affix> -->

    <div v-for="(item, index) in topicList" :key="item.id" class="topic-item" ref="topicItem">
      <private-post-item :item="item">
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
      </private-post-item>

      <comments ref="comments" :comments="item.comments" :post-id="item.id" @action-success="updateTopic" />
    </div>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'
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
  props: ['showLeftCol'],
  data () {
    return {
      topicList: [],
      moduleTitleWidth: 0
    }
  },
  computed: mapState(['currentTopic']),
  methods: {
    handleSkip () {
      document.getElementsByClassName('room-content')[0].scrollTop = 160
    },
    updateTopicList () {
      getTopicContent(localStorage.getItem('roomid'), this.currentTopic).then(({ data }) => {
        this.topicList = data.data
        if (this.topicList.length) {
          this.setModuleTitleTop()
        }
      })
    },
    setModuleTitleTop () {
      // 获取标题栏宽度
      this.moduleTitleWidth = document.getElementById('topic-layout').clientWidth - 40 + 'px'
      var moduleTitle = this.$refs.moduleTitle
      const that = this
      window.addEventListener('scroll', function () {
        this.scrollTop = document.getElementsByClassName('room-content')[0].scrollTop
        // console.log(this.scrollTop, '=========+.scrollTop')
        // 滚动到标题位置时，将标题定位
        if (this.scrollTop >= 178) {
          moduleTitle.setAttribute('class', 'module-title fixed-title')
          moduleTitle.style.width = that.moduleTitleWidth
          if (document.getElementsByClassName('topic-item').length) {
            const topicFrist = document.getElementsByClassName('topic-item')[0]
            topicFrist.style.marginTop = '70px'
          }
        } else {
          if (document.getElementsByClassName('fixed-title')) {
            moduleTitle.setAttribute('class', 'module-title')
            if (document.getElementsByClassName('topic-item').length) {
              const topicFrist = document.getElementsByClassName('topic-item')[0]
              topicFrist.style.marginTop = '0px'
            }
          }
        }
      }, true)
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
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.topicList = []
        this.updateTopicList()
      }
    },
    showLeftCol (val) {
      // 重新获取标题栏宽度
      this.moduleTitleWidth = document.getElementById('topic-layout').clientWidth - 40 + 'px'
    }
  }
}
</script>

<style lang="stylus" scoped>
.topic-layout
  border 0

  .module-title
    padding-bottom 15px
    &:hover
      box-shadow:rgb(192, 192, 192, 0.1) 0px 0px 10px
      cursor pointer

.topic-item
  padding 0 10px
  border-bottom 1px solid #dcdfe6

  &:last-child
    border-bottom 0

.fixed-title
  position: fixed;
  top:70px;
  background: #fff;
  z-index: 99;
  border-bottom: 1px solid #ccc;
</style>
