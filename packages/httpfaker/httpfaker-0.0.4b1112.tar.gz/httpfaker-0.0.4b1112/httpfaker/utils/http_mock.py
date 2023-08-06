from flask import Flask
from flask import request
import os
from httpfaker.utils.logic import ResolveYaml
from flask import Response
import json
from httpfaker.utils.generator import MGenerator
from httpfaker.utils.faker_date_time import Provider as DateTimeProvider
from httpfaker.utils.faker_tool import Provider as ToolProvider
from faker import Faker
import importlib
import sys
from httpfaker.common.error import *
from httpfaker.common.logger import log
from httpfaker.utils.init_project import scaffold

faker = Faker(locale='zh_CN', generator=MGenerator(locale='zh_CN'))


def import_module(module_path='script'):
    if not os.path.exists(module_path):
        return
    pys = [x for x in list(os.walk(module_path))[0][-1] if x.endswith(".py")]
    modules = []
    for py in pys:
        if module_path.endswith('/'):
            module_path = module_path[:-1]
        module = importlib.import_module('{}.{}'.format(module_path.replace('/', '.'), py.split(".")[0]))
        for class_name in dir(module):
            provider = getattr(module, class_name)
            if isinstance(provider, type):
                modules.append(provider)
    return modules


class HttpMock(Flask):
    def __init__(self, target='apis', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function_object = self._find_api(target)

    def callback(self, *args, **kwargs):
        """
        flask接口注册的回调方法
        :param args:
        :param kwargs:
        :return:
        """
        path = request.path
        if request.view_args:
            for key, value in request.view_args.items():
                path = request.path.replace(value, "<{}>".format(key))
        func = self.function_object['_'.join([x for x in path.split('/') if x]) + '_{}'.format(request.method)]
        response_data = func.start()
        return Response(
            response=json.dumps(response_data['body']),
            status=response_data['status_code'],
            headers=response_data['headers']
        )

    def _route(self, rules: list):
        """
        接口注册
        :param rules: 指定接口地址和请求方法注册接口
        :return:
        """
        for rule in rules:
            for key, value in rule.items():
                self.route(key, methods=value)(self.callback)

    @staticmethod
    def _find_api(path, topdown=False):
        api_files = []
        for root, dirs, files in os.walk(path, topdown):
            for file in files:
                if os.path.splitext(file)[-1] in ('.yml', '.yaml', '.json'):
                    api_files.append(os.path.join(root, file))
        if not api_files:
            log.w('未找到模板文件，请确认模板文件存在于当前目录下apis目录；或者使用--api_path来指定api模板文件所在目录')
        obj = {}
        for f in api_files:

            try:
                resolve_obj = ResolveYaml(meta=f, faker=faker, request=request)
                obj[resolve_obj.key] = resolve_obj
            except ApiFileError as e:
                log.e(e)
        return obj


def start_server(type=None, api_path='apis', listen='0.0.0.0', port=9001, script_path='script', **kwargs):
    if type == 'init':
        scaffold(project_name=kwargs.get('project_name', 'httpfaker-project'), path=kwargs.get('path', '.'))
        return
    cur_dir = os.path.abspath(os.curdir)
    sys.path.append(cur_dir)
    sys.path.append(script_path)
    faker.add_provider(DateTimeProvider, offset=0)
    faker.add_provider(ToolProvider, )
    modules = import_module(script_path)
    if modules:
        for module in modules:
            faker.add_provider(module)
    http = HttpMock(import_name=__name__, target=api_path)
    rules = []
    for h in http.function_object.values():
        log.i('接口注册： ' + str(h.request_data))
        rules.append({h.request_data['path']: h.request_data['method']})
    http._route(rules)
    http.run(host=listen, port=port)


if __name__ == '__main__':
    start_server()
