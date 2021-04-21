<template>
  <div class="moments-layout">
    <el-card shadow="hover" class="post-create-layout">
      <input type="text" class="post-create-title" placeholder="Title" v-model="postTitle" />
      <textarea rows="3" class="post-create-content" placeholder="Content" v-model="postContent" />
      <textarea rows="2" class="post-create-content" placeholder="Keywords" v-model="postKeywords" />
      <el-button class="post-create-btn" type="primary" size="mini" :loading="submitPostLoading" @click="submitPost">Post</el-button>
    </el-card>

    <el-card shadow="hover" class="topic-layout">
      <title-com title="Topic of The Day" />
      <div class="img-box"><img src="@assets/test2.png" /></div>
    </el-card>

    <div class="new-tip" v-show="newCount > 0">
      {{ newCount }} new messages, click <a href="javascript:;" @click="getNews">here</a> to update.
    </div>

    <div class="loading-layout" v-show="getNewPostLoading"><i class="el-icon-loading"></i></div>

    <ul class="moments-ul">
      <li v-for="item in moment_list" :key="item.id">
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
                <span class="moment-time">{{ item.created_at }}</span>
              </div>
              <p>{{ item.title }}</p>
              <p>{{ item.content }}</p>
            </div>
          </div>
          <div class="moment-actions">
            <button @click="factcheck(item)" :class="{ done: item.factcheck }"><v-icon name="exclamation-circle" /></button>
            <el-popover
              placement="bottom-end"
              width="350"
              trigger="click"
              v-model="comment_visible[item.id]">
              <el-input class="comment_input" type="textarea" :rows="3" placeholder="Comment Content" v-model="comment_content" />
              <el-button class="comment_btn" type="primary" size="mini" @click="comment(item.id)">Submit</el-button>
              <button slot="reference"><v-icon name="comment-dots" /></button>
            </el-popover>
            <span class="count">{{ item.dislikeCount }}</span>
            <button @click="like(item, 0)" :class="{ done: item.disliked }">
              <v-icon :name="item.disliked ? 'thumbs-down' : 'regular/thumbs-down'" />
            </button>
            <span class="count">{{ item.likeCount }}</span>
            <button @click="like(item, 1)" :class="{ done: item.liked }">
              <v-icon :name="item.liked ? 'thumbs-up' : 'regular/thumbs-up'" />
            </button>
          </div>
          <ul v-if="item.comments.length > 0" class="moment-comments">
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
                    <span class="comment-time">{{ comment.created_at }}</span>
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
        </el-card>
      </li>
      <div class="loading-layout" v-show="getPostLoading"><i class="el-icon-loading"></i></div>
      <div class="nomore-layout" v-show="noMoreData">No more~</div>
    </ul>

  </div>
</template>

<script>
import 'vue-awesome/icons/thumbs-up'
import 'vue-awesome/icons/regular/thumbs-up'
import 'vue-awesome/icons/thumbs-down'
import 'vue-awesome/icons/regular/thumbs-down'
import 'vue-awesome/icons/comment-dots'
import 'vue-awesome/icons/exclamation-circle'
import {
  getPosts,
  getPost,
  likePost,
  deleteLike,
  changeLike,
  commentPost,
  deleteComment,
  checkPost,
  deleteCheck,
  createPost
} from '@api/post'
import titleCom from '@components/title'
import { formatDate } from '@assets/utils.js'

