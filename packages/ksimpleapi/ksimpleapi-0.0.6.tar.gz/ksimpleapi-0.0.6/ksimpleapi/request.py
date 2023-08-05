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
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        keep_cookies: bool = True,
        debug: bool = False
    ):
        self.cookies = None

        self.max_request_try_count = max_request_try_count
        self.sleep_s_between_failed_requests = sleep_s_between_failed_requests

        self.keep_cookies = keep_cookies
        self.debug = debug

        if type(user_agent) == list:
            user_agent = random.choice(user_agent) if len(user_agent) > 0 else None

        self.user_agent = user_agent

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

    def get(
        self,
        url: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return self.__request(
            url,
            RequestMethod.GET,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )
    
    def post(
        self,
        url: str,
        body: dict,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return self.__request(
            url,
            RequestMethod.POST,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            body=body,
            debug=debug
        )

    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __request(
        self,
        url: str,
        method: RequestMethod,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        body: Optional[dict] = None,
        debug: Optional[bool] = None
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

        if use_cookies and self.cookies:
            headers['Cookie'] = self.cookies

        if type(proxy) == list:
            proxy = random.choice(proxy) if len(proxy) > 0 else None

        if type(user_agent) == list:
            user_agent = random.choice(user_agent) if len(user_agent) > 0 else None

        res = request(
            url,
            method,
            headers=headers,
            user_agent=user_agent or self.user_agent,
            data=body,
            debug=debug if debug is not None else self.debug,
            max_request_try_count=max_request_try_count or self.max_request_try_count,
            sleep_time=sleep_s_between_failed_requests or self.sleep_s_between_failed_requests,
            proxy=proxy or self.proxy
        )

        if use_cookies and self.keep_cookies and res and res.cookies:
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