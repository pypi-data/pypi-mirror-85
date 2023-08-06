import os

SAMPLE_YAML_DATA = '''import:
  - datetime  # 动态导包，可在jinja2模板中使用
  - time
env:
  code: 200  # 上面定义的字段可被下面的字段引用
  # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 赋值说明(字段赋值的几种方式) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  # 1. 使用engine参数和rule参数进行函数调用，engine参数描述函数名，rule描述函数接收的参数
  example1:
    engine: eq
    rule:
      value: application/json
  # 2. 使用engine参数进行函数调用，忽略rule参数，可以将参数直接写在engine参数中，使用()包裹；参考Python函数调用的语法。
  # 参数较少时可以使用此方式。
  example2:
      engine: eq('application/json')
  # 3. 直接赋值，键值对就好了。
  example3: application/json  # 直接赋值也可以
  # 4. 使用jinja2模板对值动态渲染；可引用上面定义过的字段
  #    引用时需从顶级字段开始，且双大括号与具体的变量之间要空格，比如{{ env.content_type }}，
  #    不可写成{{ content_type }}或{{env.content_type}}
  example4: '{{ env.code }}'  # 引用上面定义过的变量
  # 5. 使用faker库的标准方法或自定义方法（faker对象已经注册到jinja2模板中，直接调用方法即可）
  example5: '{{ faker.name() }}'
  # 6. 使用Python标准库
  example6: '{{ print("code: {}".format(env.code)) }}'
  sleep_time:
    - weight: 0.4
      value: [1,3]
    - weight: 0.6
      value: [0,1]
request:
  path: /api/login
  method:
    - POST
  data: null
  json:
    username: xiaoming
    password: '123456'
  args:
    type: mobile
logic:
  # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 业务逻辑处理说明 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  # 每个处理逻辑写一个键值对，键的名称没有要求，但下方引用时需要用到。
  # 当返回结果为字典时可根据字典中的键来调用，比如logic.step2.code。 (前提是code必须存在，否则会报错)
  step1: '{{ print("username: {}\npassword: {}".format(request.json.username, request.json.password)) }}'
  step2:
    engine: verify_account('{{ request.json.username }}', '{{ request.json.password }}')
  step3: '{{ faker.gen_token(request.json.username) if logic.step2.code==200 else None }}'
  step4: '{{ print(logic.token) }}'  # 当要调试的时候可以考虑写一个print
  step5: '{{ time.sleep(faker.weights_randfloat(*env.sleep_time)) }}'  # 可写一个sleep来模拟延时返回

response:
  headers:
    Content-Type: '{{ env.example1 }}'
  body:
    code: '{{ logic.step2.code }}'
    msg: '{{ logic.step2.msg }}'
    respData: '{{ logic.step3 }}'
  status_code: 200
'''

SAMPLE_FUNCTION = '''from httpfaker.utils.faker_tool import Provider

class MyProvider(Provider):
    def verify_account(self, username, password):
        users = {
            'user001': '123456',
            'user002': '654321',
            'user003': '123456'
        }
        if username in users and users.get(username) == password:
            return {"code": 200, "msg": "请求成功"}
        elif username not in users:
            return {'code': 1002, 'msg': "用户不存在"}
        else:
            return {"code": 1001, "msg": "密码不正确"}

    def gen_token(self, username):
        return {"token": self.uuid()}
'''


README = '''# 目录结构说明
```
.
├── apis    # api yaml文件存放位置
├── log     # 执行日志
└── script  # 自定义方法的Python文件存放位置；在此路径中的所有py结尾的文件中的继承faker.BaseProvider类的子类会被动态加载到faker执行方法中。
```
'''

def scaffold(project_name='dbfaker-project', path=None):
    '''
    初始化dbfaker项目
    '''
    if not path:
        path = os.path.curdir
    if not os.path.isdir(path):
        raise OSError('目录错误')
    cur_dir = os.path.join(path, project_name)
    os.mkdir(cur_dir) if not os.path.exists(cur_dir) else None
    os.chdir(cur_dir)
    os.mkdir('apis') if not os.path.exists('apis') else None
    os.mkdir('log') if not os.path.exists('log') else None
    os.mkdir('script') if not os.path.exists('script') else None
    with open(os.path.join('apis', 'example.yml'), 'w', encoding='utf-8') as f:
        f.write(SAMPLE_YAML_DATA)
    with open(os.path.join('script', 'example.py'), 'w', encoding='utf-8') as f:
        f.write(SAMPLE_FUNCTION)
    with open(os.path.join('readme.md'), 'w', encoding='utf-8') as f:
        f.write(README)
    print('项目初始化完成')
