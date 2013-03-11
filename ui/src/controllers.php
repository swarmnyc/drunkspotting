<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

$app->get('/', function () use ($app) {
    return $app['twig']->render('index.html', array());
})->bind('homepage');


$app->get('/about', function () use ($app) {
    return $app['twig']->render('about.html', array());
})->bind('about');

$app->post('/upload', function () use ($app) {
    $request = $app['request'];

    $postContent = $request->getContent();

    list($imageUrl, $canvasData) = explode(':endurl:', $postContent);
    
    list(, $canvasBase64) = explode('base64,', $canvasData);

    $canvasImageTemp = tempnam(sys_get_temp_dir(), 'Canvas');
    file_put_contents($canvasImageTemp, base64_decode($canvasBase64));

    $backgroundImage = new Imagick($imageUrl);
    $canvasImage     = new Imagick($canvasImageTemp);

    $backgroundImage->compositeImage($canvasImage, Imagick::COMPOSITE_DEFAULT, 0, 0);

    $backgroundImage->getImageBlob();

    return new JsonResponse(array('success' => true));
})->bind('upload');

$app->error(function (\Exception $e, $code) use ($app) {
    if ($app['debug']) {
        return;
    }

    $page = 404 == $code ? '404.html' : '500.html';

    return new Response($app['twig']->render($page, array('code' => $code)), $code);
});
