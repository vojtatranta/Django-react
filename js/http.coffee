express = require 'express'
React = require 'React'
require('node-jsx').install()

bodyParser = require 'body-parser'
multer = require 'multer'

app = express()

app.use bodyParser.json()  # for parsing application/json
app.use bodyParser.urlencoded( extended: true ) # for parsing application/x-www-form-urlencoded
app.use multer() # for parsing multipart/form-data

render = (template, data) ->
  React.renderToString React.createElement template, data

app.post '*', (req, res) ->
  res.send render(require(req.body['react_template_file']), req.body)

port = process.env.PORT || 3333
if not module.parent
  app.listen port
  console.log "Express started on port #{port}"

