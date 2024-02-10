<template>
  <div>
    <el-card class="members-content">
      <h2 class="module-title">Friends</h2>

      <div class="friends-content-wrapper">
        <ul class="friends">
          <li v-for="item in friends" :key="item.id" class="members-item">
            <el-avatar
              :src="item.avatar ? item.avatar : ''"
              :icon="item.avatar ? '' : 'el-icon-user-solid'"
              class="user-portrait" />
            <span class="username">{{ item.nickname }}</span>
            <!-- <button class="chat-btn" @click="$emit('start-chat', item)">
              <v-icon name="comments" scale="1.5" />
            </button> -->
          </li>
        </ul>

        <div class="forum-update">
          <h4>Forum Update</h4>
          <h5>New Post</h5>
          <span>{{ statsData.new_post_count }}</span>
          <h5>New Comment</h5>
          <span>{{ statsData.new_comment_count }}</span>
          <h5>New Likes</h5>
          <span>{{ statsData.new_like_count }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import 'vue-awesome/icons/comments'
import { getRoomStats } from '@api/room'

export default {
  data () {
    return {
      statsData: {
        new_comment_count: 0,
        new_flag_count: 0,
        new_like_count: 0,
        new_post_count: 0
      }
    }
  },
  computed: mapState([
    'user',
    'friends'
  ]),
  created () {
    getRoomStats(localStorage.getItem('roomid')).then(({ data }) => {
      if (data.result_code === 2000) {
        this.statsData = data.data
      }
    })
  }
}
</script>

<style lang="stylus" scoped>
.members-content
  border 0

  .module-title
    border-bottom 1px solid #ebeef5

  .members-item
    padding 10px
    position relative
    cursor default
    display flex
    align-items center

    .el-avatar 
      width 20px
      height 20px

    .user-portrait
      margin-right 8px

    .username
      flex 1
      overflow hidden
      text-overflow ellipsis
      white-space nowrap

    // .chat-btn
    //   display none
    //   position absolute
    //   top 0
    //   left 0
    //   width 100%
    //   height 100%
    //   background-color rgba(0, 0, 0, .2)
    //   justify-content center
    //   align-items center
    //   color #409eff

    // &:hover .chat-btn
    //   display flex

.friends-content-wrapper
  display flex
  padding 20px

  .friends
    width 50%
    border-right 1px solid #ebeef5

  .forum-update
    flex 1
    display flex
    flex-direction column
    justify-content center
    align-items center
    padding 25px 0
    font-size 16px

    h5
      margin-top 18px

    span
      color #f56c6c
</style>
