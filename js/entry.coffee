require('node-jsx').install()
React = require 'React'
render = require 'render'

djangoContextData = JSON.parse process.argv[2]
console.log(
    render(
      require(djangoContextData['react_base_template_file_path']['absolute']),
      require(djangoContextData['react_template_file_path']['absolute']), djangoContextData)
)

