<template>
  <div class="password-page">
    <el-card class="password-card">
      <h2>Set a new password</h2>
      <el-alert v-if="!token" title="This reset link is invalid. Please request a new one." type="error" :closable="false" show-icon />
      <el-form v-else-if="!complete" ref="form" :model="form" :rules="rules" @submit.native.prevent="submit">
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="New password (at least 12 characters)" autocomplete="new-password" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="Confirm new password" autocomplete="new-password" show-password />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" class="full-button">Reset password</el-button>
        <el-alert v-if="error" :title="error" type="error" :closable="false" show-icon class="form-alert" />
      </el-form>
      <el-alert v-else title="Your password has been reset. Please sign in with your new password." type="success" :closable="false" show-icon />
      <el-link type="primary" class="back-link" @click="$router.push({ name: complete ? 'Login' : 'ForgotPassword' })">{{ complete ? 'Go to login' : 'Request a new link' }}</el-link>
    </el-card>
  </div>
</template>

<script>
import { confirmPasswordReset } from '@api/auth'

export default {
  data() {
    return {
      token: this.$route.query.token || '',
      form: { password: '', confirmPassword: '' },
      rules: {
        password: [
          { required: true, message: 'Please enter a new password.', trigger: 'blur' },
          { min: 12, max: 128, message: 'Use 12 to 128 characters.', trigger: 'blur' }
        ],
        confirmPassword: [{ validator: (rule, value, callback) => {
          if (value !== this.form.password) callback(new Error('Passwords do not match.'))
          else callback()
        }, trigger: 'blur' }]
      },
      loading: false,
      complete: false,
      error: ''
    }
  },
  methods: {
    submit() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.loading = true
        this.error = ''
        confirmPasswordReset(this.token, this.form.password).then(res => {
          if (res.data.result_code === 2000) {
            this.complete = true
            this.token = ''
            this.form.password = ''
            this.form.confirmPassword = ''
            localStorage.removeItem('roomid')
            this.$router.replace({ name: 'ResetPassword' })
          } else this.error = res.data.result_msg || 'Unable to reset your password.'
        }).catch(() => {
          this.error = 'Unable to reset your password. Please try again.'
        }).finally(() => { this.loading = false })
      })
    }
  }
}
</script>

<style scoped>
.password-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #2d3a4b; padding: 20px; box-sizing: border-box; }
.password-card { width: 420px; max-width: 100%; }
h2 { margin: 0 0 24px; }
.full-button { width: 100%; }
.form-alert { margin-top: 16px; }
.back-link { margin-top: 22px; }
</style>
