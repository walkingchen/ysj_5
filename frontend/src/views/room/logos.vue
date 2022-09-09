<template>
  <div class="logos-box">
    <img v-for="item in logos" :key="item" :src="item" class="logo-item" />
  </div>
</template>

<script>
import logo1 from '@assets/logo1.png'
import logo2 from '@assets/logo2.png'
import logo3 from '@assets/logo3.png'
import logo4 from '@assets/logo4.png'
import logo5 from '@assets/logo5.png'
import logo6 from '@assets/logo6.png'
import logo7 from '@assets/logo7.png'

export default {
  data () {
    return {
      logos: [logo1, logo2, logo3, logo4, logo5, logo6, logo7]
    }
  }
}
</script>

<style lang="stylus" scoped>
.logos-box
  display flex
  flex-wrap wrap
  justify-content center
  padding 0 30px 10px

.logo-item
  height 50px
  margin-right 12px
  margin-bottom 12px
</style>
