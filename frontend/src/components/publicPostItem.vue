<template>
  <div class="moments-item" :class="{unread: _item.unread}">
    <div class="moments-item-content">
      <el-avatar
        :size="40"
        :src="_item.user.avatar ? _item.user.avatar : ''"
        :icon="_item.user.avatar ? '' : 'el-icon-user-solid'"
        class="user-portrait" />
      <div class="moment-text">
        <div>
          <span class="user-name">{{ _item.user.nickname }}</span>
          <span v-if="_item.isShared" class="shared-tip">shared:</span>
          <span class="moment-time">{{ _item.time }}</span>
        </div>
        <div>
          <p class="content">
            <highlight :content="_item.content" />
          </p>
          <img v-if="_item.photo_uri" :src="_item.photo_uri.small" class="post-photo" />
          <div v-if="_item.isShared" class="shared-box">
            <private-post-item :item="_item.postSource" />
          </div>
        </div>
      </div>
    </div>
    <div class="moment-actions">
      <!-- <button @click="factcheck(_item)" :class="{ done: _item.factcheck }"><v-icon name="exclamation-circle" /></button> -->
      <span class="count" v-if="_item.comments.length > 0">{{ _item.comments.length }}</span>
      <button @click="toggleShowMoreComments"><v-icon name="comment-dots" /></button>
      <!-- <span class="count">{{ _item.dislikeCount }}</span>
      <button @click="like(_item, 0)" :class="{ done: _item.disliked }">
        <v-icon :name="_item.disliked ? 'thumbs-down' : 'regular/thumbs-down'" />
      </button> -->
      <span class="count">{{ _item.flagCount }}</span>
      <button @click="flag(_item)" :class="{ done: _item.flagged }">
        <v-icon :name="_item.flagged ? 'flag' : 'regular/flag'" />
      </button>
      <span class="count">{{ _item.likeCount }}</span>
      <button @click="like(_item)" :class="{ done: _item.liked }">
        <v-icon :name="_item.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
      </button>
    </div>

    <comments
      ref="comments"
      :comments="_item.comments"
      :post-id="_item.id"
      style="margin-top: 10px"
      @action-success="$emit('action-success', _item.id)" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
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

export default {
  props: ['item'],
  components: {
    highlight,
    privatePostItem,
    comments
  },
  data () {
    return {
      comment_content: ''
    }
  },
  computed: {
    members () {
      return [this.user, ...this.friends]
    },
    _item () {
      const item = this.item
      const user = this.members.find(ele => ele.id === item.user_id)
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
        disliked: item.disliked,
        dislikeCount: item.dislikes.count,
        factcheck: item.factcheck,
        time: formatDate(item.created_at),
        user: user ? {
          avatar: user.avatar,
          nickname: user.nickname
        } : {
          avatar: null,
          nickname: ''
        },
        comments: item.comments
      }

      if (_item.isShared) {
        _item.postSource = item.post_shared
      }
      return _item
    },
    ...mapState([
      'user',
      'friends'
    ])
  },
  methods: {
    async flag(item) {
      if (item.flagged) {
        await deleteFlag(item.flagged.id)
      } else {
        await flagPost(item.id).then(res => {
          if (res.data.result_code === 2000) {
            this.$message.success('You\'ve flagged the post, you can cancel it by reclicking the flag button.')
          }
        })
      }
      this.$emit('action-success', item.id)
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

    .content
      font-size 14px
      line-height 1.5
      white-space pre-wrap

.shared-box
  border 1px solid #e4e7ed
  border-radius 4px
  margin 5px 0
</style>
