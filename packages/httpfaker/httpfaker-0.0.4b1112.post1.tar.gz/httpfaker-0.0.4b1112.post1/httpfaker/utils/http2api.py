from flask import Flask
from flask import request
from httpfaker.utils.constant import HTTP_TEMPLATE
from httpfaker.utils.constant import __version__
import sys
import json
import os
import argparse
import jinja2
import yaml

app = Flask(__name__)

DEFAULT_BODY = 'null'
DEFAULT_STATUS = 200
DEFAULT_PATH = 'apis'
HIDE_DATA = False
FORMAT = 'yaml'


def save_file(request, data, format):
    if not os.path.exists(DEFAULT_PATH):
        os.mkdir(DEFAULT_PATH)
    filename = '_'.join([x for x in request.path.split('/') if x]) + '_{}'.format(request.method) + format
    with open(os.path.join(DEFAULT_PATH, filename), 'w', encoding='utf-8', ) as f:
        f.write(data)


@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def save_params(path):
    def render(**kwargs):
        tp = jinja2.Template(HTTP_TEMPLATE)
        data = tp.render(kwargs)
        dict_data = yaml.load(data, Loader=yaml.FullLoader)
        if HIDE_DATA:
            dict_data['request'].pop('data')
            dict_data['request'].pop('args')
        if FORMAT == 'json':
            data_str = json.dumps(dict_data, ensure_ascii=False, indent='  ')
            save_file(request, data_str, '.json')
        else:
            data_str = yaml.dump(dict_data, encoding='utf-8', allow_unicode=True,
                                 default_flow_style=False, sort_keys=False).decode()
            save_file(request, data_str, '.yml')

        return dict_data

    data = request.json if request.content_type == 'application/json' else 'null'
    args = request.args.to_dict()
    return render(CONTENT_TYPE=request.content_type, PATH=request.path, METHOD=request.method,
                  RESPONSE_BODY=DEFAULT_BODY, RESPONSE_STATUS=DEFAULT_STATUS, DATA=data, ARGS=args)


def start_http2api(**kwargs):
    global DEFAULT_BODY, DEFAULT_STATUS, DEFAULT_PATH, HIDE_DATA, FORMAT
    default_body = kwargs.get('default_body')
    if default_body:
        if os.path.isfile(default_body):
            with open(default_body, encoding='utf-8') as f:
                try:
                    _body = f.read()
                    DEFAULT_BODY = json.loads(_body)
                except json.JSONDecodeError:
                    DEFAULT_BODY = yaml.load(_body, Loader=yaml.FullLoader)
                except Exception:
                    DEFAULT_BODY = _body

        else:
            raise ValueError('“default-body” must be the file path of a json or yaml format file')
    default_status = kwargs.get('default_status')
    if default_status:
        DEFAULT_STATUS = default_status
    DEFAULT_PATH = kwargs.get('path', 'apis')
    HIDE_DATA = kwargs.get('hide_data', False)
    FORMAT = kwargs.get('out_format', 'yaml')
    app.run(host=kwargs.get('listen'), port=kwargs.get('port'))

