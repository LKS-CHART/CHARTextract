
let createError = require('http-errors');
let express = require('express');
let app = express();
let path = require('path');
let cookieParser = require('cookie-parser');
let logger = require('morgan');
let indexRouter = require('./routes/index');
let saveRouter = require('./routes/save');
let runRouter = require('./routes/run');
let loadRouter = require('./routes/load');
let pathRouter = require('./routes/path');
let deleteRouter = require('./routes/delete');
let dataRouter = require('./routes/data');
var cors = require('cors');

// view engine setup
app.use('/data', dataRouter);
//app.use(express.static('public'));
app.use(cors());

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/save', saveRouter);
app.use('/run', runRouter);
app.use('/load', loadRouter);
app.use('/path', pathRouter);
app.use('/delete', deleteRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


module.exports = app;
