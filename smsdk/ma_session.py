from typing import List
import json
import requests

import numpy as np

from requests.structures import CaseInsensitiveDict
from requests.sessions import Session

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from smsdk import config

RESOURCE_CONFIG = json.loads(pkg_resources.read_text(config, "message_config.json"))

SM_AUTH_HEADER_SECRET_ID = RESOURCE_CONFIG["auth_header-api-secret"]
SM_AUTH_HEADER_SECRET_ID_OLD = RESOURCE_CONFIG["auth_header-api-secret_old"]
SM_AUTH_HEADER_KEY_ID = RESOURCE_CONFIG["auth_header-api-key"]

import logging
log = logging.getLogger(__name__)

class MaSession:
    def __init__(self):
        self.requests = requests
        self.session = Session()

    def _get_records(
        self,
        endpoint,
        method="get",
        _limit=np.Inf,
        _offset=0,
        **url_params
    ):
        """
        Function to get api call and fetch data from MA APIs
        :param endpoint: complete url endpoint
        :param method: Reqested method. Default = get
        :param enable_pagination: if pagination is enabled then
        the records are fetched with limit offset pagination
        :param limit: Limit the number of records for pagination
        :param offset: pagination offset
        :param url_params: dict of params for API ex filtering, columns etc
        :return: List of records
        """
        max_page_size = 5000
        
        records: List = []
        while True:
            try:
                remaining_limit = _limit - len(records)
                this_loop_limit = min(remaining_limit, max_page_size)

                # If we exactly hit our desired number of records -- limit is 0 -- then can stop
                if this_loop_limit == 0:
                    return records

                url_params["_offset"] = _offset
                url_params["_limit"] = this_loop_limit

                log.info(f'Pulling up to {this_loop_limit} records')
                
                response = getattr(self.session, method.lower())(
                    endpoint, params=url_params
                )

                if response.text:
                    if "error" in response.text:
                        raise ValueError("Error - {}".format(response.text))
                    data = response.json()
                else:
                    return []
                       
                records.extend(data)
                if len(data) < this_loop_limit:
                    # Cursor exhausted, so just return
                    return records
                _offset += this_loop_limit
                
            except:
                import traceback

                print(traceback.print_exc())
                return records
        return records

    def get_json_headers(self):
        """
        Headers for json requests
        """
        return CaseInsensitiveDict(
            {
                "Accept-Encoding": "*/*",
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )

    def modify_header_style(self, url, headers):
        """
        Modify request header keys
        V0 style- X-SM-API-Key, X-SM-API-Key-Id
        V1 style- X-SM-API-Secret, X-SM-API-Key-Id
        """
        if headers == None or {}:
            return self.get_json_headers()

        if "v1" not in url and SM_AUTH_HEADER_SECRET_ID in headers:
            headers[SM_AUTH_HEADER_SECRET_ID_OLD] = headers.pop(
                SM_AUTH_HEADER_SECRET_ID
            )
        elif "v1" in url and SM_AUTH_HEADER_SECRET_ID_OLD in headers:
            headers[SM_AUTH_HEADER_SECRET_ID] = headers.pop(
                SM_AUTH_HEADER_SECRET_ID_OLD
            )
        return headers
