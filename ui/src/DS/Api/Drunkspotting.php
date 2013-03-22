<?php

namespace DS\Api;

class Drunkspotting extends ApiAbstract
{
    public function __construct($endpoint = '')
    {
        $this->endpoint = $endpoint;
    }

    protected function uploadTemplate($pictureBlob)
    {
        $request = $this->setupRequest(
            'upload_template',
            'POST',
            $pictureBlob
        );

        $request->addHeader('Content-Type', 'text/plain');

        return $request;
    }

    protected function uploadPicture($pictureBlob)
    {
        $request = $this->setupRequest(
            'upload_picture',
            'POST',
            $pictureBlob
        );

        $request->addHeader('Content-Type', 'text/plain');

        return $request;
    }

    protected function pictures(array $data = array())
    {
        $request = $this->setupRequest(
            'pictures/',
            'POST',
            json_encode($data)
        );

        $request->addHeader('Content-Type', 'application/json');

        return $request;
    }

    protected function getPicture($id)
    {
        return $this->setupRequest(
            'pictures/' . $id,
            'GET',
            array()
        );
    }
}
