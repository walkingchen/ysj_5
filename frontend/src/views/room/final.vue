<template>
  <div class="study-info">
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Site Logo">
    </div>
    <h1>Thank You!</h1>
    <p>Thank you for your participation in this study! Your contribution is invaluable to our research.</p>
    <p>To help us further understand your experience, please complete the <a href="link" target="_blank">post-experiment survey</a>. Your feedback is essential to us and greatly appreciated.</p>
    <p>Please use the unique code <strong>EXP12345</strong> to access the survey.</p>
    <p>You will receive $xx as compensation for participating in this study. Upon completion of the survey, your payment will be processed within xx business days. If you have any questions or concerns regarding your payment, please contact our team at <a href="mailto:support@example.com">support@example.com</a>.</p>
    <p>Thank you once again for your time and effort!</p>
  </div>
</template>

<style lang="stylus" scoped>
.study-info
  width 50%
  min-width 600px
  margin 20px auto

  h1
    color #2c3e50

  p
    margin 10px 0

  a
    color #3498db
    text-decoration none

    &:hover
      text-decoration underline

.logo-container
  text-align center
  margin-bottom 20px

  img
    max-width 150px
</style>
  