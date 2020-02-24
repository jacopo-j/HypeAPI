#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import html
from utils import parse_form
from common import Banking, AuthenticationError
import json
import requests


class TimPay(Banking):

    ENROLL_URL = "https://www.hype.it/api/rest/FREE/timenrollment"

    def login(self, misdn, username, password):
        enroll = self._session.get(
            self.ENROLL_URL,
            params={"misdn": str(misdn), "status": "REGISTERED"},
            timeout=5
        )
        login_form = parse_form(
            enroll.text,
            username=username,
            password=password,
            action="login"
        )
        auth = self._session.post(
            login_form["url"],
            data=login_form["post_data"],
            timeout=5
        )
        try:
            auth_form = parse_form(auth.text)
        except IndexError:
            raise AuthenticationError("Login failed")
        res = self._session.post(
            auth_form["url"],
            data=auth_form["post_data"],
            timeout=5
        )
        try:
            self.token = res.json()["data"]["c_oauth_token"]
            self._session = requests.Session()
            self._session.headers.update({
                "hype_token": self.token,
                "Auth-Token": self.token,
                "Auth-Schema": "OAUTH-TIM"
            })
        except json.decoder.JSONDecodeError:
            raise AuthenticationError("Failed to parse response for OAuth token request")
        except KeyError:
            raise AuthenticationError("Failed to retrieve OAuth token")

    def test(self):
        print(self._session.get("https://api.platfr.io/api/hype/v1/user/card-info").text)
        
