<template>
  <div class="publicTlimeline-layout">
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
      <div v-if="getPostLoading" class="loading-layout"><i class="el-icon-loading"></i></div>
      <div v-else class="nomore-layout">No more~</div>
    </ul>

  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getPosts, getPost } from '@api/post'
import publicPostItem from '@components/publicPostItem'

export default {
  data() {
    return {
      getPostLoading: true,
      moments: [],
      me_post_moments: [],
      newCount: 0,
      getNewPostLoading: false
    }
  },
  components: {
    publicPostItem
  },
  computed: {
    moment_list() {
      return [...this.me_post_moments, ...this.moments]
    },
    ...mapState(['currentTopic'])
  },
  methods: {
    async getMomentList() {
      this.getPostLoading = true
      await getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 0,
        topic: this.currentTopic
      }).then(res => {
        this.moments.push(...res.data.data)
      })
      this.getPostLoading = false
    },
    async getNews() {
      this.getNewPostLoading = true
      this.newCount = 0

      const params = {
        room_id: localStorage.getItem('roomid'),
        timeline_type: 0,
        topic: this.currentTopic
      }
      if (this.moments.length > 0) {
        params.pull_new = 1
        params.last_update = this.moments[0].created_at
      }
      await getPosts(params).then(res => {
        this.me_post_moments = []
        this.moments.unshift(...res.data.data)
      })
      this.getNewPostLoading = false
    },
    updatePost (id, type = 1) {
      /*
      * type = 1 更新已经获取过的post，用来对某条post进行了操作后刷新该条post
      * type = 0 用来分享了private post或发表了一条post后将这条post直接显示在最上方而不用获取所有新的post
      */
      if (!type || this.moment_list.findIndex(ele => ele.id === id) > -1) {
        getPost(id).then(res => {
          if (type) {
            const momentsIndex = this.moments.findIndex(ele => ele.id === id)
            const mePostsIndex = this.me_post_moments.findIndex(ele => ele.id === id)
            if (momentsIndex > -1) {
              this.moments.splice(momentsIndex, 1, res.data.data)
            } else if (mePostsIndex > -1) {
              this.me_post_moments.splice(mePostsIndex, 1, res.data.data)
            }
          } else {
            this.$bus.$emit('share-success-refresh', id)
            if (this.currentTopic === res.data.data.topic) {
              setTimeout(() => {
                this.me_post_moments.unshift(res.data.data)
              }, 1000)
            }
          }
        })
      }
    }
  },
  mounted () {
    this.$bus.$on('share-success', id => {
      this.updatePost(id, 0)
    })
    this.$bus.$on('new_post', data => {
      if (data.topic === this.currentTopic && data.timeline_type === 0) {
        this.newCount = data.posts_number
      }
    })
    this.$bus.$on('new_comment', data => {
      if (data.topic === this.currentTopic) {
        this.updatePost(data.post_id)
      }
    })
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.me_post_moments = []
        this.moments = []
        this.getMomentList()
      }
    }
  }
}
</script>

<style lang="stylus">
.publicTlimeline-layout
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
