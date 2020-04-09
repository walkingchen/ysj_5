module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential',
    '@vue/standard'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'space-before-function-paren': 0,
    'no-undef': 0,
    'camelcase': 0,
    'vue/no-side-effects-in-computed-properties': 0,
    'no-empty-pattern': 0,
    'vue/no-async-in-computed-properties': 0
  }
}
