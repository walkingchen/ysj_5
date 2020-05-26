<template>
  <div class="side-menu" :style="{ width: isCollapse ? '60px' : '210px' }">
    <el-menu
      :default-active="$route.path"
      router
      :collapse="isCollapse"
      background-color="#304156"
      text-color="#bfcbd9">
      <el-menu-item index="/admin/dashboard">
        <v-icon name="tachometer-alt" />
        <span slot="title">Dashboard</span>
      </el-menu-item>
      <el-submenu index="2">
        <template slot="title">
          <v-icon name="comments" />
          <span slot="title">Room</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/admin/roomPrototype">
            <v-icon name="tags" />
            <span slot="title">Prototype</span>
          </el-menu-item>
          <el-menu-item index="/admin/rooms">
            <v-icon name="list" />
            <span slot="title">Rooms</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import 'vue-awesome/icons/tachometer-alt'
import 'vue-awesome/icons/comments'
import 'vue-awesome/icons/tags'
import 'vue-awesome/icons/list'

export default {
  props: ['isCollapse']
}
</script>

<style lang="stylus" scoped>
.admin-layout
  height 100vh

  .side-menu
    background-color #304156
    height 100%
    transition width .28s
    overflow hidden

    .el-menu
      width 100%
      border 0
</style>

<style lang="stylus">
.el-menu .fa-icon
  width 20px
  margin-right 5px

.el-menu-item-group__title
  padding 0 !important
</style>
