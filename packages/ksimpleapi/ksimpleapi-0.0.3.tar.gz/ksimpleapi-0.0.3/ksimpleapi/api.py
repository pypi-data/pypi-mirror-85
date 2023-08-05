# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from abc import ABC, abstractmethod
from typing import Optional, List, Union, Dict
from requests import Response

# Local
from .request import Request

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------------- class: Api -------------------------------------------------------------- #

class Api:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        keep_cookies: bool = True,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        debug: bool = False
    ):
        """init function

        Args:
            user_agent (Optional[Union[str, List[str]]], optional): User agent(s) to use for requests. If list is provided, one will be chosen randomly. Defaults to None.
            proxy (Optional[Union[str, List[str]]], optional): Proxy/Proxies to use for requests. If list is provided, one will be chosen randomly. Defaults to None.
            keep_cookies (bool, optional): Keep cookies for requests and reuse them at next one. Defaults to True.
            max_request_try_count (int, optional): How many times does a request can be tried (if fails). Defaults to 1.
            sleep_s_between_failed_requests (Optional[float], optional): How much to wait between requests when retrying. Defaults to 0.5.
            debug (bool, optional): Show debug logs. Defaults to False.
        """
        self._request = Request(
            user_agent=user_agent,
            proxy=proxy,
            keep_cookies=keep_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            default_headers=self.default_headers,
            extra_headers=self.extra_headers,
            debug=debug
        )


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def default_headers(self) -> Optional[Dict[str, any]]:
        """ Default headers to use for every request.
            Overwrite this value as needed.
        """

        return {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }

    @property
    def extra_headers(self) -> Optional[Dict[str, any]]:
        """ Every entry from this adds/overwrites an entry from 'default_headers'
            Overwrite this value as needed.
        """

        return None

    def _get(self, url: str, extra_headers: Optional[Dict[str, any]] = None) -> Optional[Response]:
        return self._request.get(url, extra_headers)

    def _post(self, url: str, body: dict, extra_headers: Optional[Dict[str, any]] = None) -> Optional[Response]:
        return self._request.post(url, body, extra_headers)


# ---------------------------------------------------------------------------------------------------------------------------------------- #