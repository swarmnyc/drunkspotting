<?php

namespace DS\Curl;

use DS\Curl\Response;

class Request
{
    /**
     * @var array
     */
    protected $endpoint = null;

    /**
     * @var string
     */
    protected $uri = null;

    /**
     * @var string
     */
    protected $requestMethod = null;

    /**
     * @var array
     */
    protected $data = array();

    /**
     * @var string
     */
    protected $url = null;

    /**
     * @var array
     */
    protected $headers = array();

    /**
     * @var string
     */
    protected $queryString = null;

    /**
     * @var SmartlingApiResponse
     */
    protected $response = null;

    /**
     * Constructor
     * Load all config info
     */
    public function __construct($endpoint = '')
    {
        $this->endpoint = $endpoint;
    }

    /**
     * Set the URI to use
     *
     * @param string $uri
     *
     * @return Request
     */
    public function setUri($uri)
    {
        $this->uri = $uri;
        return $this;
    }

    /**
     * Get the current set URI
     *
     * @return string
     */
    public function getUri()
    {
        return $this->uri;
    }

    /**
     * Set the HTTP request method to use
     *
     * @param string $requestMethod
     *
     * @return Request
     */
    public function setRequestMethod($requestMethod)
    {
        $this->requestMethod = $requestMethod;
        return $this;
    }

    /**
     * Get the current set HTTP request method
     *
     * @return string
     */
    public function getRequestMethod()
    {
        return $this->requestMethod;
    }

    /**
     * Set the data to use for the API call.
     *
     * @param array $data
     *
     * @return Request
     */
    public function setData($data = '')
    {
        $this->data = $data;

        return $this;
    }

    /**
     * Get the current set data
     *
     * @return array
     */
    public function getData()
    {
        return $this->data;
    }

    /**
     * Get the HTTP query string for the request.
     * This is built from the data array that is set.
     *
     * @return string
     */
    public function getQueryString()
    {
        if (null === $this->queryString) {
            $this->queryString = http_build_query($this->getData());
        }

        return $this->queryString;
    }

    /**
     * Get the built URL that will be sent the API request
     *
     * @return string
     */
    public function getUrl()
    {
        return $this->url;
    }

    /**
     * Add headers to be used during the API request
     *
     * @param string $name
     * @param string $value
     *
     * @return Request
     */
    public function addHeader($name, $value)
    {
        $this->headers[$name] = $value;
        return $this;
    }

    /**
     * If the request has beene executed, this will
     * contain that requests response object
     *
     * @return SmartlingApiResponse
     */
    public function getResponse()
    {
        return $this->response;
    }

    /**
     * Sets up everything needed to execute the request
     *
     * @return Request
     */
    public function buildRequest()
    {
        $this->url         = $this->endpoint . '/' . $this->getUri();
        $this->queryString = is_array($this->getData())
                              ? http_build_query($this->getData())
                              : $this->getData();

        return $this;
    }

    /**
     * Execute API request
     *
     * @return SmartlingApiResponse
     */
    public function execute() {

        // Need to build request first
        if (null === $this->getUrl()) {
            $this->buildRequest();
        }

        $url  = $this->getUrl();
        $data = $this->getQueryString();

        $handle = curl_init();

        switch ($this->getRequestMethod()) {
            case 'GET':
                if (!empty($data)) {
                    $url .= '?' . $data;
                }
                break;

            case 'POST':
                curl_setopt($handle, CURLOPT_POST, true);
                curl_setopt($handle, CURLOPT_POSTFIELDS, $this->getData());
                break;

            case 'PUT':
                curl_setopt($handle, CURLOPT_PUT, true);
                // Open memory stream
                $fileHandle = fopen('php://temp/maxmemory:6000', 'w');
                fwrite($fileHandle, $data);
                fseek($fileHandle, 0);
                // Send file
                curl_setopt($handle, CURLOPT_INFILE, $fileHandle);
                curl_setopt($handle, CURLOPT_INFILESIZE, strlen($data));
                break;

            case 'DELETE':
                if (!empty($data)) {
                    $url .= '?' . $data;
                }
                curl_setopt($handle, CURLOPT_CUSTOMREQUEST, 'DELETE');
                break;
        }

        // We need to create the headers in their string format
        $headers = array();
        if (!empty($this->_headers)) {
            foreach ($this->_headers as $key => $value) {
                $headers[] = $key . ": " . $value;
            }
        }

        curl_setopt($handle, CURLOPT_URL, $url);

        if (!empty($headers)) {
            curl_setopt($handle, CURLOPT_HTTPHEADER, $headers);
        }

        curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($handle, CURLOPT_SSL_VERIFYHOST, false);

        $response = curl_exec($handle);
        $code     = curl_getinfo($handle, CURLINFO_HTTP_CODE);

        $this->response = new Response($response, $code);

        curl_close($handle);

        return $this->response;
    }
}
