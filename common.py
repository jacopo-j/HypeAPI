#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import requests


class Banking(ABC):

    def __init__(self):
        self.token = None
        self._session = requests.Session()
        super().__init__()


class AuthenticationError(Exception):
    pass
