# -*- coding: utf-8 -*-
"""
:copyright: (c) 2020 by Greg Dubicki (c) 2019 by better-requests (c) 2012 by Kenneth Reitz.
:license: Apache2, see LICENSE for more details.
"""

from requests import Session as UpstreamSession
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from requests.compat import Callable


# noinspection PyUnusedLocal
from requests_extra.utils import default_headers_with_brotli


def _raise_for_status(res, *args, **kwargs):
    res.raise_for_status()


class Session(UpstreamSession):

    default_timeout = 10
    auto_raise_for_status = True

    def __init__(self):
        """A Requests session.

        + retries
        """

        super(Session, self).__init__()

        retries: Retry = Retry(
            total=2,  # 3 requests in total
            backoff_factor=1,  # retry after 2, 4 secs
            status_forcelist=[
                500,
                502,
                503,
                504,
                408,
                429,
            ],  # on server errors + timeout + rate limit exceeded
            method_whitelist=[
                "HEAD",
                "GET",
                "PUT",
                "DELETE",
                "OPTIONS",
                "TRACE",
            ],
        )
        self.mount("http://", HTTPAdapter(max_retries=retries))
        self.mount("https://", HTTPAdapter(max_retries=retries))

        self.default_timeout = Session.default_timeout
        self.auto_raise_for_status = Session.auto_raise_for_status

        self.headers = default_headers_with_brotli()

    def prepare_request(self, request):
        """A Requests prepared request.

        + auto raise for status
        """

        p = super(Session, self).prepare_request(request)

        # Auto raise_for_status
        if self.auto_raise_for_status:
            if p.hooks is None:
                p.hooks = {}

            hook = [_raise_for_status]

            old_hook = p.hooks.get("response")
            if old_hook is None:
                pass
            elif hasattr(old_hook, "__iter__"):
                hook.extend(old_hook)
            elif isinstance(old_hook, Callable):
                hook.append(old_hook)

            p.hooks["response"] = hook

        return p

    def send(self, request, *args, **kwargs):
        """Send a given PreparedRequest

        + timeout
        :rtype: requests.Response
        """

        # Set default timeout, None -> default, zero -> None
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.default_timeout
        elif timeout == 0:
            kwargs["timeout"] = None

        # noinspection PyArgumentList
        return super(Session, self).send(request, *args, **kwargs)
