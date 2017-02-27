"""Common tools
"""

from urllib.parse import urljoin

import requests


class BaseClient(object):
    """Convenience interface for any HTTP API"""

    def __init__(self, base_url, root_netloc='/'):

        self._base = urljoin(base_url, root_netloc)
        self._session = requests.Session()

    def __getattr__(self, request_method):
        """Proxy for `self.request(request_method, ...)`"""

        return lambda *args, **kwargs: self.request(request_method, *args, **kwargs)

    def request(self, method, url_path=None, **kwargs):
        """Send request using http verb `method` to a `url_path` (absolute or relative).
        All `kwargs` are passed to a requests.request method.
        Return requests.Response object.
        """

        return self._session.request(
            method,
            self._prepare_url(url_path),
            allow_redirects=False,
            **kwargs
        )

    def _prepare_url(self, url_path):
        """Prepare a valid URL from `url_path` using `self._base` as a base URL"""

        return urljoin(self._base, url_path) if url_path else self._base

    def update_base_url(self, new_base):
        """Update the base URL which is used for all requests"""

        self._base = self._prepare_url(new_base)
