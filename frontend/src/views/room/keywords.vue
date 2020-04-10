<template>
  <el-card shadow="hover" class="keywords-layout">
    <title-com title="分类" />
    <ul>
      <li v-for="(i, item) in 15" :key="item">keyword{{i}}</li>
    </ul>
  </el-card>
</template>

<script>
import titleCom from '@components/title'

export default {
  data() {
    return {
      keywords: []
    }
  },
  components: {
    titleCom
  }
}
</script>

<style lang="stylus" scoped>
.keywords-layout
  border 0

  ul
    padding 10px 20px

  li
    cursor pointer
    line-height 2
    max-width 100%
    overflow hidden
    text-overflow ellipsis
    white-space nowrap
    color #303133

    &:hover
      color #409eff
</style>
