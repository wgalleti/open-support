const { defineConfig } = require('@vue/cli-service')

module.exports =
  defineConfig({
    transpileDependencies: true,
    lintOnSave: false,
    configureWebpack: {
      optimization: {
        splitChunks: {
          minSize: 10000,
          maxSize: 200000
        }
      }
    }
  })
