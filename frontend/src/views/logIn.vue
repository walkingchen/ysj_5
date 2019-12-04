<template>
    <div class="login-wrapper">
      <el-form :model="data" :rules="rules" ref="form" label-position="left" label-width="0px" class="login-form-wrapper">
        <h3 class="title">登录</h3>
        <el-form-item prop="username">
          <el-input type="text" v-model="data.username" auto-complete="off" placeholder="用户名" @keyup.enter.native="login"></el-input>
        </el-form-item>
        <el-form-item prop="password" >
          <el-input type="password" v-model="data.password" auto-complete="off" placeholder="登录密码" @keyup.enter.native="login"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click.native.prevent="login" :loading="isLoading" style="color: white">登录</el-button>
        </el-form-item>
      </el-form>
    </div>

</template>

<script>
import { requestLogin } from '@/api/api.js'
  // import {  } from 'vuex'

export default {
  data() {
    return {
      isLoading: false,
      data: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
        ]
      }
    }
  },
  methods: {
    // ...mapMutations({
    //   'SET_USERNAME': 'SET_USERNAME'
    // }),
    login() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.isLoading = true
          requestLogin(this.data).then(res => {
            this.isLoading = false
            let { code, list } = res
            if (code !== 0) {
              this.$notify.error({
                title: '错误',
                message: '用户名或密码错误'
              })
            }else {
              if (list.length > 0) {
                this.SET_USERNAME(list[0].name)
                window.localStorage.setItem('username', list[0].name)
                window.localStorage.setItem('token', list[0].token)
              }
              // this.$router.replace({ path: '/home' })
            }
          })
        }
      })
    }
  }
}

</script>

<style scoped lang="stylus">
  .login-wrapper
    height 730px
    background-image: url(../assets/img/bg.jpg)
    background-repeat:no-repeat;
    background-size:100% 100%;
  .login-form-wrapper
    position absolute
    top 50%
    left 50%
    z-index 99
    background-clip padding-box
    width 350px
    padding 45px 73px 26px
    margin-left  0px
    margin-top -180px
    background: rgba(241,215,126,0.8)
    border-radius 5px
    .el-form-item
      width 300px
      margin 0 auto 41px
      &:last-child
        margin-bottom 25px
      >>> &.is-error
        .el-input__inner
          border-bottom 1px solid #f56c6c
      >>> &.is-success
        .el-input__inner
          border-bottom 1px solid #67c23a
      >>> .el-input__inner
        border none
        border-bottom 1px solid #CEE6E9
        border-radius 0
        padding 0 0 0 8px
        background-color transparent
        font-size 12px
        color #afbaba
        width 100%
      >>> .el-form-item__error
        padding-top 8px
        color #ee2f58
      .el-button--primary
        background #364e6f
        border-radius 2px
        font-size 18px
        color rgb(37, 53, 73)
        width 100%
        height 50px
        cursor pointer
        &:visited
        &:active
        &:hover
          background-color #4f6179
    .title
      margin 0px auto 40px auto
      text-align center
      color #364e6f
      font-size 24px
      font-weight 400
      user-select none
    .remember
      margin 0px 0px 35px 0px
</style>
