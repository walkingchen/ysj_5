<template>
  <el-card shadow="hover" class="dailyDigest-layout">
    <title-com title="Daily poll results" />
    <div class="img-box">
      <img src="@assets/test1.png" />
    </div>
  </el-card>
</template>

<script>
import titleCom from '@components/title'

export default {
  components: {
    titleCom
  }
}
</script>

<style lang="stylus" scoped>
.dailyDigest-layout
  border 0
  margin-bottom 20px

  .img-box
    padding 10px

  img
    max-width 100%
    max-height 100%
</style>
