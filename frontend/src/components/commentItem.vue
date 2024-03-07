<template>
  <li class="comment-item" :class="{unread: !comment.read_status}">
    <div class="comment-item-content">
      <el-avatar
        :size="32"
        :src="comment.user.avatar ? comment.user.avatar : ''"
        :icon="comment.user.avatar ? '' : 'el-icon-user-solid'"
        class="user-portrait" />
      <div class="comment-text">
        <div class="user-name">{{ comment.user.nickname }}</div>
        <p>
          <highlight :content="comment.comment_content" />
        </p>

        <div class="comment-timeAndActions">
          <span class="comment-time">{{ comment.created_at }}</span>
          <div class="moment-actions comment-actions">
            <!-- <span class="count">{{ comment.flags.count }}</span> -->
            <button @click="flag" :class="{ done: comment.flagged }">
              <v-icon :name="comment.flagged ? 'flag' : 'regular/flag'" />
            </button>
            <button @click="like" :class="{ done: comment.liked }">
              <v-icon :name="comment.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
            </button>
            <span class="count">{{ comment.likes.count }}</span>
          </div>
        </div>
      </div>
    </div>
    <flag-dialog ref="flagDialog" @handleSubmit="handleSubmit" :selectItem="selectItem"/>
  </li>
</template>

<script>
import 'vue-awesome/icons/flag'
import 'vue-awesome/icons/regular/flag'
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
import highlight from './highlight'
import flagDialog from './flagDialog.vue'
import {
  likeComment,
  deleteLike,
  flagComment,
  deleteFlag
} from '@api/comment'

export default {
  props: ['comment'],
  components: {
    highlight,
    flagDialog
  },
  data () { 
    return {
      selectItem: {}
    }
  },
  methods: {
    flag () {
      const item = this.comment
      if (!item.flagged) {
        this.$refs.flagDialog.dialogVisible = true
        this.selectItem = item
      }
      // if (item.flagged) {
      //   this.$confirm(`Are you sure to ${item.flagged ? 'unflag ' : 'flag'} this comment?`, '', {
      //     confirmButtonText: 'OK',
      //     cancelButtonText: 'Cancel',
      //     type: 'warning'
      //   }).then(() => {
      //     if (item.flagged) {
      //       deleteFlag(item.flagged.id).then(res => {
      //         if (res.data.result_code === 2000) {
      //           this.comment.flagged = null
      //           this.comment.flags.count -= 1
      //         }
      //       })
      //     }
      //   }).catch(_ => {})
      // } else {
      //   this.$refs.flagDialog.dialogVisible = true
      //   this.selectItem = item
      // }
      // this.$confirm(`Are you sure to ${item.flagged ? 'unflag ' : 'flag'} this comment?`, '', {
      //   confirmButtonText: 'OK',
      //   cancelButtonText: 'Cancel',
      //   type: 'warning'
      // }).then(() => {
      //   if (item.flagged) {
      //     deleteFlag(item.flagged.id).then(res => {
      //       if (res.data.result_code === 2000) {
      //         this.comment.flagged = null
      //         this.comment.flags.count -= 1
      //       }
      //     })
      //   } else {
      //     flagComment(item.id).then(res => {
      //       if (res.data.result_code === 2000) {
      //         this.$message.success('You\'ve flagged the comment, you can cancel it by reclicking the flag button.')
      //         this.comment.flagged = res.data.data
      //         this.comment.flags.count += 1
      //       }
      //     })
      //   }
      // }).catch(_ => {})
    },
    handleSubmit (data) {
      let params = {
        comment_id: data.item.id,
        flag_content: data.selectTag
      }
      flagComment(params).then(res => {
        if (res.data.result_code === 2000) {
          // this.$message.success('You\'ve flagged the comment, you can cancel it by reclicking the flag button.')
          this.$message.success('You\'ve reported the comment.')
          this.comment.flagged = res.data.data
          this.comment.flags.count += 1
        }
      })
    },
    like () {
      const item = this.comment
      if (item.liked) {
        deleteLike(item.liked.id).then(res => {
          if (res.data.result_code === 2000) {
            this.comment.liked = null
            this.comment.likes.count -= 1
          }
        })
      } else {
        likeComment({
          like_or_not: 1,
          comment_id: item.id
        }).then(res => {
          if (res.data.result_code === 2000) {
            this.comment.liked = res.data.data
            this.comment.likes.count += 1
          }
        })
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.comment-item
  padding 8px 0

  .user-portrait
    margin-right 12px

  .comment-item-content
    display flex

  .comment-text
    flex 1
    border-bottom 1px solid #dcdfe6

    .user-name
      font-size 12px
      line-height 22px

    .comment-time
      color #666
      font-size 12px
      line-height 22px

    p
      line-height 1.5
      font-size 13px

.comment-timeAndActions {
  display flex
  align-items center
  justify-content space-between
}

.comment-actions
  display flex
  font-size 14px

  button
    height 20px

  .fa-icon
    height 14px
</style>
