<template>
  <el-card id="publicTimeline">
    <h2
      class="module-title public-title"
      :class="{ fixed: titleFixed }"
      :style="{ width: titleWidth }"
      @click="handleSkip"
    >Public Post</h2>

    <el-alert v-show="newCount > 0" type="info" center :closable="false" class="new-tip">
      <span slot="title">{{ newCount }} new messages, click <a href="javascript:;" @click="getNews">here</a> to update.</span>
    </el-alert>

    <div class="loading-layout" v-show="getNewPostLoading"><i class="el-icon-loading"></i></div>

    <ul id="moments-ul">
      <li v-for="item in moment_list" :key="item.id">
        <public-post-item :item="item" @action-success="updatePost" />
      </li>
    </ul>

    <div v-if="getPostLoading" class="loading-layout"><i class="el-icon-loading"></i></div>
    <div v-else class="nomore-layout">no more</div>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'
import elementResizeDetectorMaker from 'element-resize-detector'
import { getPosts, getPost } from '@api/post'
import publicPostItem from '@components/publicPostItem'

export default {
  data() {
    return {
      titleFixed: false,
      titleWidth: '100%',
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
    handleSkip () {
      document.getElementsByClassName('room-content')[0].scrollTop = document.getElementById('topicOfDay').offsetHeight + 130
    },
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
        this.newCount += data.posts_number
      }
    })
    this.$bus.$on('new_comment', data => {
      if (data.topic === this.currentTopic) {
        this.updatePost(data.post_id)
      }
    })

    // 处理标题栏宽度
    const erd = elementResizeDetectorMaker()
    erd.listenTo(document.getElementById('publicTimeline'), element => {
      this.titleWidth = element.offsetWidth + 'px'
    })

    this.$bus.$on('room-content-scroll', top => {
      console.log(top)
      // 滚动到标题位置时，将标题定位
      if (top >= (document.getElementById('topicOfDay').offsetHeight + 131)) {
        this.titleFixed = true
      } else {
        this.titleFixed = false
      }
    })
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.me_post_moments = []
        this.moments = []
        this.newCount = 0
        this.getMomentList()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
#publicTimeline
  margin-top 20px

  >>> .el-card__body
    padding-top 59px
    min-height 15px
    position relative

  .public-title
    position absolute
    top 0
    box-sizing border-box
    padding-bottom 15px

    &.fixed
      background-color #fff
      cursor pointer
      border-bottom 1px solid #ddd
      position fixed
      top 145px
      z-index 10

      &:hover
        box-shadow rgb(192, 192, 192, 0.1) 0px 0px 10px

  .new-tip
    margin-top 10px

    a
      color #409eff
      text-decoration none

      &:hover
        text-decoration underline

  .loading-layout
    text-align center
    padding 20px 0 10px
    font-size 20px
    color #409eff

  .nomore-layout
    text-align center
    padding 20px 0 10px
    color #999

#moments-ul > li
  margin-top 20px
  border-bottom 1px dashed #cdd0d6

  &:last-child
    border-bottom 0
</style>
