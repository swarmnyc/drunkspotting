<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * Home Page
 *
 * Route: /
 * Name: homepage
 */
$app->get('/', function () use ($app) {
    return $app['twig']->render('index.html', array());
})->bind('homepage');

/**
 * About
 *
 * Route: /about
 * Name: about
 */
$app->get('/about', function () use ($app) {
    return $app['twig']->render('about.html', array());
})->bind('about');

/**
 * Spot
 *
 * Route: /spot/{id}
 * Name: spot
 */
$app->get('/spot/{id}', function ($id) use ($app) {
    $dsApi = $app['drunkspotting_api'];
    $spot = $dsApi->executeGetPicture($id);

    if (!$spot->isSuccessful()) {
        throw new NotFoundHttpException('That drunkspot was not found.', null, 404);
    }

    return $app['twig']->render('spot.html', array('spot' => $spot, 'id' =>$id));
})->bind('spot');

/**
 * Upload Template
 *
 * Route: /upload/template
 * Name: upload_template
 */
$app->post('/upload/template', function () use ($app) {
    $dsApi   = $app['drunkspotting_api'];
    $request = $app['request'];

    if (!$request->files->has('file')) {
        throw new \Exception('Missing required "file" input value.');
    }

    $templateImage = new Imagick($request->files->get('file')->getPathname());

    $templateImage->stripImage();

    $templateImage->setImageCompressionQuality(50);

    $uploadTemplateResult = $dsApi->executeUploadTemplate($templateImage->getImageBlob());

    unlink($request->files->get('file')->getPathname());

    return new Response($uploadTemplateResult->rawResponse, $uploadTemplateResult->code, array('Content-Type' => 'application/json'));
})->bind('upload_template');


/**
 * Upload Picture
 *
 * Route: /upload/picture
 * Name: upload_picture
 */
$app->post('/upload/picture', function () use ($app) {
    $dsApi   = $app['drunkspotting_api'];
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

    $uploadPictureData = $dsApi->executeUploadPicture($backgroundImage->getImageBlob());

    $data = array(
        'template_id' => 0,
        'title' => '',
        'latitude' => 0,
        'longitude' => 0,
        'description' => '',
        'url' => $uploadPictureData->data->url
    );

    $pictureResult = $dsApi->executePictures($data);

    unlink($canvasImageTemp);

    return new Response($pictureResult->rawResponse, $pictureResult->code, array('Content-Type' => 'application/json'));
})->bind('upload_picture');

$app->error(function (\Exception $e, $code) use ($app) {
    if ($app['debug']) {
        return;
    }

    $page = 404 == $code ? '404.html' : '500.html';

    return new Response($app['twig']->render($page, array('code' => $code)), $code);
});
