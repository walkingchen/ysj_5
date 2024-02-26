<template>
  <div class="moments-item" :class="{unread: _item.unread}">
    <div class="moments-item-content">
      <el-avatar
        :size="40"
        :src="_item.user.avatar ? _item.user.avatar : ''"
        :icon="_item.user.avatar ? '' : 'el-icon-user-solid'"
        class="user-portrait" />
      <div class="moment-text">
        <div class="message-header">
          <div>
            <span class="user-name">{{ _item.user.nickname }}</span>
            <span v-if="_item.isShared" class="shared-tip">shared:</span>
          </div>
          <button @click="flag(_item)" style="display: flex; align-items: center;">
            <!-- <v-icon name="regular/flag" v-if="!_item.flagged" style="fill:#409eef; margin-right: 5px;" height="12" width="12"/> -->
            <!-- <span>{{ _item.flagged ? 'unflag this post' : 'Report' }}</span> -->
            <v-icon name="regular/flag" style="fill:#409eef; margin-right: 5px;" height="12" width="12"/>
            <span>Report</span>
          </button>
        </div>
        <div>
          <p class="message-content">
            <highlight :content="_item.content" />
          </p>
          <img v-if="_item.photo_uri" :src="_item.photo_uri.small" class="post-photo" />
          <div v-if="_item.isShared" class="shared-box">
            <private-post-item v-if="_item.postSource" :item="_item.postSource" />
            <el-empty v-else description="Content deleted." :image-size="100" />
          </div>
        </div>
      </div>
    </div>
    <div class="message-footer">
      <span class="moment-time">{{ _item.time }}</span>
      <div class="moment-actions">
        <!-- <button @click="factcheck(_item)" :class="{ done: _item.factcheck }"><v-icon name="exclamation-circle" /></button> -->
        <span class="count" v-if="_item.comments.length > 0">{{ _item.comments.length }}</span>
        <button @click="toggleShowMoreComments"><v-icon name="comment-dots" /></button>
        <!-- <span class="count">{{ _item.dislikeCount }}</span>
        <button @click="like(_item, 0)" :class="{ done: _item.disliked }">
          <v-icon :name="_item.disliked ? 'thumbs-down' : 'regular/thumbs-down'" />
        </button> -->
        <!-- <span class="count">{{ _item.flagCount }}</span>
        <button @click="flag(_item)" :class="{ done: _item.flagged }">
          <v-icon :name="_item.flagged ? 'flag' : 'regular/flag'" />
        </button> -->
        <span class="count">{{ _item.likeCount }}</span>
        <button @click="like(_item)" :class="{ done: _item.liked }">
          <v-icon :name="_item.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
        </button>
      </div>
    </div>

    <comments
      ref="comments"
      :comments="_item.comments"
      :post-id="_item.id"
      style="margin-top: 10px"
      @action-success="$emit('action-success', _item.id)" />
      <flag-dialog ref="flagDialog" @handleSubmit="handleSubmit" :selectItem="selectItem"/>
  </div>
</template>

<script>
import 'vue-awesome/icons/flag'
import 'vue-awesome/icons/regular/flag'
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
// import 'vue-awesome/icons/thumbs-down'
// import 'vue-awesome/icons/regular/thumbs-down'
import 'vue-awesome/icons/comment-dots'
// import 'vue-awesome/icons/exclamation-circle'
import {
  flagPost,
  deleteFlag,
  likePost,
  deleteLike,
  // changeLike,
  checkPost,
  deleteCheck
} from '@api/post'
import highlight from './highlight'
import privatePostItem from '@components/privatePostItem'
import comments from '@components/comments'
import { formatDate } from '@assets/utils.js'
import FlagDialog from './flagDialog.vue'

export default {
  props: ['item'],
  components: {
    highlight,
    privatePostItem,
    comments,
    FlagDialog
  },
  data () {
    return {
      comment_content: '',
      selectItem: {}
    }
  },
  computed: {
    _item () {
      const item = this.item
      const _item = {
        id: item.id,
        unread: !item.read_status,
        isShared: item.post_shared_id,
        content: item.post_content,
        photo_uri: item.photo_uri,
        flagged: item.flagged,
        flagCount: item.flags.count,
        liked: item.liked,
        likeCount: item.likes.count,
        // disliked: item.disliked,
        // dislikeCount: item.dislikes.count,
        // factcheck: item.factcheck,
        time: formatDate(item.created_at),
        user: item.user,
        comments: item.comments
      }

      if (_item.isShared) {
        _item.postSource = item.post_shared
      }
      return _item
    }
  },
  methods: {
    flag(item) {
      this.$refs.flagDialog.dialogVisible = true
      this.selectItem = item
      // if (item.flagged) {
      //   this.$confirm(`Are you sure to ${item.flagged ? 'unflag ' : 'flag'} this post?`, '', {
      //   confirmButtonText: 'OK',
      //   cancelButtonText: 'Cancel',
      //   type: 'warning'
      //   }).then(async () => {
      //     await deleteFlag(item.flagged.id)
      //     this.$emit('action-success', item.id)
      //   }).catch(_ => {})
      // } else {
      //   this.$refs.flagDialog.dialogVisible = true
      //   this.selectItem = item
      // }
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
      this.$emit('action-success', data.item.id)
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
      this.$emit('action-success', item.id)
    },
    // async like(item, type) {
    //   if (item.liked === null && item.disliked === null) { // 初次赞或踩
    //     await likePost({
    //       like_or_not: type,
    //       post_id: item.id
    //     })
    //   } else {
    //     if (type === 1) { // 赞
    //       if (item.liked) { // 如果已经赞了
    //         await deleteLike(item.liked.id)
    //       } else if (item.disliked) { // 如果已经踩了
    //         await changeLike(item.disliked.id, { like_or_not: type })
    //       }
    //     } else { // 踩
    //       if (item.liked) { // 如果已经赞了
    //         await changeLike(item.liked.id, { like_or_not: type })
    //       } else if (item.disliked) { // 如果已经踩了
    //         await deleteLike(item.disliked.id)
    //       }
    //     }
    //   }
    //   this.$emit('action-success', item.id)
    // },
    async factcheck(item) {
      item.factcheck = item.factcheck ? null : {}
      if (item.factcheck) {
        await deleteCheck(item.factcheck.id)
      } else {
        await checkPost({ post_id: item.id })
      }
      this.$emit('action-success', item.id)
    },
    toggleShowMoreComments () {
      if (this.item.comments.length > 2) {
        this.$refs.comments.toggleShowMoreComments()
      }
    }
  }
}
</script>

<style lang="stylus">
.moments-item
  padding 12px 16px

  &-content
    display flex

  .user-portrait
    margin-right 12px

  .moment-text
    flex 1
    width 0
    font-size 14px

    .message-header 
      display flex
      align-items center
      justify-content space-between
      button
        float right
        background-color #eef0f3
        color #409eef
        height 30px
        padding 0 30px
        border-radius 15px

        &:hover
          opacity .8

    .user-name
      display inline-block
      height 24px
      line-height 24px

    .shared-tip
      font-weight 900
      margin-left 12px

    .moment-time
      float right
      color #999
      font-size 14px
      line-height 24px

    .message-content
      font-size 14px

  .message-footer
    display flex
    justify-content space-between
    align-items center
    .moment-time
      color #999
      font-size 14px
      line-height 24px
      margin-left 52px

.shared-box
  border 1px solid #e4e7ed
  border-radius 4px
  margin 5px 0

  .privateMessage-titleWithImage
    max-width 350px
</style>
