# scrapy-middlewares
scrapy middlewares

### Installation 安装

```sh
pip install scrapy_middlewares requests httpx aiohttp
```

### Usage example 使用示例
```python
'DOWNLOADER_MIDDLEWARES': {
    'scrapy_middlewares.req_sync_middleware.ModuleReqMiddleware': 601
},

# module_name:
# 	'httpx', 'requests'

yield ModuleRequest(url=url, callback=self.parse, module_name='requests')
```

```python
'DOWNLOADER_MIDDLEWARES': {
    'scrapy_middlewares.req_async_middleware.ModuleAsyncReqMiddleware': 601
},

# module_name:
# 	'httpx_async', 'aiohttp'

yield ModuleRequest(url=url, callback=self.parse, module_name='httpx_async')
```

