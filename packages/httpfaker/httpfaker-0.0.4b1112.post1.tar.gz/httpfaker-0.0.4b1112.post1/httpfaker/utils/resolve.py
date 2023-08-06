from httpfaker.common.setting import get_yaml
from httpfaker.common.logger import log
import json
import jinja2
from httpfaker.common.error import *
import ast
import copy
from faker import Faker


class ResolveBase:
    def __init__(self,  faker=None):
        self.faker = faker if faker else Faker(locale='zh_CN')
        self.all_package = {}
        self.log = log
        self.env_data = {'env': {}, 'request': {}, "logic": {}, 'response': {}, 'faker': self.faker}
        self.yaml_files = []

    def dict_resolve(self, data: dict):
        """
        递归将字典的value使用模板格式化
        :param data:
        :return:
        """
        for key, value in data.items():
            if isinstance(value, dict):
                self.dict_resolve(value)
            elif isinstance(value, str):
                value = self._template_render(value)
            data[key] = value
        return data

    @staticmethod
    def _import_package(packages: list = None):
        """
        动态导包
        """
        obj_package = {}
        if isinstance(__builtins__, dict):
            obj_package.update(__builtins__)
        else:
            obj_package.update(__builtins__.__dict__)
        for i in packages:
            try:
                obj_package[i] = __import__(i)
            except ModuleNotFoundError:
                log.e('import package {} failed'.format(i))
        return obj_package

    def _field_handle(self, env_key=None, **kwargs):
        data = {}
        for key, value in copy.deepcopy(kwargs).items():
            if not isinstance(value, dict):
                _data = self.dict_resolve({key:value})
            elif 'engine' not in value:
                _data = self.dict_resolve({key: self._field_handle(**value)})
            else:
                _data = {key: self._gen_field(**self.dict_resolve(value))}
            data.update(_data)
            if env_key:
                self.env_data[env_key].update(data)
        return data

    def _gen_field(self, engine: str, rule=None):
        if isinstance(rule, str):
            rule = json.loads(self._template_render(rule))
        if rule:
            rule = self.dict_resolve(rule)
        faker = self.faker
        if not engine:
            return
        if 'faker.' not in engine:
            engine = "faker.{engine}".format(engine=engine)
        if "(" in engine and ")" in engine:
            r = eval(engine)
        else:
            if isinstance(rule, list):
                r = eval("{engine}(*{rule})".format(engine=engine, rule=rule))
            elif isinstance(rule, dict):
                r = eval("{engine}(**{rule})".format(engine=engine, rule=rule))
            elif rule is None:
                r = eval("{engine}()".format(engine=engine))
            else:
                raise Exception('rule type must be dictionary or list！')
        return r

    def _template_render(self, s, env=None):
        """
        jinja2模板渲染
        """
        source_type = type(s)
        if isinstance(s, (list, dict)):
            s = json.dumps(s).replace('\\\"', "'")
        if isinstance(s, (int, float)):
            return s
        tp = jinja2.Template(s)
        if isinstance(env, dict):
            self.all_package.update(env)
        tp.globals.update(self.all_package)
        r = tp.render(**self.env_data)
        if source_type in [list, dict]:
            r = json.loads(r)
        if isinstance(r, str):
            try:
                r = ast.literal_eval(r)
            except Exception:
                pass

        return r

    @staticmethod
    def check_api_file(f):
        data = get_yaml(f)
        if not data or not isinstance(data, dict):
            raise ApiFileError('文件内容不符合解析标准，请按照指定格式进行编写: {f}'.format(f=f))
        return data



if __name__ == '__main__':
    from httpfaker.utils.generator import MGenerator
    from httpfaker.utils.faker_date_time import Provider as DateTimeProvider
    from httpfaker.utils.faker_tool import Provider as ToolProvider

    faker = Faker(locale='zh_CN', generator=MGenerator(locale='zh_CN'))
    faker.add_provider(DateTimeProvider, offset=0)
    faker.add_provider(ToolProvider, )
    r = ResolveBase(faker=faker)

