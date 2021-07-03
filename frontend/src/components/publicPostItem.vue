<template>
  <div class="moments-item">
    <div class="moments-item-content">
      <el-avatar
        :size="40"
        :src="item.user.avatar ? item.user.avatar : ''"
        :icon="item.user.avatar ? '' : 'el-icon-user-solid'"
        class="user-portrait" />
      <div class="moment-text">
        <div>
          <span class="user-name">{{ item.user.nickname }}</span>
          <span v-if="item.isShared" class="shared-tip">shared:</span>
          <span class="moment-time">{{ item.time }}</span>
        </div>
        <div>
          <p class="post-title">{{ item.title }}</p>
          <p class="post-content">{{ item.content }}</p>
          <div v-if="item.isShared" class="moments-item-content shared-box">
            <el-avatar
              :size="40"
              :src="item.postSource.user.avatar ? item.postSource.user.avatar : ''"
              :icon="item.postSource.user.avatar ? '' : 'el-icon-user-solid'"
              class="user-portrait" />
            <div class="moment-text">
              <div>
                <span class="user-name">{{ item.postSource.user.nickname }}</span>
                <span class="moment-time">{{ item.postSource.time }}</span>
              </div>
              <div>
                <p class="post-title">{{ item.postSource.title }}</p>
                <p class="post-content">{{ item.postSource.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="moment-actions">
      <!-- <button @click="factcheck(item)" :class="{ done: item.factcheck }"><v-icon name="exclamation-circle" /></button> -->
      <span class="count" v-if="item.comments.length > 0">{{ item.comments.length }}</span>
      <button @click="showComments = !showComments"><v-icon name="comment-dots" /></button>
      <!-- <span class="count">{{ item.dislikeCount }}</span>
      <button @click="like(item, 0)" :class="{ done: item.disliked }">
        <v-icon :name="item.disliked ? 'thumbs-down' : 'regular/thumbs-down'" />
      </button> -->
      <span class="count">{{ item.flagCount }}</span>
      <button @click="flag(item)" :class="{ done: item.flagged }">
        <v-icon :name="item.flagged ? 'flag' : 'regular/flag'" />
      </button>
      <span class="count">{{ item.likeCount }}</span>
      <button @click="like(item, 1)" :class="{ done: item.liked }">
        <v-icon :name="item.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
      </button>
    </div>
    <div v-show="showComments" class="comments-box">
      <ul>
        <li class="comment-item" v-for="comment in item.comments" :key="comment.id">
          <div class="comment-item-content">
            <el-avatar
              :size="32"
              :src="comment.user.avatar ? comment.user.avatar : ''"
              :icon="comment.user.avatar ? '' : 'el-icon-user-solid'"
              class="user-portrait" />
            <div class="comment-text">
              <div>
                <span class="user-name">{{ comment.user.nickname }}</span>
                <span class="comment-time">{{ comment.created_at }}</span>
              </div>
              <p>{{ comment.comment_content }}</p>
            </div>
          </div>
        </li>
      </ul>

      <div class="post-comment">
        <el-avatar
          :size="32"
          :src="user.avatar ? user.avatar : ''"
          :icon="user.avatar ? '' : 'el-icon-user-solid'"
          class="user-portrait" />
        <div class="post-comment-input-box">
          <input
            v-model="comment_content"
            placeholder="Write a comment..."
            class="post-comment-input"
            @keyup.enter="postComment(item.id)" />
          <p>Press Enter to post.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import 'vue-awesome/icons/flag'
import 'vue-awesome/icons/regular/flag'
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
import 'vue-awesome/icons/thumbs-down'
import 'vue-awesome/icons/regular/thumbs-down'
import 'vue-awesome/icons/comment-dots'
import 'vue-awesome/icons/exclamation-circle'
import {
  // flagPost,
  // deleteFlag,
  likePost,
  deleteLike,
  changeLike,
  commentPost,
  deleteComment,
  checkPost,
  deleteCheck
} from '@api/post'

export default {
  props: {
    item: {
      type: Object,
      required: true
    },
    isTopic: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      showComments: false,
      comment_content: ''
    }
  },
  computed: mapState(['user']),
  methods: {
    async flag(item) {
      if (item.flagged) {
        await deleteFlag(item.flagged.id)
      } else {
        await flagPost(item.id)
      }
      this.$emit('action-success', {
        id: item.id,
        isTopic: this.isTopic
      })
    },
    async like(item, type) {
      if (item.liked === null && item.disliked === null) { // 初次赞或踩
        await likePost({
          like_or_not: type,
          post_id: item.id
        })
      } else {
        if (type === 1) { // 赞
          if (item.liked) { // 如果已经赞了
            await deleteLike(item.liked.id)
          } else if (item.disliked) { // 如果已经踩了
            await changeLike(item.disliked.id, { like_or_not: type })
          }
        } else { // 踩
          if (item.liked) { // 如果已经赞了
            await changeLike(item.liked.id, { like_or_not: type })
          } else if (item.disliked) { // 如果已经踩了
            await deleteLike(item.disliked.id)
          }
        }
      }
      this.$emit('action-success', {
        id: item.id,
        isTopic: this.isTopic
      })
    },
    postComment (id) {
      commentPost({
        comment_content: this.comment_content,
        post_id: id
      }).then(() => {
        this.$emit('action-success', {
          id,
          isTopic: this.isTopic
        })
        this.comment_content = ''
      })
    },
    deleteComment(momentid, commentid) {
      deleteComment(commentid).then(() => {
        this.$emit('action-success', {
          id: momentid,
          isTopic: this.isTopic
        })
      })
    },
    async factcheck(item) {
      item.factcheck = item.factcheck ? null : {}
      if (item.factcheck) {
        await deleteCheck(item.factcheck.id)
      } else {
        await checkPost({ post_id: item.id })
      }
      this.$emit('action-success', {
        id: item.id,
        isTopic: this.isTopic
      })
    }
  }
}
</script>

<style lang="stylus">
.moments-item
  padding 10px

  &-content
    display flex

  .user-portrait
    margin-right 12px

  .moment-text
    flex 1

    .user-name
      display inline-block
      height 24px
      font-size 18px
      line-height 24px

    .shared-tip
      font-weight 900
      margin-left 12px
      font-size 18px

    .moment-time
      float right
      color #666
      font-size 14px
      line-height 24px

    p
      margin-top 3px
      line-height 1.5

    .post-title
      font-weight 600

    .post-content
      font-size 14px

  .moment-actions
    height 30px
    display flex
    flex-direction row-reverse

    button
      padding 0 8px
      height 24px
      color #909399

      &:hover
        color #409eff

      &.done
        color #409eff

    .count
      margin-right 8px

  .comments-box
    border-top 1px solid #e4e7ed
    padding 8px

  .comment-item
    padding 8px 0

    .comment-item-content
      display flex

    .comment-text
      flex 1
      padding 10px
      background-color #f0f2f5
      border-radius 8px

      .user-name
        font-size 16px
        line-height 22px

      .comment-time
        float right
        color #666
        font-size 12px
        line-height 22px

      p
        line-height 1.5
        font-size 14px

.shared-box
  border 1px solid #e4e7ed
  border-radius 4px
  padding 5px
  margin 5px 0

.post-comment
  display flex

  &-input-box
    flex 1

    p
      font-size 12px

  &-input
    width calc(100% - 24px)
    height 36px
    background-color #f0f2f5
    border-radius 18px
    border 0
    padding 0 12px
    outline none
</style>
