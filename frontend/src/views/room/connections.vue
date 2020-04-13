<template>
  <el-card shadow="hover" class="members-content">
    <title-com title="Connections" />
    <ul>
      <li v-for="(item, index) in members" :key="item.id" class="members-item">
        <el-avatar :size="81" :src="item.avatar ? item.avatar : ''" shape="square" class="user-portrait">
          {{ item.avatar ? '' : item.nickname }}
        </el-avatar>
        <button v-if="index > 0"><v-icon name="comments" /></button>
        <div class="user-name">{{ item.nickname }}</div>
      </li>
    </ul>
  </el-card>
</template>

<script>
import 'vue-awesome/icons/comments'
import titleCom from '@components/title'

export default {
  components: {
    titleCom
  },
  computed: {
    members() {
      return this.$store.state.room_members
    }
  }
}
</script>

<style lang="stylus" scoped>
.members-content
  border 0
  margin-bottom 20px

  ul
    padding 5px 10px

  .members-item
    display inline-block
    padding 10px 5px
    position relative
    cursor default

    .user-portrait
      margin-bottom 5px
      font-size 20px

    .user-name
      max-width 81px
      text-align center
      overflow hidden
      text-overflow ellipsis
      white-space nowrap

    button
      position absolute
      top 70px
      right 5px
      padding 0 8px
      height 20px
      color #409eff
      display none

    &:hover
      button
        display block
</style>
