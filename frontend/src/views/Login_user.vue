<template>
  <login :to-router="{ path: '/' }">
    <div style="text-align: center">
      <el-link type="primary" href="javascript:;" @click.native.prevent="$router.push({ name: 'Register' })">Register</el-link>
      <span style="margin: 0 12px; color: #889aa4">·</span>
      <el-link type="primary" href="javascript:;" @click.native.prevent="$router.push({ name: 'ForgotPassword' })">Forgot password?</el-link>
    </div>
  </login>
</template>

<script>
import login from '@components/login'

export default {
  components: {
    login
  }
}
</script>
