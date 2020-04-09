const webpack = require('webpack')
const path = require('path')

function resolve (dir) {
  return path.join(__dirname, dir)
}

module.exports = {
  devServer: {
    port: 9099,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  chainWebpack: config => {
    config.plugin('provide').use(webpack.ProvidePlugin, [{
      axios: 'axios'
    }])

    config.resolve.alias.set('@assets', resolve('src/assets'))
    config.resolve.alias.set('@views', resolve('src/views'))
    config.resolve.alias.set('@components', resolve('src/components'))
    config.resolve.alias.set('@api', resolve('src/api'))
  },
  filenameHashing: false
}
