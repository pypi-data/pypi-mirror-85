__version__ = '0.0.4-beta1112'
__author__ = 'Long Guo'
__author_email__ = '565169745@qq.com'
__url__ = 'https://gitee.com/guojongg/http-faker'
__description__ = '一个无需编写代码的后台服务（mock）'


HTTP_TEMPLATE = '''# Request: 请求描述；提供与描述一致的接口服务
# Logic: 请求的处理逻辑描述；描述请求过来后如何处理；
# Response: 请求返回的数据生成方式描述；

# 下面的配置描述了，当用户请求登录接口的场景。
# 用户使用用户名和密码登录，传过来后在Logic块中，我们先验证账号是否存在于数据库中。存在的话我们往redis生成token。返回信息按照token生成与否来自适应返回。
# （使用此方式基本可以实现具体的业务场景）

import: []
env: {}

request:
  path: {{ PATH }}
  method: [{{ METHOD }}]
  data: {{ DATA }}
  args: {{ ARGS }}

# 数据处理逻辑处理的块，可以对request请求进行一系列逻辑处理，从而处理真实的业务请求
logic: {} 

response:  # Response属性描述。会按照此描述给客户端返回数据。
  headers:
    Content-Type: {{ CONTENT_TYPE }}
  body: {{ RESPONSE_BODY }}
  status_code: {{ RESPONSE_STATUS }}
'''
