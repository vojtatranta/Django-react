require('node-jsx').install();
var React = require('React');

var render = function(template, data)
{
    return React.renderToString(React.createElement(template, data));
};

var djangoContextData = JSON.parse(process.argv[2]);
console.log(
    render(require(djangoContextData['react_template_file']), djangoContextData)
);

