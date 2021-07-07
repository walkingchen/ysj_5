<template>
  <div class="publicTlimeline-layout">
    <el-card class="post-create-layout">
      <textarea rows="3" class="post-create-content" placeholder="What's on your mind?" v-model="postContent" />
      <el-button class="post-create-btn" type="primary" size="mini" :loading="submitPostLoading" @click="submitPost">Post</el-button>
    </el-card>

    <el-card class="topic-layout">
      <title-com title="Topic of The Day" />
      <public-post-item v-if="showTopic" :item="_topicData" :is-topic="true" @action-success="updatePost" />
    </el-card>

    <div class="new-tip" v-show="newCount > 0">
      {{ newCount }} new messages, click <a href="javascript:;" @click="getNews">here</a> to update.
    </div>

    <div class="loading-layout" v-show="getNewPostLoading"><i class="el-icon-loading"></i></div>

    <ul id="moments-ul">
      <li v-for="item in moment_list" :key="item.id">
        <el-card>
          <public-post-item :item="item" @action-success="updatePost" />
        </el-card>
      </li>
      <div class="loading-layout" v-show="getPostLoading"><i class="el-icon-loading"></i></div>
      <div class="nomore-layout" v-show="noMoreData">No more~</div>
    </ul>

  </div>
</template>

<script>
import 'vue-awesome/icons/angle-right'
import {
  getTopic,
  getPosts,
  getPost,
  createPost
} from '@api/post'
import titleCom from '@components/title'
import publicPostItem from '@components/publicPostItem'
import { formatDate } from '@assets/utils.js'

export default {
  props: ['sid'],
  data() {
    return {
      showTopic: false,
      topicData: {},
      getPostLoading: true,
      moments: [],
      noMoreData: false,
      postContent: '',
      submitPostLoading: false,
      me_post_moments: [],
      newCount: 0,
      getNewPostLoading: false
    }
  },
  components: {
    titleCom,
    publicPostItem
  },
  computed: {
    stopLoadMoments() {
      return this.getPostLoading || this.noMoreData
    },
    members () {
      return [this.$store.state.user, ...this.$store.state.friends]
    },
    moment_list() {
      const moments = [...this.me_post_moments, ...this.moments]
      return moments.map(item => this.formatPostData(item))
    },
    _topicData () {
      return this.formatPostData(this.topicData, false)
    }
  },
  created() {
    this.updateTopic()
    this.getMomentList()

    this.$bus.$on('share-success', id => {
      this.updatePost({
        id,
        type: 0
      })
    })
  },
  methods: {
    formatPostData (item, showShared = true) {
      const user = this.members.find(ele => ele.id === item.user_id)
      const _item = {
        id: item.id,
        isShared: showShared && item.post_shared_id,
        title: item.post_title,
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
        comments: item.comments.map(ele => {
          ele.created_at = formatDate(ele.created_at)
          return ele
        })
      }

      if (_item.isShared) {
        _item.postSource = {
          id: item.post_shared_id,
          time: formatDate(item.post_shared.created_at),
          title: item.post_shared.post_title,
          content: item.post_shared.post_content,
          photo_uri: item.post_shared.photo_uri
        }
      }
      return _item
    },
    updateTopic () {
      getTopic(localStorage.getItem('roomid')).then(({ data }) => {
        this.showTopic = true
        this.topicData = data.data
      })
    },
    async getMomentList() {
      this.getPostLoading = true
      await getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 0,
        pull_new: 0,
        topic: 1,
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
        topic: 1,
        last_update: this.moments.length === 0 ? null : this.moments[0].created_at
      }).then(res => {
        this.me_post_moments = []
        this.moments.unshift(...res.data.data)
      })
      this.getNewPostLoading = false
    },
    updatePost ({ id, type = 1, isTopic = false }) {
      /*
      * type = 1 更新已经获取过的timeline，用来进行了like/dislike/comment/fackcheck操作后对当前单条timeline进行刷新
      * type = 0 用来分享了private timeline或新增了一条timeline后将这条timeline直接显示在最上方而不用获取所有新的post
      */
      if (type && isTopic) {
        this.updateTopic()
      } else {
        getPost(id).then(res => {
          if (type) {
            const momentIndex = this.moments.findIndex(ele => ele.id === id)
            this.moments.splice(momentIndex, 1, res.data.data)
          } else {
            this.$bus.$emit('share-success-refresh', id)
            setTimeout(() => {
              this.me_post_moments.unshift(res.data.data)
            }, 1000)
          }
        })
      }
    },
    async submitPost() {
      if (this.postContent) {
        this.submitPostLoading = true
        await createPost({
          post_content: this.postContent,
          timeline_type: 0,
          post_type: 1,
          topic: 1,
          sid: this.sid,
          room_id: Number(localStorage.getItem('roomid'))
        }).then(res => {
          this.postContent = ''

          this.updatePost({
            id: res.data.data.id,
            type: 0
          })
        })
        this.submitPostLoading = false
      } else {
        this.$message({
          message: 'Please enter the content.',
          type: 'warning'
        })
      }
    }
  }
}
</script>

<style lang="stylus">
.publicTlimeline-layout
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
      padding 10px
      resize none
      outline none

    .post-create-btn
      float right

  .topic-layout
    border 0
    margin-top 20px

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

  #moments-ul > li
    margin-top 20px

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
