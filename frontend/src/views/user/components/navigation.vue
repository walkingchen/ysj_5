<template>
  <div class="nav-content">
    <div></div>
  </div>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {}
  },
  created() {
  }
}
</script>

<style lang="scss" scoped>
.nav-content{
  width: 100%;
  height: 57vh;
  background-color: floralwhite;
}
</style>
