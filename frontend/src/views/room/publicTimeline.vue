<template>
  <div class="publicTlimeline-layout">
    <el-card class="post-create-layout">
      <input type="text" class="post-create-title" placeholder="Title" v-model="postTitle" />
      <textarea rows="3" class="post-create-content" placeholder="Content" v-model="postContent" />
      <textarea rows="2" class="post-create-content" placeholder="Keywords" v-model="postKeywords" />
      <el-button class="post-create-btn" type="primary" size="mini" :loading="submitPostLoading" @click="submitPost">Post</el-button>
    </el-card>

    <el-card class="topic-layout">
      <title-com title="Topic of The Day" />
      <public-post-item v-if="showTopic" :item="_topicData" :is-topic="true" @action-success="updatePost" />
    </el-card>

    <div @click="showMoments = !showMoments">
      <el-card class="toggle">
        <v-icon name="angle-right" :style="{transform: `rotate(${showMoments ? 90 : 0}deg)`}" />
      </el-card>
    </div>

    <div class="moments-layout" :style="{ height: showMoments ? momentsLayoutHeight + 'px' : 0 }">
      <div ref="momentsLayout">
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
    </div>

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
const elementResizeDetectorMaker = require('element-resize-detector')

export default {
  props: ['sid'],
  data() {
    return {
      showTopic: false,
      topicData: {},
      getPostLoading: true,
      showMoments: true,
      momentsLayoutHeight: 0,
      moments: [],
      noMoreData: false,
      postTitle: '',
      postContent: '',
      postKeywords: '',
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
  mounted() {
    elementResizeDetectorMaker().listenTo(this.$refs.momentsLayout, element => {
      this.momentsLayoutHeight = element.offsetHeight + 20
    })
  },
  methods: {
    formatPostData (item, showShared = true) {
      const user = this.members.find(ele => ele.id === item.user_id)
      const _item = {
        id: item.id,
        isShared: showShared && item.timeline_type === 2,
        title: item.post_title,
        content: item.post_content,
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
        const postUser = this.members.find(ele => ele.id === item.post_shared.user_id)
        _item.time = formatDate(item.updated_at)
        _item.postSource = {
          user: postUser ? {
            avatar: postUser.avatar,
            nickname: postUser.nickname
          } : {
            avatar: null,
            nickname: ''
          },
          time: formatDate(item.post_shared.created_at),
          title: item.post_shared.post_title,
          content: item.post_shared.post_content
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
      border-top 1px solid #e4e7ed
      padding 10px
      resize none
      outline none

    .post-create-btn
      float right

  .toggle
    margin-top 20px
    text-align center
    border 0
    padding 5px 0
    cursor pointer

    .fa-icon
      transition transform .5s

  .topic-layout
    border 0
    margin-top 20px

  .moments-layout
    overflow hidden
    transition height .5s

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
