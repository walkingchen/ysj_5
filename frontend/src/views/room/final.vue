<template>
    <div class="study-info">
      <div class="logo-container">
        <img src="assets/logo.png" alt="Site Logo" class="site-logo">
      </div>
      <h1>Thank You!</h1>
      <p>Thank you for your participation in this study! Your contribution is invaluable to our research.</p>
      <p>
        To help us further understand your experience, please complete the
        <a href="link" target="_blank">post-experiment survey</a>. Your feedback is essential to us and greatly appreciated.
      </p>
      <p>
        Please use the unique code <strong>EXP12345</strong> to access the survey.
      </p>
      <p>
        You will receive $xx as compensation for participating in this study. Upon completion of the survey, your payment will be processed within xx business days. If you have any questions or concerns regarding your payment, please contact our team at
        <a href="mailto:support@example.com">support@example.com</a>.
      </p>
      <p>Thank you once again for your time and effort!</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'StudyInfo',
  };
  </script>
  
  <style scoped>
  .study-info {
    font-family: Arial, sans-serif;
    margin: 20px;
  }
  
  .logo-container {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .site-logo {
    max-width: 150px;
  }
  
  .study-info h1 {
    color: #2c3e50;
  }
  
  .study-info p {
    margin: 10px 0;
  }
  
  .study-info a {
    color: #3498db;
    text-decoration: none;
  }
  
  .study-info a:hover {
    text-decoration: underline;
  }
  </style>
  