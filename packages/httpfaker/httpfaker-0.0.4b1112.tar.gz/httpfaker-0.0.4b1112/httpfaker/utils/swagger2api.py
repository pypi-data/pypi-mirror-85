import requests
import json
import os
import yaml


class Swagger2Api(object):
    """
    接口定义类
    """

    def save_file(self, filename, data, path, file_type):
        if not os.path.exists(path):
            os.mkdir(path)
        if not file_type.startswith('.'):
            file_type = '.' + file_type
        filename = filename + file_type
        with open(os.path.join(path, filename), 'w', encoding='utf-8', ) as f:
            if file_type in ('.yml', '.yaml'):
                data_str = yaml.dump(data, encoding='utf-8', allow_unicode=True,
                                     default_flow_style=False, sort_keys=False).decode()
            else:
                data_str = json.dumps(data, ensure_ascii=False, indent='  ')
            f.write(data_str)

    def __init__(self, host, url, type='.yml', api_path='apis'):
        interface = Interface(url, host)
        for path_info in interface.itfs_path:
            for method in interface.itfs_path[path_info]:
                file_name = path_info
                if path_info.startswith('/'):
                    file_name = path_info[1:]
                self.save_file(
                    file_name.replace("/", '_').replace("{", "").replace("}", "") + "_{}".format(method.upper()),
                    interface.format_itfs(path_info, method), api_path, type)
        print('转换完成，文件所在目录： {}'.format(os.path.abspath(api_path)))


class Interface(object):
    def __init__(self, url, host=None):
        if not url.startswith('http') and host.startswith("http"):
            interface_url = host + url
        elif url.startswith("http"):
            interface_url = url
        else:
            raise ValueError("请求地址必须以http或https开头")
        session = requests.Session()
        itfs = session.get(interface_url).text
        try:
            itfs = json.loads(itfs.replace("'", "\""))
        except json.decoder.JSONDecodeError:
            raise ValueError('swagger接口数据解析失败，请检查地址是否正确。另外，swagger返回的接口地址必须为json格式。')
        self.itfs_head = itfs['info']
        self.itfs_path = itfs['paths']
        self.definitions = itfs['definitions']

    def _resolve(self, interface_info, url, method):
        """
        swagger接口解析
        :param interface_info:
        :param url:
        :param method:
        :return:
        """

        content_type = interface_info['consumes'][0] if 'consumes' in interface_info else None
        parameters = interface_info["parameters"] if 'parameters' in interface_info else {}
        params, data, json = self.parameters_resolve(parameters)
        responses = self.response_resolve(interface_info['responses'])

        model = {
            'import': [],
            'env': {},
            'request': {
                "description": interface_info['summary'] if "summary" in interface_info else "",
                "path": url.replace("{", "<").replace("}", ">"),
                "method": [method.upper()],
                "args": params if params else None,
                "data": data if data else None,
                "json": json if json else None,
                "files": None,
            },
            "logic": {},
            "response": {
                'headers': {
                    'content-type': content_type
                },
                'body': responses,
                'status_code': 200
            }
        }
        return model

    def response_resolve(self, responses: dict):
        for key, value in responses.items():
            if value.get("schema") and "$ref" in value.get("schema"):
                _schema = self.ref_anaysis(value['schema']['$ref'].split("/")[-1])
                return _schema

    def parameters_resolve(self, parameters):
        params = {}
        data = {}
        json = {}
        _in = None
        for parameter in parameters:
            if 'in' in parameter:
                _in = parameter['in']
                if _in == "body":
                    _schema = parameter['schema']
                    if "$ref" in _schema:
                        ref = _schema["$ref"].split("/")[-1]
                        datas = self.ref_anaysis(ref)
                        json = datas
                    elif "type" in _schema:
                        json[parameter['name']] = None
                elif _in == "query":
                    params[parameter['name']] = None
                elif _in == "formData":
                    data[parameter['name']] = None
                elif _in == "path":
                    # print("请将URL中{}包裹的参数格式化后再请求")
                    pass
        return params, data, json

    def ref_anaysis(self, ref):
        """
        实体信息解析
        :param ref:
        :return:
        """
        definition = self.definitions[ref]
        datas = {}
        if 'properties' in definition:
            for field in definition['properties']:
                value = definition['properties'][field]
                if 'example' in value:
                    datas[field] = value['example']
                elif value.get("type") == 'array':
                    _schema = value['items']
                    if "$ref" in _schema:
                        ref = _schema["$ref"].split("/")[-1]
                        datas[field] = self.ref_anaysis(ref)
        return datas

    def format_itfs(self, url, method=None):
        """
        从接口文档实时获取接口信息，解决开发代码变动需手动维护测试代码的问题
        使用方法：
            1. 使用url和method可以唯一确定一个接口，此时返回dict类型数据
            2. 只传url时返回此url包含所有方法的list
            3. 传入url不存在时返回None
        :param url: 接口地址，与接口文档一致
        :param method: 请求方法
        :return: list / dict / None
        """
        if url not in self.itfs_path:
            raise Exception("未找到指定url:\"{}\"接口，请检查url是否正确".format(url))
        info = self.itfs_path[url]
        if method:
            inter_info = info[method]
            return self._resolve(inter_info, url, method)

        results = []
        for inter in info:
            results.append(self._resolve(inter, url, method))
        return results





if __name__ == '__main__':
    main()
