<?php

// Dev use
use Symfony\Component\ClassLoader\DebugClassLoader;
use Symfony\Component\HttpKernel\Debug\ErrorHandler;
use Symfony\Component\HttpKernel\Debug\ExceptionHandler;

require_once __DIR__.'/../vendor/autoload.php';

// Get the current environment and debug mode from server headers
$env = isset($_SERVER['SYMFONY_ENV']) ? $_SERVER['SYMFONY_ENV'] : 'prod';
$debug = (isset($_SERVER['SYMFONY_DEBUG']) && $_SERVER['SYMFONY_DEBUG'] === 'true') ? true : false;

ini_set('display_errors', 0);
$configFile = __DIR__.'/../config/prod.php';

if ("dev" === $env) {
  error_reporting(-1);
  DebugClassLoader::enable();
  ErrorHandler::register();
  if ('cli' !== php_sapi_name()) {
      ExceptionHandler::register();
  }

  $configFile = __DIR__.'/../config/dev.php';
}

$app = require __DIR__.'/../src/app.php';
require $configFile;
require __DIR__.'/../src/controllers.php';
$app->run();
