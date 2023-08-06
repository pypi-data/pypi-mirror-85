from httpfaker import start_server
import sys
import argparse
from httpfaker.utils.constant import __version__
from httpfaker import start_http2api
from httpfaker import Swagger2Api
from httpfaker.utils.init_project import scaffold


def parse_args_httpfaker():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='启动mock服务')
    parser.add_argument('type', nargs='?', action='store', default='start-server',
                        help='操作类型； start-server: 启动httpfaker服务； init： 创建httpfaker项目目录')
    parser.add_argument('--api-path', nargs='?', action='store', default='apis', help='api描述文件所在路径， 默认apis')
    parser.add_argument('--project-name', nargs='?', action='store', default='httpfaker-project', help='项目名， 默认httpfaker-project')
    parser.add_argument('--script-path', nargs='?', action='store', default='script', help='自定义方法脚本所在目录, 默认script')
    parser.add_argument('--listen', nargs='?', action='store', default='0.0.0.0', help='启动服务默认监听地址，默认0.0.0.0')
    parser.add_argument('--port', nargs='?', action='store', default='9001', help='启动服务默认监听端口，默认9001')
    args = parser.parse_args()
    return args


def parse_args_http2api():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='调用接口生成mock描述文件')
    parser.add_argument('--default-body', nargs='?', action='store',
                        help='Response默认的返回体，指定后生成的Response中的body字段将按照此定义来生成。用法：指定文件路径，文件内容格式可以是json或者yaml！')
    parser.add_argument('--default-status', nargs='?', action='store', default=200,
                        help='Response中status_code返回值，默认为200')
    parser.add_argument('--path', nargs='?', action='store', default='apis', help='输出的配置文件存放路径, 默认当前目录下的apis目录')
    parser.add_argument('--hide-data', action='store_true', help='不转换Request中的请求体和请求参数数据（请求参数和请求体数据仅做参考，不参与实际逻辑）')
    parser.add_argument('--out-format', nargs='?', action='store', default='yml', help='转换的配置文件的格式；可选yml和json，默认yml格式')
    parser.add_argument('--listen', nargs='?', action='store', default='0.0.0.0', help='启动服务默认监听地址，默认0.0.0.0')
    parser.add_argument('--port', nargs='?', action='store', default='9000', help='启动服务默认监听端口，默认9000')
    args = parser.parse_args()

    return args


def parse_args_swagger2api():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='swagger转api工具, 使用方式： swagger2api --url http://127.0.0.1/v2/api-docs')
    parser.add_argument('--api-path', nargs='?', action='store', default='apis', help='生成api描述文件存放路径， 默认apis')
    parser.add_argument('--url', nargs='?', action='store', help='swagger接口地址')
    parser.add_argument('--host', nargs='?', action='store', default='http://127.0.0.1',
                        help='请求地址host，默认：http://127.0.0.1，当url参数中包含请求schema时此参数无效')
    parser.add_argument('--type', nargs='?', action='store', default='yml', help='转换api文件类型，默认为.yml， 可选json')
    args = parser.parse_args()
    if not args.url:
        print('"url" can not be empty')
        parser.print_help()
        exit()
    return args


def httpfaker():
    args = parse_args_httpfaker()
    start_server(**args.__dict__)


def http2api():
    args = parse_args_http2api()
    start_http2api(**args.__dict__)


def swagger2api():
    args = parse_args_swagger2api()
    Swagger2Api(**args.__dict__)


if __name__ == '__main__':
    # httpfaker()
    http2api()
    # swagger2api()
