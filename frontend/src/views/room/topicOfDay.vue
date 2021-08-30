<template>
  <el-card class="topic-layout">
    <title-com title="Topic of The Day" />

    <div v-for="(item, index) in topicList" :key="item.id" class="topic-item">
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
import titleCom from '@components/title'
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
    titleCom,
    privatePostItem,
    comments
  },
  data () {
    return {
      topicList: []
    }
  },
  computed: mapState(['currentTopic']),
  methods: {
    updateTopicList () {
      getTopicContent(localStorage.getItem('roomid'), this.currentTopic).then(({ data }) => {
        this.topicList = data.data
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
      this.$confirm(`Are you sure to ${item.flagged ? 'cancel ' : ''}flag this post?`, '', {
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
    }
  }
}
</script>

<style lang="stylus" scoped>
.topic-layout
  border 0

.topic-item
  padding 0 10px
  border-bottom 1px solid #dcdfe6

  &:last-child
    border-bottom 0
</style>
