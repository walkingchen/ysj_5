<template>
  <el-card shadow="hover" class="moments-item">
    <div class="moments-item-content">
      <el-avatar
        shape="square"
        :size="50"
        :src="item.user.avatar ? item.user.avatar : ''"
        :icon="item.user.avatar ? '' : 'el-icon-user-solid'"
        class="user-portrait" />
      <div class="moment-text">
        <div>
          <span class="user-name">{{ item.user.nickname }}</span>
          <span class="moment-time">{{ item.time }}</span>
        </div>
        <div v-if="item.isShared" class="moments-item-content shared-box">
          <el-avatar
            shape="square"
            :size="30"
            :src="item.postSource.user.avatar ? item.postSource.user.avatar : ''"
            :icon="item.postSource.user.avatar ? '' : 'el-icon-user-solid'"
            class="user-portrait" />
          <div class="moment-text">
            <div>
              <span class="user-name">{{ item.postSource.user.nickname }}</span>
              <span class="moment-time">{{ item.postSource.time }}</span>
            </div>
            <div>
              <p>{{ item.postSource.title }}</p>
              <p>{{ item.postSource.content }}</p>
            </div>
          </div>
        </div>
        <div v-else>
          <p>{{ item.title }}</p>
          <p>{{ item.content }}</p>
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
      <el-input type="textarea" :rows="3" placeholder="Comment Content" v-model="comment_content" />
      <div class="commentSubmitBtn-box">
        <el-button type="primary" size="mini" @click="comment(item.id)">Submit</el-button>
      </div>

      <ul>
        <li class="comment-item" v-for="comment in item.comments" :key="comment.id">
          <div class="comment-item-content">
            <el-avatar
              :size="35"
              :src="comment.user.avatar ? comment.user.avatar : ''"
              :icon="comment.user.avatar ? '' : 'el-icon-user-solid'"
              shape="square"
              class="user-portrait" />
            <div class="comment-text">
              <div>
                <span class="user-name">{{ comment.user.nickname }}</span>
                <span class="comment-time">{{ comment.time }}</span>
                <button
                  v-if="comment.user_id === userid || item.user_id === userid"
                  class="comment-delete-btn"
                  @click="deleteComment(item.id, comment.id)">
                  <i class="el-icon-delete"></i>
                </button>
              </div>
              <p>{{ comment.comment_content }}</p>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </el-card>
</template>

<script>
import 'vue-awesome/icons/flag'
import 'vue-awesome/icons/regular/flag'
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
import 'vue-awesome/icons/thumbs-down'
import 'vue-awesome/icons/regular/thumbs-down'
import 'vue-awesome/icons/comment-dots'
import 'vue-awesome/icons/exclamation-circle'
import {
  flagPost,
  deleteFlag,
  likePost,
  deleteLike,
  changeLike,
  commentPost,
  deleteComment,
  checkPost,
  deleteCheck
} from '@api/post'

export default {
  props: ['item'],
  data () {
    return {
      showComments: false,
      comment_content: ''
    }
  },
  computed: {
    userid() {
      return this.$store.state.user.id
    }
  },
  methods: {
    async flag(item) {
      if (item.flagged) {
        await deleteFlag(item.flagged.id)
      } else {
        await flagPost(item.id)
      }
      this.$emit('action-success', item.id)
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
      this.$emit('action-success', item.id)
    },
    comment(id) {
      commentPost({
        comment_content: this.comment_content,
        post_id: id
      }).then(() => {
        this.$emit('action-success', item.id)
        this.comment_content = ''
      })
    },
    deleteComment(momentid, commentid) {
      deleteComment(commentid).then(() => {
        this.$emit('action-success', item.id)
      })
    },
    async factcheck(item) {
      if (item.factcheck) {
        await deleteCheck(item.factcheck.id)
      } else {
        await checkPost({ post_id: item.id })
      }
      this.updateMoment(item.id)
    }
  }
}
</script>

<style lang="stylus">
.moments-item
  padding 10px
  border 0

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

    .moment-time
      float right
      color #666
      font-size 14px
      line-height 24px

    p
      margin-top 3px
      line-height 1.5

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

    & > ul
      margin-top 10px

  .comment-item
    padding 8px 0

    .comment-item-content
      display flex

    .comment-text
      flex 1

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

      .comment-delete-btn
        float right
        margin-right 5px
        padding 0 8px
        height 22px
        color #909399
        display none

        &:hover
          color #409eff

    &:hover
      .comment-delete-btn
        display block

.shared-box
  border 1px solid #e4e7ed
  border-radius 4px
  padding 5px
  margin 5px 0

.commentSubmitBtn-box
  margin-top 8px
  height 28px

  button
    float right
</style>
