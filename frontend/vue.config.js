// module.exports = {
//   transpileDependencies: []
// };


module.exports = {
  configureWebpack: {
    resolve: {
      extensions: ['.js', '.vue', '.json' ],
      alias: {
        'vue$': 'vue/dist/vue.esm-bundler.js'
      }
    }
  }
}

