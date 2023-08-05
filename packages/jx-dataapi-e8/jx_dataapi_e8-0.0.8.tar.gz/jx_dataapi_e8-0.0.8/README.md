# 嘉迅网关数据接口封装包（jx-dataapi-e8）

主要功能
- 数据查询
- 用量计算
- 网关采集设置
- 告警设置

封装功能
- 异常值处理
- 缺失值处理
- 设备变比处理
- 特殊协议解析处理
- 更换表计、更换网关编号数据衔接处理
- 通用用量计算
- 主动/被动监控告警设置

使用说明
- 安装包
```
pip install jx-dataapi-e8
```
- 使用包
```
# 云端版
from dataapi_e8 import DataApi

api = DataApi('https://e8api.xjiaxun.com/api','appid','appsecret')
ret = api.get_latest(devs='E80142003_0101')


# 本地版
from dataapi_e8 import DataApiLocal

api = DataApiLocal('http://127.0.0.1:8000/api','appid','appsecret')
ret = api.get_latest(devs='E80142003_0101')
```
初始化参数说明：
1. baseurl 接口地址
2. appid 接口appid
3. appsecret 接口appsecret
4. configObj 接口配置文件，如下
```
class Config(object):

    # 设备更换信息配置
    E8API_CHANGE_CONFIG = {
        'E81022180_0101': {
            # 网关编号更换情况
            'wg':  [
                {
                    "mid": "E81022180_0102", # 网关编号
                    "tm": 0 # 采集时间
                },{
                    "mid": "E81022180_0101",
                    "tm": 1590447603
                }
            ],
            # 表计更换情况
            'meter': [
                {
                    "tm": 1590447603, # 更换时间
                    "vals": {
                        "ImpEp": [  # 需要衔接的属性
                            28, # 更换前数值
                            47  # 更换后数值
                        ]
                    }
                }
            ]
        }
    }
    # 接口数据开始时间配置
    E8API_BEG_CONFIG = {
        'E81022180_0101': 1590426063
    }
    # 需要补值的参数
    E8API_FILL_ATTR_CONFIG = ['ImpEp']
```
5. debug 启动调试模式
6. timeout 接口调用超时时间

- 开放接口

    详见接口文档

打包上传
```
python3 setup.py sdist build

twine upload ./dist/*
```