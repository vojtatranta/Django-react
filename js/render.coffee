React = require 'react'

module.exports = render = (base, template, data) ->
  data['bodyHtml'] = React.renderToString React.createElement(template, data)
  React.renderToString React.createElement(base, data)
