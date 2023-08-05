import os
from courierman.postman_entry import PostmanEntry
from courierman.folder import Folder
from courierman.collection import Collection
from courierman.request import Request

import pytest


def test_postman_entry():
    postman_entry = PostmanEntry(os.path.join(
        "../", "samples", "Postman Echo.postman_collection.json"))
    assert len(postman_entry.items) == 8


testdata = [
    ({
        "variables": [],
        "info": {
            "name": "Postman Echo",
            "_postman_id": "f695cab7-6878-eb55-7943-ad88e1ccfd65",
            "description": "Postman Echo is service you can use to test your REST clients and make sample API calls. It provides endpoints for `GET`, `POST`, `PUT`, various auth mechanisms and other utility endpoints.\n\nThe documentation for the endpoints as well as example responses can be found at [https://postman-echo.com](https://postman-echo.com/?source=echo-collection-app-onboarding)",
            "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
        }
    }, Collection),
    ({
        "name": "Utilities / Postman Collection",
        "description": "",
        "item": []
    }, Folder),
    ({
        "name": "Utilities / Postman Collection",
        "description": "",
        "item": []
    }, Folder),
    ({
        "name": "DigestAuth Request",
        "event": [
            {
                "listen": "test",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "tests[\"response code is 401\"] = responseCode.code === 401;",
                        "tests[\"response has WWW-Authenticate header\"] = (postman.getResponseHeader('WWW-Authenticate'));",
                        "",
                        "var authenticateHeader = postman.getResponseHeader('WWW-Authenticate'),",
                        "    realmStart = authenticateHeader.indexOf('\"',authenticateHeader.indexOf(\"realm\")) + 1 ,",
                        "    realmEnd = authenticateHeader.indexOf('\"',realmStart),",
                        "    realm = authenticateHeader.slice(realmStart,realmEnd),",
                        "    nonceStart = authenticateHeader.indexOf('\"',authenticateHeader.indexOf(\"nonce\")) + 1,",
                        "    nonceEnd = authenticateHeader.indexOf('\"',nonceStart),",
                        "    nonce = authenticateHeader.slice(nonceStart,nonceEnd);",
                        "    ",
                        "postman.setGlobalVariable('echo_digest_realm', realm);",
                        "postman.setGlobalVariable('echo_digest_nonce', nonce);"
                    ]
                }
            }
        ],
        "request": {
            "url": "https://postman-echo.com/digest-auth",
            "method": "GET",
            "header": [],
            "body": {
                "mode": "formdata",
                "formdata": [
                    {
                        "key": "code",
                        "value": "xWnkliVQJURqB2x1",
                        "type": "text"
                    },
                    {
                        "key": "grant_type",
                        "value": "authorization_code",
                        "type": "text"
                    },
                    {
                        "key": "redirect_uri",
                        "value": "https://www.getpostman.com/oauth2/callback",
                        "type": "text"
                    },
                    {
                        "key": "client_id",
                        "value": "abc123",
                        "type": "text"
                    },
                    {
                        "key": "client_secret",
                        "value": "ssh-secret",
                        "type": "text"
                    }
                ]
            },
            "description": "Performing a simple `GET` request to this endpoint returns status code `401 Unauthorized` with `WWW-Authenticate` header containing information to successfully authenticate subsequent requests.\nThe `WWW-Authenticate` header must be processed to extract `realm` and `nonce` values to hash subsequent requests.\n\nWhen this request is executed within Postman, the script attached with this request does the hard work of extracting realm and nonce from the header and set it as [global variables](https://www.getpostman.com/docs/environments#global-variables?source=echo-collection-app-onboarding) named `echo_digest_nonce` and `echo_digest_realm`.\nThese variables are re-used in subsequent request for seamless integration of the two requests."
        },
        "response": []
    }, Request),
]


@pytest.mark.parametrize("json, cls", testdata)
def test_postman_entry_create(json, cls):
    postman_entry = PostmanEntry.create(json=json)
    assert type(postman_entry) == cls


def test_entry_repr():
    postman_entry = PostmanEntry.create(os.path.join(
        "../", "samples", "Postman Echo.postman_collection.json"))
    assert "Collection" in postman_entry.__repr__()
