<template>
  <login :to-router="{ path: '/' }" />
</template>

<script>
import login from '@components/login'

export default {
  components: {
    login
  }
}
</script>
