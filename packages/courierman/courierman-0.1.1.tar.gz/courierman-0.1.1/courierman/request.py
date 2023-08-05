import requests

from courierman.postman_entry import PostmanEntry


class Request(PostmanEntry):

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        self._method = None
        self._auth = None
        self._body = None
        self._headers = None
        self._url = None
        self._description = None

    def execute(self):
        return requests.request(self.method, self.url, data=self._body, headers=self.headers)

    @property
    def name(self):
        return self._json["name"]

    @property
    def headers(self):
        if self._headers is None:
            self._update_request_info()
        headers = {}
        for header in self._headers:
            headers[header["key"]] = header["value"]
        return headers

    @property
    def method(self):
        if not self._method:
            self._update_request_info()
        return self._method

    @property
    def url(self):
        if not self._url:
            self._update_request_info()
        return self._url

    @property
    def body(self):
        if not self._body:
            self._update_request_info()
        if self._body["mode"] == "raw":
            body = self._body["raw"]
        else:
            raise NotImplementedError("Other body modes not suported")
        return body

    @property
    def description(self):
        if not self._description:
            self._update_request_info()
        return self._description

    def _update_request_info(self):
        self._method = self._json["request"]["method"]
        self._auth = self._json["request"].get("auth")
        self._body = self._json["request"]["body"]
        self._headers = self._json["request"]["header"]
        self._url = self._json["request"]["url"]
        self._description = self._json["request"]["description"]

    def foo(self):
        x = {'auth': {'type': 'basic',
                   'basic': {'username': 'postman', 'password': 'password', 'saveHelperData': True,
                             'showPassword': False}},
            'url': 'https://postman-echo.com/basic-auth',
          'method': 'GET',
          'header': [{'key': 'Authorization', 'value': 'Basic cG9zdG1hbjpwYXNzd29yZA==', 'description': ''}],
          'body': {},
          'description': 'This endpoint simulates a **basic-auth** protected endpoint. \nThe endpoint accepts a default username and password and returns a status code of `200 ok` only if the same is provided. \nOtherwise it will return a status code `401 unauthorized`.\n\n> Username: `postman`\n> \n> Password: `password`\n\nTo use this endpoint, send a request with the header `Authorization: Basic cG9zdG1hbjpwYXNzd29yZA==`. \nThe cryptic latter half of the header value is a base64 encoded concatenation of the default username and password. \nUsing Postman, to send this request, you can simply fill in the username and password in the "Authorization" tab and Postman will do the rest for you.\n\nTo know more about basic authentication, refer to the [Basic Access Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) wikipedia article.\nThe article on [authentication helpers](https://www.getpostman.com/docs/helpers#basic-auth?source=echo-collection-app-onboarding) elaborates how to use the same within the Postman app.'}
