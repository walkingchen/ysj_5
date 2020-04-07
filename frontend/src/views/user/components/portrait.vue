<template>
  <div class="por-content">
    <div v-for="(i, k) in members" :key="k" class="por-content-item">
      <div class="item-image"></div>
      <div class="item-info">{{ i.nickname }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    members: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {}
  },
  watch: {
    members: function(v, old) {
      this.$nextTick(() => {
        this.init()
      })
    },
    deep: true
  },
  created() {
  },
  mounted() {
  },
  methods: {
    init() {
      console.log(this.members)
      const colors = ['#d2707e', '#659cb8', '#dd8061', '#87c3bd', '#b2acbe', '#ecb97e', '#cbc4b5']
      for (let i = 0; i < this.members.length; i++) {
        const random_color = colors[Math.floor(Math.random() * colors.length)]
        document.getElementsByClassName('por-content-item')[i].style.backgroundColor = random_color
      }
      console.log(Math.floor(Math.random() * colors.length))
    }
  }
}
</script>

<style lang="scss" scoped>
.por-content{
  width: 100%;
  height: 32vh;
  background-color:beige;
  padding: 8px 8px 12px 8px;
  .por-content-item{
    margin: 5px;
    width: calc((100% - 30px) / 3);
    height: calc((100% - 30px) / 3);
    display: inline-block;
    position: relative;
    padding: 5px;
    overflow: hidden;
    .item-image{
      width: 30px;
      height: 30px;
      background-color: white;
      float: left;
    }
    .item-info{
      float: right;
      font-size: 10px;
      text-align: left;
      width: calc(100% - 40px);
    }
  }
}
</style>
