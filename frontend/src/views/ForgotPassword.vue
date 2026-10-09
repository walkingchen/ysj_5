<template>
  <div class="password-page">
    <el-card class="password-card">
      <h2>Reset your password</h2>
      <p>Enter your Chattera email address and we'll send you a reset link.</p>
      <el-form v-if="!submitted" ref="form" :model="form" :rules="rules" @submit.native.prevent="submit">
        <el-form-item prop="email">
          <el-input v-model.trim="form.email" type="email" placeholder="Email address" autocomplete="email" />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" class="full-button">Send reset link</el-button>
        <el-alert v-if="error" :title="error" type="error" :closable="false" show-icon class="form-alert" />
      </el-form>
      <el-alert v-else title="If an account exists for this email, a reset link will be sent. Please check your inbox." type="success" :closable="false" show-icon />
      <el-link type="primary" class="back-link" @click="$router.push({ name: 'Login' })">Back to login</el-link>
    </el-card>
  </div>
</template>

<script>
import { requestPasswordReset } from '@api/auth'

export default {
  data() {
    return {
      form: { email: '' },
      rules: { email: [
        { required: true, message: 'Please enter your email address.', trigger: 'blur' },
        { type: 'email', message: 'Please enter a valid email address.', trigger: 'blur' }
      ] },
      loading: false,
      submitted: false,
      error: ''
    }
  },
  methods: {
    submit() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.loading = true
        this.error = ''
        requestPasswordReset(this.form.email).then(res => {
          if (res.data.result_code === 2000) this.submitted = true
          else this.error = res.data.result_msg || 'Unable to send the reset link.'
        }).catch(() => {
          this.error = 'Unable to send the reset link. Please try again.'
        }).finally(() => { this.loading = false })
      })
    }
  }
}
</script>

<style scoped>
.password-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #2d3a4b; padding: 20px; box-sizing: border-box; }
.password-card { width: 420px; max-width: 100%; }
h2 { margin: 0 0 12px; }
p { color: #606266; line-height: 1.5; margin-bottom: 24px; }
.full-button { width: 100%; }
.form-alert { margin-top: 16px; }
.back-link { margin-top: 22px; }
</style>
