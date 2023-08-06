import requests
import os
from httpfaker.common.logger import log
from httpfaker.common.setting import get_yaml
import re

class Request:
    def __init__(self, base_url='http://127.0.0.1:9001', ):
        self.base_url = base_url
        self.session = requests.Session()
        self.response = None
        self.request_info = None

    @staticmethod
    def _find_api(path, topdown=False):
        api_files = []
        for root, dirs, files in os.walk(path, topdown):
            for file in files:
                if os.path.splitext(file)[-1] in ('.yml', '.yaml', '.json'):
                    api_files.append(os.path.join(root, file))
        if not api_files:
            log.w('未找到模板文件，请确认模板文件存在于当前目录下apis目录；或者使用--api_path来指定api模板文件所在目录')
        return api_files

    def send(self, data):
        request_data = data.get('request', {})
        path = request_data.get('path')
        self.request_info = {
            'data': request_data.get('data'),
            'json': request_data.get('json'),
            'params': request_data.get('args'),
            'files': request_data.get('files'),
            'url': self.base_url + path,
            'method': request_data.get('method')[0] if isinstance(request_data.get('method'), list) else request_data.get('method'),
            'headers': request_data.get('headers')
        }
        try:
            self.response = self.session.request(**self.request_info)
            print(self.response.text)
        except Exception as e:
            log.e(e)



    def start_test(self, path='apis'):
        api_files = self._find_api(path=path)
        for f in api_files:
            data = get_yaml(f)
            self.send(data)


if __name__ == '__main__':
    rq = Request('http://127.0.0.1:9001')
    rq.start_test(path='apis')