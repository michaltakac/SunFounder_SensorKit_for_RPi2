const path = require('path')
const express = require('express')
const webpack = require('webpack');
const bodyParser = require('body-parser')
const cors = require('cors');
const proxy = require('express-http-proxy')
const assert = require('assert')
const webpackConfig = require('./webpack.config');
const compiler = webpack(webpackConfig);

const app = express()
const indexPath = path.join(__dirname, 'public', 'index.html')

if (process.env.NODE_ENV !== 'production') {
  app.use(require('webpack-dev-middleware')(compiler, {
    noInfo: true, publicPath: webpackConfig.output.publicPath
  }));

  app.use(require('webpack-hot-middleware')(compiler, {
    log: console.log, path: '/__webpack_hmr', heartbeat: 10 * 1000
  }));
}

const port = (process.env.PORT || 4040)

const sse = function (req, res, next) {
  res.sseSetup = () => {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': '',
      'X-Accel-Buffering': 'no'
    })
  }

  res.sseSend = (data) => {
    res.write('data: ' + JSON.stringify(data) + '\n\n')
  }

  next()
}

app.use(sse)
app.use(bodyParser.json())
app.get('/', function (_, res) { res.sendFile(indexPath) })
app.use(express.static(path.join(__dirname, 'public')))
app.use(cors())
app.use('/dist', express.static(path.join(__dirname, 'dist')))

app.listen(port)

console.log(`Listening at http://localhost:${port}`)
