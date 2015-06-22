express = require 'express'
React = require 'React'
require 'coffee-react/register'
require('node-jsx').install()

bodyParser = require 'body-parser'
multer = require 'multer'

render = require './render'

app = express()

app.use bodyParser.json()  # for parsing application/json
app.use bodyParser.urlencoded( extended: true ) # for parsing application/x-www-form-urlencoded
app.use multer() # for parsing multipart/form-data


app.post '*', (req, res) ->
  res.send '<!doctype html>' +
    render(require(req.body['react_base_template_file_path']['absolute']),
      require(req.body['react_template_file_path']['absolute']), req.body)

port = process.env.PORT || 3333
if not module.parent
  app.listen port
  console.log "Express started on port #{port}"

