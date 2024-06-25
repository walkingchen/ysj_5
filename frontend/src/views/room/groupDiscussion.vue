<template>
  <el-card id="groupDiscussion">
    <h2
      class="module-title public-title"
      :class="{ fixed: titleFixed }"
      :style="{ width: titleWidth, top: fixedTitleTop + 'px' }"
      @click="handleSkip"
    >Group Discussion</h2>

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
      fixedTitleTop: 0,
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
      document.getElementsByClassName('room-content')[0].scrollTop = document.getElementById('topShares').offsetHeight + 110
    },
    async getMomentList() {
      this.getPostLoading = true
      await getPosts({
        room_id: localStorage.getItem('roomid'),
        timeline_type: 0,
        topic: this.currentTopic
      }).then(res => {
        this.moments.push(...res.data.data.filter(item => item.topic === this.currentTopic))
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
    elementResizeDetectorMaker().listenTo(document.getElementById('groupDiscussion'), element => {
      this.titleWidth = window.getComputedStyle(element).getPropertyValue('width')
    })

    const topSharesDom = document.getElementById('topShares')
    let appHeight = document.getElementById('app').offsetHeight
    let postForumHeight = document.getElementById('addDiscussion').offsetHeight
    let topSharesHeight = topSharesDom.offsetHeight
    this.$bus.$on('room-content-scroll', top => {

      if (top < (20 + postForumHeight + 20 + topSharesHeight + 20 + 62 - (appHeight - 70))) { // 向上滚动到 title 位置时，将 title 固定在底部
        this.titleFixed = true
        this.fixedTitleTop = appHeight - 50
      } else if (top >= (20 + postForumHeight + 20 + topSharesHeight + 20 - (50 + 38))) { // 向下滚动到 title 位置时，将 title 固定在顶部
        this.titleFixed = true
        this.fixedTitleTop = 158 // 70header + 50'COVID Flashbacks: Top Shares' + 38alert
      } else { // title 出现在可视区域内时取消上下固定
        this.titleFixed = false
        this.fixedTitleTop = 0
      }
    })

    // 监听 topShares & add discussion dom 高度变化，判断是否将标题固定在底部
    const title = document.getElementsByClassName('public-title')[0]
    const fixedTitleOnBottom = () => {
      if (title.getBoundingClientRect().top > appHeight - 46) {
        this.titleFixed = true
        this.fixedTitleTop = appHeight - 46
      }
    }

    // 监听 topShares dom 高度变化
    const MutationObserver = window.MutationObserver || window.webkitMutationObserver || window.MozMutationObserver
    const topSharesMutationObserver = new MutationObserver(() => {
      const height = topSharesDom.offsetHeight
      if (height === topSharesHeight) return
      topSharesHeight = height
      fixedTitleOnBottom()
    })
    topSharesMutationObserver.observe(topSharesDom, {
      childList: true, // 子节点的变动（新增、删除或者更改）
      attributes: true, // 属性的变动
      characterData: true, // 节点内容或节点文本的变动
      subtree: true // 是否将观察器应用于该节点的所有后代节点
    })

    // 监听 add discussion dom 高度变化
    elementResizeDetectorMaker().listenTo(document.getElementById('addDiscussion'), el => {
      postForumHeight = el.offsetHeight
      fixedTitleOnBottom()
    })
  },
  watch: {
    currentTopic (topic) {
      if (topic) {
        this.me_post_moments = []
        this.moments = []
        this.newCount = 0
        this.titleFixed = false
        this.fixedTitleTop = 0
        this.getMomentList()
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
#groupDiscussion
  border 0
  margin-top 20px

  .loading-layout
    padding 20px 0 10px

  >>> .el-card__body
    padding-top var(--module-title-height)
    min-height 15px
    position relative

  .public-title
    position absolute
    top 0
    box-sizing border-box
    background-color #429cd9
    color #fff

  .new-tip
    margin-top 10px

    a
      color #409eff
      text-decoration none

      &:hover
        text-decoration underline

#moments-ul > li
  margin-top 20px
  border-bottom 1px dashed #cdd0d6

  &:last-child
    border-bottom 0
</style>
