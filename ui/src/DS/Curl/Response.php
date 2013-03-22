<?php

namespace DS\Curl;

class Response
{
    const SUCCESS                = 200;
    const VALIDATION_ERROR       = 400;
    const AUTHENTICATION_ERROR   = 401;
    const GENERAL_ERROR          = 500;
    const MAINTENANCE_MODE_ERROR = 503;

    /**
     * @var string
     */
    public $rawResponse = null;

    /**
     * @var array
     */
    public $data = array();

    /**
     * @var int
     */
    public $code = null;

    /**
     * Constructor
     *
     * @param string $rawResponse The raw string that was returned
     * @param int    $code        The HTTP response code
     */
    public function __construct($rawResponse, $code)
    {
        $this->rawResponse = $rawResponse;
        $this->data        = json_decode($rawResponse);
        $this->code        = $code;
    }

    /**
     * Checks response code to determine a successful request
     *
     * @return boolean
     */
    public function isSuccessful()
    {
        return self::SUCCESS === $this->code;
    }
}
