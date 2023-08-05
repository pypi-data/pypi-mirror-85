import copy
from scrapy import Request
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class ModuleRequest(Request):

    def __init__(self, module_name=None, *args, **kwargs):
        self.module_name = module_name
        super().__init__(*args, **kwargs)
