<template>
  <div>
    <el-card shadow="hover" class="myself-box">
      <el-avatar
        :size="80"
        :src="user.avatar ? user.avatar : ''"
        :icon="user.avatar ? '' : 'el-icon-user-solid'" />
      <p>{{ user.nickname }}</p>
    </el-card>

    <el-card shadow="hover" class="members-content">
      <title-com title="Friends" />
      <ul>
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
    </el-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import 'vue-awesome/icons/comments'
import titleCom from '@components/title'

export default {
  components: {
    titleCom
  },
  computed: mapState([
    'user',
    'friends'
  ])
}
</script>

<style lang="stylus" scoped>
.myself-box
  border 0
  padding 20px

  & >>> .el-card__body
    display flex
    flex-direction column
    align-items center

  p
    margin-top 15px

.members-content
  border 0
  margin-top 20px

  .members-item
    padding 10px
    position relative
    cursor default
    display flex
    align-items center

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
</style>
