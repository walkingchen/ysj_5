<template>
  <div class="pub-content">
    <el-scrollbar style="height: 100%">
      <div class="pub-content-item" v-for="(i, key) in 14" :key="key">
        <div class="item-user"></div>
        <div class="item-text">
          <div class="item-name">sdv</div>
          <div>技术部是长江索道VB讲哈上将并不具备上档次 艾斯比从v和当贝市场</div>
        </div>
        <div class="item-comment">
          <div style="display: inline-block; float:right">
            <i class="el-icon-edit"></i>
            <span style="font-size: 12px">点赞</span>
            <i class="el-icon-edit"></i>
            <span style="font-size: 12px">评论</span>
          </div>
        </div>
        <div style="width: 100%; height: 1px; background-color: rgba(0,0,0,.08)"></div>
      </div>
    </el-scrollbar>
  </div>
</template>

<script>
import { getPubTimeLine } from '@api/chatroom'
export default {
  props: {
    id: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {}
  },
  watch: {
    id: function(val) {
      this.$nextTick(() => {
        this.init()
      })
    }
  },
  created() {
  },
  methods: {
    init() {
      const params = { room_id: String(this.id), timeline_type: '1' }
      getPubTimeLine(params).then(res => {
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.pub-content{
  width: 100%;
  height: 92vh;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, .05);
  .pub-content-item{
    border-radius: 6px;
    position: relative;
    padding: 10px;
    width: 100%;
    min-height: 50px;
    background-color: #fff;
    .item-user{
      display: inline-block;
      margin: 10px;
      width: 50px;
      height: 50px;
      background-color: pink;
      vertical-align: top;
    }
    .item-text{
      display: inline-block;
      width: 80%;
      height: 100%;
      margin: 10px;
      min-height: 40px;
      background-color: #fff;
      font-size: 15px;
      .item-name{
        font-size: 16px;
        margin: 5px 0;
      }
    }
    .item-comment{
      width: 100%;
      height: 30px;
      background-color: #fff;
      border-radius: 6px;
    }
  }
}
.pub-content >>> .el-scrollbar__bar{
  z-index: -2;
}
</style>
