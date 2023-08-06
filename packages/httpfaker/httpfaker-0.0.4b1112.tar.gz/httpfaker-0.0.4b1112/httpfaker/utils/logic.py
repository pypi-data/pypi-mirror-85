from httpfaker.utils.resolve import ResolveBase
import re


class ResolveYaml(ResolveBase):
    def __init__(self, meta, faker=None, request=None):
        super().__init__(faker)
        self.meta_data = self.check_api_file(meta)
        self.request_data = {}
        self.request = {}
        self.logic = {}
        self.response = {}
        self.key = None
        self.import_package()
        self.resolve_env()
        self.resolve_request(request)

    def import_package(self):
        self.env_data.update(self._import_package(packages=self.meta_data.get('import')))

    def resolve_env(self):
        """
        环境变量预处理
        :param condition:
        :return:
        """
        env = self.meta_data.get('env')
        if not env:
            return
        self._field_handle(env_key='env', **env)

    def resolve_request(self, request):
        self.request_data = self.dict_resolve(self.meta_data.get('request'))
        method = self.request_data['method']
        self.key = '_'.join([x for x in self.request_data['path'].split("/") if x]) + '_' + '_'.join(method)
        self.request = request
        self.env_data['request'] = request

    def resolve_logic(self):
        logic = self.meta_data.get('logic')
        _logic = {}
        self._field_handle(env_key='logic', **logic)

    def resolve_response(self):
        # response = self.dict_resolve(self.meta_data.get('response'))
        response = self.meta_data.get('response')
        _response = {}
        self.response = self._field_handle(env_key='response', **response)


    def start(self):
        self.resolve_logic()
        self.resolve_response()
        return self.response
