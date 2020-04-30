<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" label-position="left">

      <h3 class="title">Login</h3>

      <el-form-item prop="username">
        <span class="svg-container">
          <v-icon name="envelope" />
        </span>
        <el-input
          v-model="loginForm.username"
          placeholder="E-mail"
          type="text"
          @keyup.enter.native="handleLogin"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <v-icon name="lock" />
        </span>
        <el-input
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <v-icon :name="passwordType === 'password' ? 'eye' : 'eye-slash'" />
        </span>
      </el-form-item>

      <el-button :loading="loading" type="primary" class="login-btn" @click.native.prevent="handleLogin">Login</el-button>

      <el-alert v-show="error_show" title="Login failed, please try again." type="error" show-icon :closable="false" />

    </el-form>
  </div>
</template>

<script>
import 'vue-awesome/icons/envelope'
import 'vue-awesome/icons/lock'
import 'vue-awesome/icons/eye'
import 'vue-awesome/icons/eye-slash'
import { login } from '@api/auth'

export default {
  props: ['toRouter'],
  data() {
    return {
      loginForm: {
        username: 'user14',
        password: '123456'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', message: 'Please enter the username.' }],
        password: [{ required: true, trigger: 'blur', message: 'Please enter the password.' }]
      },
      loading: false,
      passwordType: 'password',
      error_show: false
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = 'text'
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.error_show = false
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          login(this.loginForm).then(res => {
            if (res.data.result_code === 2000) {
              localStorage.setItem('roomid', res.data.data.id)
              this.$router.push(this.toRouter)
            } else {
              this.loading = false
              this.error_show = true
            }
          }).catch(() => {
            this.loading = false
            this.error_show = true
          })
        }
      })
    }
  }
}
</script>

<style lang="stylus">
/* 修复input 背景不协调 和光标变色 */
$bg = #283443
$light_gray = #fff
$cursor =  #fff

@supports (-webkit-mask: none) and (not (cater-color: $cursor))
  .login-container .el-input input
    color: $cursor

/* reset element-ui css */
.login-container
  .el-input
    display inline-block
    height 47px
    width 85%

    input
      background transparent
      border 0px
      -webkit-appearance none
      border-radius 0px
      padding 12px 5px 12px 15px
      color $light_gray
      height 47px
      caret-color $cursor

      &:-webkit-autofill
        box-shadow 0 0 0px 1000px $bg inset !important
        -webkit-text-fill-color $cursor !important

  .el-form-item
    border 1px solid rgba(255, 255, 255, 0.1)
    background rgba(0, 0, 0, 0.1)
    border-radius 5px
    color #454545
</style>

<style lang="stylus" scoped>
$bg = #2d3a4b
$dark_gray = #889aa4
$light_gray = #eee

.login-container
  height 100vh
  background-color $bg
  overflow hidden
  display flex
  justify-content center
  align-items center

  .login-form
    width 520px
    max-width 100%
    height 316px

  .title
    text-align center
    color $light_gray
    margin-bottom 40px
    font-weight bold

  .svg-container
    padding 6px 5px 6px 15px
    color $dark_gray
    vertical-align middle
    width 30px
    display inline-block

  .show-pwd
    position absolute
    right 10px
    top 7px
    font-size 16px
    color $dark_gray
    cursor pointer
    user-select none

  .login-btn
    width 100%
    margin-bottom 22px
</style>
