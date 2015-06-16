var express = require('express');
var React = require('React');
require('node-jsx').install();

var bodyParser = require('body-parser');
var multer = require('multer');

var app = express();

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
app.use(multer()); // for parsing multipart/form-data

var render = function(template, data)
{
    return React.renderToString(React.createElement(template, data));
};


app.post('*', function(req, res)
{
    res.send(
        render(require(req.body['react_template_file']), req.body)
    );

});

var port = process.env.PORT || 3333;
if (!module.parent) {
  app.listen(port);
  console.log('Express started on port ' + port);
}
