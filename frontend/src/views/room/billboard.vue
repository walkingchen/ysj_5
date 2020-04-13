<template>
  <div class="moments-layout">
    <title-com title="Public Billboard" class="moments-title" />
    <ul class="moments-ul">
      <li v-if="moment_list.length === 0" class="moments-item">No data.</li>
      <li class="moments-item" v-for="item in moment_list" :key="item.id">
        <div class="moments-item-content">
          <el-avatar :size="50" :src="item.user.avatar ? item.user.avatar : ''" shape="square" class="user-portrait">
            {{ item.user.avatar ? '' : item.user.nickname }}
          </el-avatar>
          <div class="moment-text">
            <div>
              <span class="user-name">{{ item.user.nickname }}</span>
              <span class="moment-time">{{ item.created_at }}</span>
            </div>
            <p>{{ item.content }}</p>
          </div>
        </div>
        <div class="moment-actions">
          <el-popover
            placement="bottom-end"
            width="350"
            trigger="click"
            v-model="comment_visible[item.id]">
            <el-input class="comment_input" type="textarea" :rows="3" placeholder="请输入评论内容" v-model="comment_content" />
            <el-button class="comment_btn" type="primary" size="mini" @click="comment(item.id)">确定</el-button>
            <button slot="reference"><v-icon name="comment-dots" /></button>
          </el-popover>
          <span>{{ item.likeCount }}</span>
          <button @click="like(item)" :class="{ liked: item.liked }"><v-icon :name="item.liked ? 'thumbs-up' : 'regular/thumbs-up'" /></button>
        </div>
        <ul v-if="item.comments.length > 0" class="moment-comments">
          <li class="comment-item" v-for="comment in item.comments" :key="comment.id">
            <div class="comment-item-content">
              <el-avatar :size="35" :src="comment.user.avatar ? comment.user.avatar : ''" shape="square" class="user-portrait">
                {{ comment.user.avatar ? '' : comment.user.nickname }}
              </el-avatar>
              <div class="comment-text">
                <div>
                  <span class="user-name">{{ comment.user.nickname }}</span>
                  <span class="comment-time">{{ comment.created_at }}</span>
                  <button v-if="comment.user_id === userid || item.user_id === userid" class="comment-delete-btn" @click="deleteComment(comment.id)">
                    <i class="el-icon-delete"></i>
                  </button>
                </div>
                <p>{{ comment.comment_content }}</p>
              </div>
            </div>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
import 'vue-awesome/icons/comment-dots'
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
import { getPosts, likePost, unlikePost, commentPost, deleteComment } from '@api/post'
import titleCom from '@components/title'
import { formatDate } from '@assets/utils.js'

export default {
  data() {
    return {
      moments: [],
      comment_content: '',
      comment_visible: {}
    }
  },
  components: {
    titleCom
  },
  computed: {
    moment_list() {
      const members = this.$store.state.room_members
      return this.moments.map(item => {
        const user = members.find(ele => ele.id === item.user_id)
        const _item = {
          id: item.id,
          content: item.post_content,
          liked: item.liked,
          likeCount: item.likes.count,
          created_at: formatDate(item.created_at),
          user: user ? {
            avatar: user.avatar,
            nickname: user.nickname
          } : {
            avatar: null,
            nickname: ''
          },
          comments: item.comments.map(ele => {
            ele.created_at = formatDate(ele.created_at)
            return ele
          })
        }
        return _item
      })
    },
    userid() {
      return this.$store.state.userid
    }
  },
  created() {
    this.getMomentList()
  },
  methods: {
    getMomentList() {
      getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: '0',
        last_update: ''
      }).then(res => {
        this.moments = res.data.data
        res.data.data.forEach(item => {
          this.comment_visible[item.id] = false
        })
      })
    },
    comment(id) {
      commentPost({
        comment_content: this.comment_content,
        post_id: id,
        user_id: this.userid
      }).then(() => {
        this.getMomentList()
        this.comment_visible[id] = false
        this.comment_content = ''
      })
    },
    deleteComment(id) {
      deleteComment(id).then(() => {
        this.getMomentList()
      })
    },
    like(item) {
      if (item.liked) {
        const likes = this.moments.find(ele => ele.id === item.id).likes.details
        const like_id = likes.find(ele => ele.user_id === this.userid).id
        unlikePost(like_id).then(() => {
          this.moments.find(ele => ele.id === item.id).liked = false
        })
      } else {
        likePost({
          post_id: item.id,
          user_id: this.userid
        }).then(() => {
          this.moments.find(ele => ele.id === item.id).liked = true
        })
      }
    }
  }
}
</script>

<style lang="stylus">
.moments-layout
  .moments-title
    background-color #fff

  .moments-ul
    padding 20px 0

  .moments-item
    padding 10px
    background-color #fff
    margin-bottom 20px

    &:last-child
      margin-bottom 0

    .moments-item-content
      display flex

    .user-portrait
      margin-right 12px
      font-size 20px

    .moment-text
      flex 1

      .user-name
        font-size 18px
        line-height 24px

      .moment-time
        float right
        color #666
        font-size 14px
        line-height 24px

      p
        margin-top 8px
        line-height 1.5

    .moment-actions
      height 30px
      display flex
      flex-direction row-reverse

      button
        margin-left 10px
        padding 0 8px
        height 24px
        color #909399

        &:hover
          color #409eff

        &.liked
          color #409eff

    .moment-comments
      border-top 1px solid #e4e7ed

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

.comment_input
  margin-bottom 8px

.comment_btn
  float right
</style>
