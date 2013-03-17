<?php

namespace DS\Api;

use DS\Curl\Request;

abstract class ApiAbstract
{
    /**
     * @var DS\Curl\Request
     */
    protected $lastRequest = null;

    /**
     * @var string
     */
    protected $endpoint = null;

    /**
     * Setup the magic wrapper methods
     *
     * @param  string $name
     * @param  array  $arguments
     *
     * @return mixed
     */
    public function __call($name, $arguments) {
        // Decide what the call type will be.
        // Kinda nasty, but functional.
        $callType = 0 === strpos($name, "setup")
                    ? "setup"
                    : (0 === strpos($name, "execute")
                        ? "execute"
                        : false);

        // Opps must be an invalid call type
        if (false === $callType) {
            throw new BadFunctionCallException(sprintf("The method, '%s', that you have requested is not valid.", $name));
        }

        // Create the actual method name from the magic method name
        $method = lcfirst(str_replace($callType, "", $name));

        // Execute the method that will setup the API call
        $request = call_user_func_array(array($this, $method), $arguments);

        // Store here so someone can easily debug the last request
        $this->lastRequest = $request;

        // Simple switch to determine what should be returned back from this call
        switch ($callType) {
            case "setup":
                return $request->buildRequest();
                break;

            case "execute":
                return $request->execute();
                break;
        }
    }

    /**
     * Get the last setup request
     *
     * @return DS\Curl\Request
     */
    public function getLastRequest()
    {
        return $this->lastRequest;
    }

    /**
     * Sets up the SmartlingRequest based on the provided params
     *
     * @param  string $uri    URI for the API call
     * @param  string $method The HTTP method to be used
     * @param  array  $data   Array of data to be sent with request
     *
     * @return Request
     */
    protected function setupRequest($uri, $method, $data = '')
    {
        $request = new Request($this->endpoint);
        $request->setUri($uri)
                ->setRequestMethod($method)
                ->setData($data);

        return $request;
    }
}
