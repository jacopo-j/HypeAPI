#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from banking import Banking
from utils import parse_form
from utils import loginrequired


class TimPay(Banking):

    ENROLL_URL = "https://www.hype.it/api/rest/FREE/timenrollment"
    PROFILE_URL = "https://api.platfr.io/api/hype/v1/user/financial-situation"
    BALANCE_URL = "https://api.platfr.io/api/hype/v1/user/financial-situation"
    CARD_URL = "https://api.platfr.io/api/hype/v1/user/card-info"

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
            raise self.AuthenticationError("Login failed")
        res = self._session.post(
            auth_form["url"],
            data=auth_form["post_data"],
            timeout=5
        )
        try:
            self.token = res.json()["data"]["c_oauth_token"]
            self._session = requests.Session()
            self._session.headers.update({
                "Auth-Token": self.token,
                "Auth-Schema": "OAUTH-TIM"
            })
        except json.decoder.JSONDecodeError:
            raise self.AuthenticationError("Failed to parse response for OAuth token request")
        except KeyError:
            raise self.AuthenticationError("Failed to retrieve OAuth token")

    def otp2fa(self, *args, **kwargs):
        """
        Two-factor authentication not required for TIM Pay.
        """
        raise NotImplementedError

    @loginrequired
    def get_profile_info(self):
        return self._api_request(method="GET", url=self.PROFILE_URL)["userSettings"]

    @loginrequired
    def get_balance(self):
        b = self._api_request(method="GET", url=self.BALANCE_URL)
        del b["userSettings"]
        return b
