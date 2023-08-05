# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union, Dict
from requests import Response
import random, copy

# Pip
from kcu.request import request, RequestMethod

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Request ------------------------------------------------------------ #

class Request:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        default_headers: Optional[Dict[str, any]] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        user_agent: Optional[str] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        keep_cookies: bool = True,
        debug: bool = False
    ):
        self.user_agent = user_agent
        self.cookies = None

        self.max_request_try_count = max_request_try_count
        self.sleep_s_between_failed_requests = sleep_s_between_failed_requests

        self.keep_cookies = keep_cookies
        self.debug = debug

        if type(proxy) == list:
            proxy = random.choice(proxy) if len(proxy) > 0 else None

        self.proxy = proxy
        self.default_headers = {}

        if default_headers:
            for k, v in default_headers.items():
                if not v:
                    continue

                if type(v) != str:
                    v = str(v)

                self.default_headers[k] = v

        if extra_headers:
            for k, v in extra_headers.items():
                if not v:
                    continue

                if type(v) != str:
                    v = str(v)

                self.default_headers[k] = v

    def get(self, url: str, extra_headers: Optional[Dict[str, any]] = None) -> Optional[Response]:
        return self.__request(url, RequestMethod.GET, extra_headers)
    
    def post(self, url: str, body: dict, extra_headers: Optional[Dict[str, any]] = None) -> Optional[Response]:
        return self.__request(url, RequestMethod.POST, extra_headers, body)

    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __request(
        self,
        url: str,
        method: RequestMethod,
        extra_headers: Optional[Dict[str, any]] = None,
        body: Optional[dict] = None
    ) -> Optional[Response]:
        headers = copy.deepcopy(self.default_headers)

        if 'Host' not in headers or not headers['Host']:
            host = self.__get_host(url)

            if host:
                headers['Host'] = host

        if extra_headers:
            for k, v in extra_headers.items():
                if not v:
                    continue

                if type(v) != str:
                    v = str(v)

                extra_headers[k] = v

        if self.cookies:
            headers['Cookie'] = self.cookies

        res = request(
            url,
            method,
            headers=headers,
            user_agent=self.user_agent,
            data=body,
            debug=self.debug,
            max_request_try_count=self.max_request_try_count,
            sleep_time=self.sleep_s_between_failed_requests,
            proxy=self.proxy
        )

        if self.keep_cookies and res and res.cookies:
            cookie_strs = []

            for k, v in res.cookies.get_dict().items():
                cookie_strs.append(k+'='+v)

            self.cookies = '; '.join(cookie_strs)

        return res

    def __get_host(self, url: str) -> Optional[str]:
        try:
            return url.split('://')[1].split('/')[0]
        except:
            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #