<template>
  <main class="password-auth">
    <section class="password-auth__form" aria-labelledby="reset-title">
      <h1 id="reset-title" class="password-auth__title">Set a new password</h1>
      <p v-if="token && !complete" class="password-auth__description">Choose a password with at least 12 characters.</p>

      <div v-if="!token && !complete" class="password-auth__message" role="alert">
        <p>This reset link is invalid or has expired. Please request a new one.</p>
      </div>
      <el-form v-else-if="!complete" ref="form" :model="form" :rules="rules" @submit.native.prevent="submit">
        <el-form-item prop="password" class="password-auth__field">
          <span class="password-auth__icon" aria-hidden="true"><v-icon name="lock" /></span>
          <el-input v-model="form.password" type="password" placeholder="New password" aria-label="New password" autocomplete="new-password" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword" class="password-auth__field">
          <span class="password-auth__icon" aria-hidden="true"><v-icon name="lock" /></span>
          <el-input v-model="form.confirmPassword" type="password" placeholder="Confirm new password" aria-label="Confirm new password" autocomplete="new-password" show-password />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" class="password-auth__button">Reset password</el-button>
        <el-alert v-if="error" :title="error" type="error" :closable="false" show-icon class="password-auth__alert" />
      </el-form>
      <div v-else class="password-auth__message" role="status">
        <p>Your password has been reset. Please sign in with your new password.</p>
      </div>

      <div class="password-auth__footer">
        <el-link type="primary" @click="$router.push({ name: complete ? 'Login' : 'ForgotPassword' })">{{ complete ? 'Go to login' : 'Request a new link' }}</el-link>
      </div>
    </section>
  </main>
</template>

<script>
import 'vue-awesome/icons/lock'
import { confirmPasswordReset } from '@api/auth'
import '@assets/password-auth.css'

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
