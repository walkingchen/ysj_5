<template>
  <div class="admin-layout">
    <side-menu :is-collapse="isCollapse" />
    <div class="main-container">
      <header>
        <button @click="isCollapse = !isCollapse">
          <v-icon :name="isCollapse ? 'indent' : 'outdent'" />
        </button>
        <button class="logout" @click="logout">
          <v-icon name="sign-out-alt" />
        </button>
      </header>
      <section>
        <transition name="fade-transform" mode="out-in">
          <router-view :key="$route.path" />
        </transition>
      </section>
    </div>
  </div>
</template>

<script>
import 'vue-awesome/icons/indent'
import 'vue-awesome/icons/outdent'
import 'vue-awesome/icons/sign-out-alt'
import sideMenu from './sideMenu'
import { logout } from '@api/auth'

export default {
  components: {
    sideMenu
  },
  data() {
    return {
      isCollapse: false
    }
  },
  methods: {
    logout() {
      logout()
      this.$router.push({ name: 'AdminLogin' })
    }
  }
}
</script>

<style lang="stylus" scoped>
.admin-layout
  height 100vh
  display flex
  overflow hidden

  .main-container
    flex 1
    height 100%
    display flex
    flex-direction column
    overflow hidden

    header
      height 50px
      // box-shadow 0 1px 4px rgba(0, 21, 41, .08)

      button
        padding 0 15px
        height 100%

        &:hover
          background-color rgba(0, 0, 0, .025)

        &.logout
          float right

    section
      flex 1
      overflow auto
      padding 20px
</style>
