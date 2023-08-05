import sys
import ujson
import httpx
import aiohttp
import asyncio
import twisted
from .req_settings import *
from scrapy.http import HtmlResponse
from .scrapy_requests import ModuleRequest
from twisted.internet.defer import Deferred
from .req_sync_middleware import ReqMiddleware

from twisted.internet.asyncioreactor import AsyncioSelectorReactor

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

reactor = AsyncioSelectorReactor(asyncio.get_event_loop())

twisted.internet.reactor = reactor
sys.modules['twisted.internet.reactor'] = reactor


def as_deferred(f):
    return Deferred.fromFuture(asyncio.ensure_future(f))


class ModuleAsyncReqMiddleware(ReqMiddleware):
    def __init__(self, *args, **kwargs):
        super(ModuleAsyncReqMiddleware, self).__init__(*args, **kwargs)

    async def _process_request(self, request, spider):
        _module_name = request.module_name
        if not isinstance(request, ModuleRequest) or not _module_name:
            return None

        if _module_name not in MODULE_NAME_LIST:
            self.logger.error(f'modul_name: {_module_name}, not in {MODULE_NAME_LIST}, Please check your modul_name')
            return None

        _meta_proxy = request.meta.get('proxy')
        _proxy = _meta_proxy
        _headers = self.transform_headers(request.headers)
        _data = ujson.loads(request.body.decode()) if request.body else ''
        _timeout = spider.settings.getint('DOWNLOAD_TIMEOUT') or self._settings.getint('DOWNLOAD_TIMEOUT', 60)

        if _module_name == HTTPX_ASYNC:
            async with httpx.AsyncClient(proxies=_proxy) as _client:
                response = await _client.request(request.method, request.url, headers=_headers, data=_data, timeout=_timeout)
                _url = str(response.url)
                _body = response.content
                _status = response.status_code

        elif _module_name == AIOHTTP:
            async with aiohttp.ClientSession() as _session:
                async with _session.request(request.method, request.url, headers=_headers, data=_data, timeout=_timeout, proxy=_proxy) as response:
                    _body = await response.content.read()
                    _url = str(response.url)
                    _status = response.status

        response = HtmlResponse(
            _url,
            status=_status,
            headers=response.headers,
            body=_body,
            encoding='utf-8',
            request=request
        )
        return response

    def process_request(self, request, spider):
        return as_deferred(self._process_request(request, spider))

    async def _spider_closed(self):
        pass

    def spider_closed(self):
        return as_deferred(self._spider_closed())
