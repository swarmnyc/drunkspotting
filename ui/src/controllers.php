<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

function sendPost($url, $data)
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    $code     = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    curl_close($ch);

    return array(
        'response' => $response,
        'code'     => $code
    );
}

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

    $canvasImage->scaleImage(
        $backgroundImage->getImageWidth(),
        $backgroundImage->getImageHeight()
    );

    $canvasImage->stripImage();
    $backgroundImage->stripImage();

    $backgroundImage->compositeImage($canvasImage, Imagick::COMPOSITE_DEFAULT, 0, 0);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://api.drunkspotting.com/upload_picture");
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $backgroundImage->getImageBlob());
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: text/plain'));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $result = curl_exec($ch);
    $code   = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    $uploadPictureData = json_decode($result);

    $data = array(
        'title' => '',
        'latitude' => 0,
        'longitude' => 0,
        'description' => '',
        'url' => $uploadPictureData->url
    );

    $jsonData = json_encode($data);

    $templateResult = sendPost("http://api.drunkspotting.com/templates/", $jsonData);
    $templateData = json_decode($templateResult['response']);

    $data['template_id'] = $templateData->id;

    $jsonData = json_encode($data);

    $pictureResult = sendPost("http://api.drunkspotting.com/pictures/", $jsonData);

    return new Response($pictureResult['response'], $pictureResult['code'], array('Content-Type' => 'application/json'));
})->bind('upload');

$app->error(function (\Exception $e, $code) use ($app) {
    if ($app['debug']) {
        return;
    }

    $page = 404 == $code ? '404.html' : '500.html';

    return new Response($app['twig']->render($page, array('code' => $code)), $code);
});
