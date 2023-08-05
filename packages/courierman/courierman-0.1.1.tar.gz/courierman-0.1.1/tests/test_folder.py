from courierman.folder import Folder


def test_folder():
    sample_folder_json = {
        "name": "Cookies",
        "description": "The cookie related endpoints allow one to get, set and delete simple cookies.\n\nCookies are small snippets of information that is stored in the browser and sent back to the server with every subsequent requests in order to store useful information between requests.\nIf you want to know more about cookies, read the [HTTP Cookie](https://en.wikipedia.org/wiki/HTTP_cookie) article on wikipedia.",
        "item": [
            {
                "name": "Set Cookies",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "// handle case where it is 304",
                                "",
                                "if (responseCode.code === 200) {",
                                "    tests[\"Status code is 302 or 200\"] = true;",
                                "    tests[\"Body contains cookies\"] = responseBody.has(\"cookies\");",
                                "    ",
                                "    var body = JSON.parse(responseBody);",
                                "    tests[\"Body contains cookie foo1\"] = 'foo1' in body.cookies;",
                                "    tests[\"Body contains cookie foo2\"] = 'foo2' in body.cookies;",
                                "",
                                "}",
                                "else if (responseCode.code === 302) {",
                                "    tests[\"Status code is 302 or 200\"] = true;",
                                "    tests[\"Body has redirection message\"] = responseBody.has(\"Found. Redirecting to /cookies\")",
                                "}",
                                "else {",
                                "    tests[\"Status code is 302 or 200\"] = false;",
                                "}",
                                "",
                                "tests[\"foo1 cookie is set\"] = _.get(postman.getResponseCookie('foo1'), 'value') === 'bar1';",
                                "",
                                "tests[\"foo2 cookie is set\"] = _.get(postman.getResponseCookie('foo2'), 'value') === 'bar2';"
                            ]
                        }
                    }
                ],
                "request": {
                    "url": "https://postman-echo.com/cookies/set?foo1=bar1&foo2=bar2",
                    "method": "GET",
                    "header": [],
                    "body": {},
                    "description": "The cookie setter endpoint accepts a list of cookies and their values as part of URL parameters of a `GET` request. These cookies are saved and can be subsequently retrieved or deleted. The response of this request returns a JSON with all cookies listed.\n\nTo set your own set of cookies, simply replace the URL parameters \"foo1=bar1&foo2=bar2\" with your own set of key-value pairs."
                },
                "response": [
                    {
                        "id": "17f096a3-90c0-4426-972c-e329550979ff",
                        "name": "Cookies",
                        "originalRequest": {
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": ""
                            }
                        },
                        "status": "OK",
                        "code": 200,
                        "_postman_previewlanguage": "javascript",
                        "_postman_previewtype": "html",
                        "header": [
                            {
                                "name": "Access-Control-Allow-Credentials",
                                "key": "Access-Control-Allow-Credentials",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Headers",
                                "key": "Access-Control-Allow-Headers",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Methods",
                                "key": "Access-Control-Allow-Methods",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Origin",
                                "key": "Access-Control-Allow-Origin",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Connection",
                                "key": "Connection",
                                "value": "keep-alive",
                                "description": ""
                            },
                            {
                                "name": "Content-Encoding",
                                "key": "Content-Encoding",
                                "value": "gzip",
                                "description": ""
                            },
                            {
                                "name": "Content-Length",
                                "key": "Content-Length",
                                "value": "51",
                                "description": ""
                            },
                            {
                                "name": "Content-Type",
                                "key": "Content-Type",
                                "value": "application/json; charset=utf-8",
                                "description": ""
                            },
                            {
                                "name": "Date",
                                "key": "Date",
                                "value": "Thu, 29 Oct 2015 06:15:28 GMT",
                                "description": ""
                            },
                            {
                                "name": "Server",
                                "key": "Server",
                                "value": "nginx/1.6.2",
                                "description": ""
                            },
                            {
                                "name": "Vary",
                                "key": "Vary",
                                "value": "Accept-Encoding",
                                "description": ""
                            },
                            {
                                "name": "X-Powered-By",
                                "key": "X-Powered-By",
                                "value": "Sails <sailsjs.org>",
                                "description": ""
                            }
                        ],
                        "cookie": [],
                        "responseTime": "3063",
                        "body": "{\"cookies\":{\"foo1\":\"bar\",\"foo2\":\"bar\"}}"
                    }
                ]
            },
            {
                "name": "Get Cookies",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "var responseJSON;",
                                "try {",
                                "    tests[\"Body contains cookies\"] = responseBody.has(\"cookies\");",
                                "    responseJSON = JSON.parse(responseBody);",
                                "    tests[\"Cookies object is empty\"] = (Object.keys(responseJSON.cookies).length > 0)",
                                "}",
                                "catch (e) { }",
                                "",
                                "tests[\"Status code is 200\"] = responseCode.code === 200;",
                                ""
                            ]
                        }
                    }
                ],
                "request": {
                    "url": "https://postman-echo.com/cookies",
                    "method": "GET",
                    "header": [],
                    "body": {},
                    "description": "Use this endpoint to get a list of all cookies that are stored with respect to this domain. Whatever key-value pairs that has been previously set by calling the \"Set Cookies\" endpoint, will be returned as response JSON."
                },
                "response": [
                    {
                        "id": "527b6f9d-26ab-4b3a-8365-a4d87adcd320",
                        "name": "Cookies",
                        "originalRequest": {
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": ""
                            }
                        },
                        "status": "OK",
                        "code": 200,
                        "_postman_previewlanguage": "javascript",
                        "_postman_previewtype": "html",
                        "header": [
                            {
                                "name": "Access-Control-Allow-Credentials",
                                "key": "Access-Control-Allow-Credentials",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Headers",
                                "key": "Access-Control-Allow-Headers",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Methods",
                                "key": "Access-Control-Allow-Methods",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Origin",
                                "key": "Access-Control-Allow-Origin",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Connection",
                                "key": "Connection",
                                "value": "keep-alive",
                                "description": ""
                            },
                            {
                                "name": "Content-Encoding",
                                "key": "Content-Encoding",
                                "value": "gzip",
                                "description": ""
                            },
                            {
                                "name": "Content-Length",
                                "key": "Content-Length",
                                "value": "46",
                                "description": ""
                            },
                            {
                                "name": "Content-Type",
                                "key": "Content-Type",
                                "value": "application/json; charset=utf-8",
                                "description": ""
                            },
                            {
                                "name": "Date",
                                "key": "Date",
                                "value": "Thu, 29 Oct 2015 06:16:29 GMT",
                                "description": ""
                            },
                            {
                                "name": "Server",
                                "key": "Server",
                                "value": "nginx/1.6.2",
                                "description": ""
                            },
                            {
                                "name": "Vary",
                                "key": "Vary",
                                "value": "Accept-Encoding",
                                "description": ""
                            },
                            {
                                "name": "X-Powered-By",
                                "key": "X-Powered-By",
                                "value": "Sails <sailsjs.org>",
                                "description": ""
                            }
                        ],
                        "cookie": [],
                        "responseTime": "462",
                        "body": "{\"cookies\":{\"foo2\":\"bar\"}}"
                    }
                ]
            },
            {
                "name": "Delete Cookies",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "// handle case where it is 304",
                                "",
                                "if (responseCode.code === 200) {",
                                "    tests[\"Status code is 302 or 200\"] = true;",
                                "    tests[\"Body contains cookies\"] = responseBody.has(\"cookies\");",
                                "    ",
                                "    var body = JSON.parse(responseBody);",
                                "    tests[\"Body contains cookie foo1\"] = 'foo1' in body.cookies;",
                                "    tests[\"Body contains cookie foo2\"] = 'foo2' in body.cookies;",
                                "",
                                "}",
                                "else if (responseCode.code === 302) {",
                                "    tests[\"Status code is 302 or 200\"] = true;",
                                "    tests[\"Body has redirection message\"] = responseBody.has(\"Found. Redirecting to /cookies\")",
                                "}",
                                "else {",
                                "    tests[\"Status code is 302 or 200\"] = false;",
                                "}",
                                "",
                                "tests[\"foo1 cookie is set\"] = _.get(postman.getResponseCookie('foo1'), 'value') === undefined;",
                                "",
                                "tests[\"foo2 cookie is set\"] = _.get(postman.getResponseCookie('foo2'), 'value') === undefined;"
                            ]
                        }
                    }
                ],
                "request": {
                    "url": "https://postman-echo.com/cookies/delete?foo1&foo2",
                    "method": "GET",
                    "header": [],
                    "body": {},
                    "description": "One or more cookies that has been set for this domain can be deleted by providing the cookie names as part of the URL parameter. The response of this request is a JSON containing the list of currently set cookies."
                },
                "response": [
                    {
                        "id": "2b84bd0c-814b-4569-b5ab-8530857f4d4f",
                        "name": "Cookies Response",
                        "originalRequest": {
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": ""
                            }
                        },
                        "status": "OK",
                        "code": 200,
                        "_postman_previewlanguage": "javascript",
                        "_postman_previewtype": "html",
                        "header": [
                            {
                                "name": "Access-Control-Allow-Credentials",
                                "key": "Access-Control-Allow-Credentials",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Headers",
                                "key": "Access-Control-Allow-Headers",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Methods",
                                "key": "Access-Control-Allow-Methods",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Access-Control-Allow-Origin",
                                "key": "Access-Control-Allow-Origin",
                                "value": "",
                                "description": ""
                            },
                            {
                                "name": "Connection",
                                "key": "Connection",
                                "value": "keep-alive",
                                "description": ""
                            },
                            {
                                "name": "Content-Encoding",
                                "key": "Content-Encoding",
                                "value": "gzip",
                                "description": ""
                            },
                            {
                                "name": "Content-Length",
                                "key": "Content-Length",
                                "value": "46",
                                "description": ""
                            },
                            {
                                "name": "Content-Type",
                                "key": "Content-Type",
                                "value": "application/json; charset=utf-8",
                                "description": ""
                            },
                            {
                                "name": "Date",
                                "key": "Date",
                                "value": "Thu, 29 Oct 2015 06:16:00 GMT",
                                "description": ""
                            },
                            {
                                "name": "Server",
                                "key": "Server",
                                "value": "nginx/1.6.2",
                                "description": ""
                            },
                            {
                                "name": "Vary",
                                "key": "Vary",
                                "value": "Accept-Encoding",
                                "description": ""
                            },
                            {
                                "name": "X-Powered-By",
                                "key": "X-Powered-By",
                                "value": "Sails <sailsjs.org>",
                                "description": ""
                            }
                        ],
                        "cookie": [],
                        "responseTime": "1417",
                        "body": "{\"cookies\":{\"foo2\":\"bar\"}}"
                    }
                ]
            }
        ]
    }
    folder = Folder(json=sample_folder_json)
    assert folder.name == "Cookies"
    assert len(folder.items) == 3
