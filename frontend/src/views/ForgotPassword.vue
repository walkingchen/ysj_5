<template>
  <main class="password-auth">
    <section class="password-auth__form" aria-labelledby="forgot-title">
      <h1 id="forgot-title" class="password-auth__title">Reset your password</h1>
      <p class="password-auth__description">Enter the email address you used to register with Chattera. We'll send you a link to set a new password.</p>

      <el-form v-if="!submitted" ref="form" :model="form" :rules="rules" @submit.native.prevent="submit">
        <el-form-item prop="email" class="password-auth__field">
          <span class="password-auth__icon" aria-hidden="true"><v-icon name="envelope" /></span>
          <el-input v-model.trim="form.email" type="email" placeholder="E-mail" aria-label="E-mail" autocomplete="email" @keyup.enter.native="submit" />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" class="password-auth__button">Send reset link</el-button>
        <el-alert v-if="error" :title="error" type="error" :closable="false" show-icon class="password-auth__alert" />
      </el-form>

      <div v-else class="password-auth__message" role="status">
        <v-icon name="envelope" class="password-auth__message-icon" aria-hidden="true" />
        <p>If an account exists for <strong>{{ form.email }}</strong>, a reset link will be sent. Please check your inbox.</p>
      </div>

      <div class="password-auth__footer">
        <el-link type="primary" @click="$router.push({ name: 'Login' })">Back to login</el-link>
      </div>
    </section>
  </main>
</template>

<script>
import 'vue-awesome/icons/envelope'
import { requestPasswordReset } from '@api/auth'
import '@assets/password-auth.css'

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
