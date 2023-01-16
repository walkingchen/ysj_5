const { defineConfig } = require('@vue/cli-service')
const path = require('path')

function resolve (dir) {
  return path.join(__dirname, dir)
}

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 9099,
    proxy: {
      '/api': {
        target: 'http://ysj_5.soulfar.com',
        changeOrigin: true
      },
      '/uploads': {
        target: 'http://ysj_5.soulfar.com',
        changeOrigin: true
      },
      '/socket.io': {
        target: 'http://ysj_5.soulfar.com',
        ws: true,
        changeOrigin: true
      }
    }
  },
  chainWebpack: config => {
    config.resolve.alias.set('@assets', resolve('src/assets'))
    config.resolve.alias.set('@views', resolve('src/views'))
    config.resolve.alias.set('@components', resolve('src/components'))
    config.resolve.alias.set('@api', resolve('src/api'))
  },
  filenameHashing: false
})
