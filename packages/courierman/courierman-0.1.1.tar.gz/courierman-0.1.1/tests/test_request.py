from courierman.request import Request


request_json = {
    "name": "Basic Auth",
    "event": [
        {
            "listen": "test",
            "script": {
                "type": "text/javascript",
                "exec": [
                    "tests[\"response code is 200\"] = responseCode.code === 200;",
                    "tests[\"Body contains authenticated\"] = responseBody.has(\"authenticated\");"
                ]
            }
        }
    ],
    "request": {
        "auth": {
            "type": "basic",
            "basic": {
                "username": "postman",
                "password": "password",
                "saveHelperData": True,
                "showPassword": False
            }
        },
        "url": "https://postman-echo.com/basic-auth",
        "method": "GET",
        "header": [
            {
                "key": "Authorization",
                "value": "Basic cG9zdG1hbjpwYXNzd29yZA==",
                "description": ""
            }
        ],
        "body": {},
        "description": "This endpoint simulates a **basic-auth** protected endpoint. \nThe endpoint accepts a default username and password and returns a status code of `200 ok` only if the same is provided. \nOtherwise it will return a status code `401 unauthorized`.\n\n> Username: `postman`\n> \n> Password: `password`\n\nTo use this endpoint, send a request with the header `Authorization: Basic cG9zdG1hbjpwYXNzd29yZA==`. \nThe cryptic latter half of the header value is a base64 encoded concatenation of the default username and password. \nUsing Postman, to send this request, you can simply fill in the username and password in the \"Authorization\" tab and Postman will do the rest for you.\n\nTo know more about basic authentication, refer to the [Basic Access Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) wikipedia article.\nThe article on [authentication helpers](https://www.getpostman.com/docs/helpers#basic-auth?source=echo-collection-app-onboarding) elaborates how to use the same within the Postman app."
    },
    "response": [
        {
            "id": "293117f0-35e9-4ad6-ad44-24cb03228b11",
            "name": "200",
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
                    "value": "42",
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
                    "value": "Sat, 31 Oct 2015 06:38:25 GMT",
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
            "responseTime": "377",
                            "body": "{\"authenticated\":true}"
        }
    ]
}


def test_request_info():
    request = Request(json=request_json)
    assert request.name == "Basic Auth"

def test_request_execute():
    # TODO: we should mock this API
    request = Request(json=request_json)
    ans = request.execute()
    assert ans.status_code == 200
