<template>
  <div class="side-menu" :style="{ width: isCollapse ? '60px' : '210px' }">
    <el-menu
      :default-active="$route.path"
      router
      :collapse="isCollapse"
      background-color="#304156"
      text-color="#bfcbd9">
      <el-menu-item index="/admin/assign">
        <v-icon name="bezier-curve" />
        <span slot="title">Assign Message</span>
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
      <el-menu-item index="/admin/mails">
        <v-icon name="envelope" />
        <span slot="title">Mail</span>
      </el-menu-item>
      <el-menu-item @click="toDataManage">
        <v-icon name="table" />
        <span slot="title">Data</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import 'vue-awesome/icons/bezier-curve'
import 'vue-awesome/icons/comments'
import 'vue-awesome/icons/tags'
import 'vue-awesome/icons/list'
import 'vue-awesome/icons/envelope'
import 'vue-awesome/icons/table'

export default {
  props: ['isCollapse'],
  methods: {
    toDataManage () {
      window.open('http://ysj_5.soulfar.com/admin')
    }
  }
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
  fill rgb(191, 203, 217)

.el-menu-item.is-active .fa-icon
  fill #409eff

.el-menu-item-group__title
  padding 0 !important
</style>