export default {
  props: ['sid'],
  data() {
    return {
      getPostLoading: true,
      moments: [],
      noMoreData: false,
      postTitle: '',
      postContent: '',
      postKeywords: '',
      submitPostLoading: false,
      comment_content: '',
      comment_visible: {},
      me_post_moments: [],
      newCount: 0,
      getNewPostLoading: false
    }
  },
  components: {
    titleCom
  },
  computed: {
    stopLoadMoments() {
      return this.getPostLoading || this.noMoreData
    },
    moment_list() {
      const members = [this.$store.state.user, ...[this.$store.state.friends]]
      const moments = [...this.me_post_moments, ...this.moments]
      return moments.map(item => {
        const user = members.find(ele => ele.id === item.user_id)
        const _item = {
          id: item.id,
          title: item.post_title,
          content: item.post_content,
          liked: item.liked,
          disliked: item.disliked,
          likeCount: item.likes.count,
          dislikeCount: item.dislikes.count,
          factcheck: item.factcheck,
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
      return this.$store.state.user.id
    }
  },
  created() {
    this.getMomentList()
  },
  methods: {
    async getMomentList() {
      this.getPostLoading = true
      await getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 0,
        pull_new: 0,
        last_update: this.moments.length === 0 ? null : this.moments[this.moments.length - 1].created_at
      }).then(res => {
        if (res.data.data.length === 0) {
          this.noMoreData = true
        }

        this.moments.push(...res.data.data)
      })
      this.getPostLoading = false
    },
    async getNews() {
      this.getNewPostLoading = true
      this.newCount = 0
      await getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 0,
        pull_new: 1,
        last_update: this.moments.length === 0 ? null : this.moments[0].created_at
      }).then(res => {
        this.me_post_moments = []
        this.moments.unshift(...res.data.data)
      })
      this.getNewPostLoading = false
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
      this.updateMoment(item.id)
    },
    comment(id) {
      commentPost({
        comment_content: this.comment_content,
        post_id: id
      }).then(() => {
        this.updateMoment(id)
        this.comment_visible[id] = false
        this.comment_content = ''
      })
    },
    deleteComment(momentid, commentid) {
      deleteComment(commentid).then(() => {
        this.updateMoment(momentid)
      })
    },
    async factcheck(item) {
      if (item.factcheck) {
        await deleteCheck(item.factcheck.id)
      } else {
        await checkPost({ post_id: item.id })
      }
      this.updateMoment(item.id)
    },
    updateMoment(id, type = 1) {
      /*
      * type = 1 更新已经获取过的timeline，用来进行了like/dislike/comment/fackcheck操作后对当前单条timeline进行刷新
      * type = 0 用来分享了private timeline或新增了一条timeline后将这条timeline直接显示在最上方而不用获取所有新的post
      */
      getPost(id).then(res => {
        if (type) {
          const momentIndex = this.moments.findIndex(ele => ele.id === id)
          this.moments.splice(momentIndex, 1, res.data.data)
        } else {
          this.me_post_moments.unshift(res.data.data)
        }
      })
    },
    async submitPost() {
      if (this.postTitle && this.postContent) {
        this.submitPostLoading = true
        await createPost({
          post_content: this.postContent,
          post_title: this.postTitle,
          keywords: this.postKeywords,
          timeline_type: 0,
          post_type: 1,
          sid: this.sid,
          room_id: Number(localStorage.getItem('roomid'))
        }).then(res => {
          this.postTitle = ''
          this.postContent = ''
          this.postKeywords = ''

          this.updateMoment(res.data.data.id, 0)
        })
        this.submitPostLoading = false
      } else {
        this.$message({
          message: 'Please enter the title and content.',
          type: 'warning'
        })
      }
    }
  },
  watch: {
    moment_list(val) {
      val.forEach(item => {
        this.comment_visible[item.id] = false
      })
    }
  }
}
</script>

<style lang="stylus">
.moments-layout
  .post-create-layout
    border 0
    padding 10px

    .post-create-title
      width calc(100% - 20px)
      border 0
      height 30px
      padding 0 10px
      outline none

    .post-create-content
      width calc(100% - 20px)
      border 0
      border-top 1px solid #e4e7ed
      padding 10px
      resize none
      outline none

    .post-create-btn
      float right

  .topic-layout
    border 0
    margin-top 20px

    .img-box
      padding 10px

    img
      max-width 100%
      max-height 100%

  .new-tip
    background-color #fff
    margin-top 20px
    text-align center
    padding 10px 0

    a
      color #409eff
      text-decoration none

      &:hover
        text-decoration underline

  .moments-ul > li
    margin-top 20px

  .moments-item
    padding 10px
    border 0

    .moments-item-content
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

  .loading-layout
    text-align center
    padding-top 20px
    font-size 20px
    color #409eff

  .nomore-layout
    text-align center
    padding-top 20px
    color #999
</style>
