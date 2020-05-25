<template>
  <login :to-router="{ name: 'Admin' }" />
</template>

<script>
import login from '@components/login'

export default {
  components: {
    login
  }
}
</script>
