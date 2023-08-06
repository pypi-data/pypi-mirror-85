# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_session(*, retries):
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        method_whitelist=["HEAD", "OPTIONS", "GET", "POST"],
        status_forcelist=[413, 429, 500, 503, 504],
        backoff_factor=1,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get(*args, **kwargs):
    session = get_session(retries=8)
    return session.get(*args, **kwargs)


def post(*args, **kwargs):
    session = get_session(retries=3)
    return session.post(*args, **kwargs)
