var path = require('path');
var childProcess = require('child_process');
var webpack = require('webpack');

// Add HMR for development environments only.
var entry = ['./src/app.js'];
if (process.env.NODE_ENV !== 'production') {
  entry = [
    'webpack-hot-middleware/client?path=/__webpack_hmr&timeout=20000&reload=true'
  ].concat(entry);
}
// Minification.
var plugins = [
  new webpack.DefinePlugin({
    'process.env':{
      'NODE_ENV': JSON.stringify(process.env.NODE_ENV)
    },
    VERSION: JSON.stringify(require('./package.json').version)
  }),
];
if (process.env.NODE_ENV === 'production') {
  plugins.push(new webpack.optimize.UglifyJsPlugin({
    compress: {warnings: false}
  }));
} else {
  // Development
  plugins.push(new webpack.NamedModulesPlugin());
  plugins.push(new webpack.HotModuleReplacementPlugin());
  plugins.push(new webpack.NoEmitOnErrorsPlugin());
}

// dist/
var filename = 'sensorkit-app.js';
var outPath = 'dist';
if (process.env.AFRAME_DIST) {
  outPath = 'dist';
  if (process.env.NODE_ENV === 'production') {
    filename = 'sensorkit-app.min.js';
  }
}

const PATH = (process.env.CI && process.env.CIRCLE_BRANCH !== 'master')
  ? '/branch/' + process.env.CIRCLE_BRANCH + '/dist/'
  : '/dist/'

module.exports = {
  devServer: {
    contentBase: './dist',
    disableHostCheck: true,
    hot: true
  },
  entry: entry,
  output: {
    path: path.join(__dirname, outPath),
    filename: filename,
    publicPath: PATH
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'ify-loader'
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env', 'es2015', 'react'],
            plugins: ['transform-object-rest-spread', 'transform-class-properties']
          }
        }
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          { loader: 'css-loader', options: { importLoaders: 1 } }
        ]
      },
      {
        test: /\.scss$/,
        use: [{
          loader: 'style-loader'
        }, {
          loader: 'css-loader'
        }, {
          loader: 'sass-loader'
        }]
      }
    ]
  },
  plugins: plugins
};
