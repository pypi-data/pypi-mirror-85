import logging

logger = logging.getLogger('ModuleReqMiddleware.request')


class ReqMiddleware:
    def __init__(self, settings, *args, **kwargs):
        super(ReqMiddleware, self).__init__(*args, **kwargs)
        self._settings = settings
        self.logger = logger

    @staticmethod
    def transform_headers(headers):
        new_headers = {
            x.decode(): ','.join(map(lambda y: y.decode(), y))
            for x, y in headers.items()
        }
        return new_headers

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)
