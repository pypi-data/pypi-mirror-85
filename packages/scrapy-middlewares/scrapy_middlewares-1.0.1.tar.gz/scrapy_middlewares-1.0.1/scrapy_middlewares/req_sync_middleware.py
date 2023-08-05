import httpx
import ujson
import requests
from .req_settings import *
from scrapy.http import HtmlResponse
from .req_middleware import ReqMiddleware
from .scrapy_requests import ModuleRequest


class ModuleReqMiddleware(ReqMiddleware):
    def __init__(self, *args, **kwargs):
        super(ModuleReqMiddleware, self).__init__(*args, **kwargs)

    def process_request(self, request, spider):
        _module_name = request.module_name
        if not isinstance(request, ModuleRequest) or not _module_name:
            return None

        if _module_name not in MODULE_NAME_LIST:
            self.logger.error(f'modul_name: {_module_name}, not in {MODULE_NAME_LIST}, Please check your modul_name')
            return None

        _meta_proxy = request.meta.get('proxy')
        _proxy = {
            'http': _meta_proxy,
            'https': _meta_proxy
        }
        _headers = self.transform_headers(request.headers)
        _data = ujson.loads(request.body.decode()) if request.body else ''
        _timeout = spider.settings.getint('DOWNLOAD_TIMEOUT') or self._settings.getint('DOWNLOAD_TIMEOUT', 60)

        if _module_name == REQUESTS:
            response = requests.request(request.method, request.url, headers=_headers, data=_data, proxies=_proxy, timeout=_timeout)
            _url = response.url

        elif _module_name == HTTPX:
            with httpx.Client(proxies=_proxy) as _client:
                response = _client.request(request.method, request.url, headers=_headers, data=_data, timeout=_timeout)
                _url = str(response.url)

        response = HtmlResponse(
            _url,
            status=response.status_code,
            body=response.content,
            encoding='utf-8',
            request=request
        )
        return response
