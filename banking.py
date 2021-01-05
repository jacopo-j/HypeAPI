#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from utils import loginrequired
import requests
import json


class Banking(ABC):

    class AuthenticationError(Exception):
        """
        Raised when an error occurs during authentication.
        """
        pass

    class AuthenticationFailure(Exception):
        """
        Raised when an authentication error occurs during a request
        for which the user should already be authenticated.
        """
        pass

    class RequestException(Exception):
        """
        Raised when an error occurs during a request to the
        backend.
        """
        pass

    @property
    @classmethod
    @abstractmethod
    def ENROLL_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def PROFILE_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def BALANCE_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def CARD_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def MOVEMENTS_URL(cls):
        return NotImplementedError

    def __init__(self):
        self.token = None
        self._session = requests.Session()
        super().__init__()

    def _api_request(self, **kwargs):
        """
        Wrapper for requests to the backend. Checks if the request was
        successful, then returns the response data.
        """
        r = self._session.request(**kwargs)
        try:
            data = r.json()
        except json.decoder.JSONDecodeError:
            raise self.RequestException("Failed to parse response: " + r.text)
        if "responseCode" not in data:
            raise self.RequestException("Missing response code from response: " + r.text)
        if data["responseCode"] in ("401", "007"):
            raise self.AuthenticationFailure
        elif data["responseCode"] != "200":
            raise self.RequestException("Server returned response {responseCode}: {responseDescr}".format(**data))
        return data["data"]

    @abstractmethod
    def login(self, *args, **kwargs):
        pass

    @abstractmethod
    def otp2fa(self, *args, **kwargs):
        """
        OTP code verification for two-factor authentication.
        """
        pass

    @abstractmethod
    def renew(self, *args, **kwargs):
        pass

    @loginrequired
    def get_profile_info(self):
        return self._api_request(method="GET", url=self.PROFILE_URL)

    @loginrequired
    def get_balance(self):
        return self._api_request(method="GET", url=self.BALANCE_URL)

    @loginrequired
    def get_card_info(self):
        return self._api_request(method="GET", url=self.CARD_URL)

    @abstractmethod
    def get_movements(self, *args, **kwargs):
        pass
