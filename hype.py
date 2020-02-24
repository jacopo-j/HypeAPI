#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import Banking, AuthenticationError
from uuid import uuid4
import json
import requests


class Hype(Banking):

    ENROLL_URL = "https://api.hype.it/v2/auth/hypeconnector.aspx"
    APP_VERSION = "5.1.6"
    DEVICE_ID = str(uuid4()).replace("-", "") + "hype"
    DEVICE_INFO = json.dumps({
        "jailbreak": "false",
        "osversion": "13.3.1",
        "model": "iPhone11,2"
    })

    def __init__(self):
        self._username = None
        self.newids = None
        super().__init__()

    def login(self, username, password):
        enroll1 = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "codiceinternet": username,
                "deviceid": self.DEVICE_ID,
                "function": "FREE/LOGINFIRSTSTEP.SPR",
                "pin": password,
                "platform": "IPHONE"
            },
            timeout=5
        )
        try:
            if enroll1.json()["Check"] != "OK":
                raise AuthenticationError("Login failed")
        except json.decoder.JSONDecodeError:
            raise AuthenticationError("Failed to parse response for login request")
        except KeyError:
            raise AuthenticationError("Missing data in response for login request")
        enroll2 = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "deviceid": self.DEVICE_ID,
                "function": "INFO/ENROLLBIO.SPR",
                "platform": "IPHONE"
            },
            timeout=5
        )
        try:
            if enroll2.json()["ErrorMessage"] != "":
                raise AuthenticationError("Server returned error: " + enroll2.json()["ErrorMessage"])
        except json.decoder.JSONDecodeError:
            raise AuthenticationError("Failed to parse response for bioToken request")
        except KeyError:
            raise AuthenticationError("Missing data in response for bioToken request")
        self._username = username

    def otp2fa(self, code):
        if self._username is None:
            raise Exception("Please login() before verifying OTP code")
        otp = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "codiceinternet": self._username,
                "deviceid": self.DEVICE_ID,
                "function": "FREE/LOGINSECONDSTEP.SPR",
                "pwd": str(code),
                "platform": "IPHONE"
            },
            timeout=5
        )
        try:
            if otp.json()["Check"] != "OK":
                raise AuthenticationError("OTP verification failed")
            self.token = self._session.cookies.get_dict()["token"]
            self.newids = self._session.cookies.get_dict()["newids"]
            self._session = requests.Session()
            self._session.headers.update({
                "hype_token": self.token,
                "newids": self.newids,
                "App-Version": self.APP_VERSION
            })
        except json.decoder.JSONDecodeError:
            raise AuthenticationError("Failed to parse response for OTP verification request")
        except KeyError:
            raise AuthenticationError("Missing data in response for OTP verification request")

    def test(self):
        print(self._session.get("https://api.hype.it/v1/rest/u/profile").text)
