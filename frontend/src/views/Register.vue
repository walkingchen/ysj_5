<template>
  <div class="register-container">
    <el-form ref="register" :model="registerForm" :rules="rules" class="register-form" label-position="left">

      <h3 class="title">Register</h3>

      <el-form-item prop="email">
        <span class="svg-container">
          <v-icon name="envelope" />
        </span>
        <el-input
          v-model="registerForm.email"
          placeholder="E-mail"
          type="text"
          @keyup.enter.native="submit"
        />
      </el-form-item>

      <el-form-item class="avatar-form-item">
        <span class="svg-container">
          <v-icon name="user-ninja" />
        </span>
        <ul>
          <li
            v-for="(item, index) in avatars"
            :key="index"
            :class="{ actived: avatarIndex === index }"
            @click="avatarIndex = index"
          >
            <img :src="item" />
          </li>
        </ul>
      </el-form-item>

      <el-form-item prop="nickname">
        <span class="svg-container">
          <v-icon name="user" />
        </span>
        <el-input
          v-model="registerForm.nickname"
          placeholder="Name"
          type="text"
          @keyup.enter.native="submit"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <v-icon name="lock" />
        </span>
        <el-input
          ref="password"
          v-model="registerForm.password"
          :type="passwordType"
          placeholder="Password"
          @keyup.enter.native="submit"
        />
        <span class="show-pwd" @click="showPwd">
          <v-icon :name="passwordType === 'password' ? 'eye' : 'eye-slash'" />
        </span>
      </el-form-item>

      <el-form-item prop="checkPassword">
        <span class="svg-container">
          <v-icon name="check-square" />
        </span>
        <el-input
          ref="checkPassword"
          v-model="registerForm.checkPassword"
          :type="checkPasswordType"
          placeholder="Check Password"
          @keyup.enter.native="submit"
        />
        <span class="show-pwd" @click="showCheckPwd">
          <v-icon :name="checkPasswordType === 'password' ? 'eye' : 'eye-slash'" />
        </span>
      </el-form-item>

      <el-button :loading="loading" type="primary" class="register-btn" @click.native.prevent="submit">Submit</el-button>

      <el-alert v-show="error_show" title="Registration failed, please try again later." type="error" show-icon :closable="false" />

    </el-form>
  </div>
</template>

<script>
import 'vue-awesome/icons/envelope'
import 'vue-awesome/icons/user-ninja'
import 'vue-awesome/icons/user'
import 'vue-awesome/icons/lock'
import 'vue-awesome/icons/check-square'
import 'vue-awesome/icons/eye'
import 'vue-awesome/icons/eye-slash'
import { register } from '@api/auth.js'
const avatars = require('@assets/avatars.json')

export default {
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter password.'))
      } else {
        if (this.registerForm.checkPassword !== '') {
          this.$refs.register.validateField('checkPassword')
        }
        callback()
      }
    }
    const validateCheckPassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter the password again.'))
      } else if (value !== this.registerForm.password) {
        callback(new Error('The two passwords are inconsistent.'))
      } else {
        callback()
      }
    }

    return {
      avatars,
      registerForm: {
        email: '',
        nickname: '',
        password: '',
        checkPassword: ''
      },
      rules: {
        email: [
          { required: true, message: 'Please enter E-mail.', trigger: 'blur' },
          { type: 'email', message: 'Must be of type email.', trigger: 'blur' }
        ],
        nickname: [{ required: true, message: 'Please enter nickname.', trigger: 'blur' }],
        password: [{ validator: validatePassword, trigger: 'blur' }],
        checkPassword: [{ validator: validateCheckPassword, trigger: 'blur' }]
      },
      avatarIndex: 0,
      passwordType: 'password',
      checkPasswordType: 'password',
      loading: false,
      error_show: false,
      errorMessage: ''
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
    showCheckPwd() {
      if (this.checkPasswordType === 'password') {
        this.checkPasswordType = 'text'
      } else {
        this.checkPasswordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.checkPassword.focus()
      })
    },
    submit() {
      this.error_show = false
      this.$refs.register.validate(valid => {
        if (valid) {
          this.loading = true
          const submitData = {
            avatar: this.avatars[this.avatarIndex]
          }
          Object.assign(submitData, this.registerForm)
          delete submitData.checkPassword
          register(submitData).then(() => {
            this.loading = false
            this.$router.push({ name: 'Login' })
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
  .register-container .el-input input
    color: $cursor

/* reset element-ui css */
.register-container
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

.avatar-form-item .el-form-item__content
  display flex
</style>

<style lang="stylus" scoped>
$bg = #2d3a4b
$dark_gray = #889aa4
$light_gray = #eee

.register-container
  height 100vh
  background-color $bg
  overflow hidden
  display flex
  justify-content center
  align-items center

  .register-form
    width 520px
    max-width 100%
    height 586px

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

  .avatar-form-item
    ul
      flex 1
      padding 8px 10px 0 15px

    li
      float left
      height 30px
      margin 0 5px 5px 0
      cursor pointer
      border 1px solid transparent
      padding 3px
      border-radius 5px

      &.actived
        border-color rgb(121, 187, 255)

      img
        width 30px
        height 30px
        border-radius 100%

  .show-pwd
    position absolute
    right 10px
    top 7px
    font-size 16px
    color $dark_gray
    cursor pointer
    user-select none

  .register-btn
    width 100%
    margin-bottom 22px
</style>
