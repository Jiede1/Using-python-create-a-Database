class birds:
    def __init__(self):
        self.name = 'ds'

    @staticmethod
    def watch():
        print(112)
        return 112

#a=birds()
#print(a.watch())
print(birds.watch())

print(isinstance([1,2],list))

import json

print(json.loads('{"1":"2"}'))   #str --> dict

import json


# 数据库核心模块序列化接口
class SerializedInterface:
    json = json # 内部定义一个 json 对象，方便后续操作不需要 import
    def __init__(self):
        self.name = 'json'

    # 反序列化方法
    @staticmethod
    def deserialized(obj):
        raise NotImplementedError   # 抛出未实现异常

    # 序列化方法
    def serialized(self):
        raise NotImplementedError   # 抛出未实现异常
print(SerializedInterface.json)
print(SerializedInterface().name)
'''
a=SerializedInterface()
a.serialized()
a.deserialized()
'''
a=(int,float,str)
print(isinstance(1,a))

from enum import Enum

class Color(Enum):
    red = 1
    orange = 2
    yellow = 3
    green = 4
    blue = 5
    indigo = 6
    purple = 7
print(Color(1))
print(Color['red'])
print(Color.red.value)
print(Color.red.value)

rows=[1,2,3,4,5,5]
print(rows[::-1])
if not '':
    print(13)
else:
    print(2)

def parse_conditions(**conditions):
    # 如果条件为空，数据索引为所有，反之为匹配条件的索引
    if 'index' in conditions:
        if conditions['index'] == '*':
            match_index = range(0, 4)
            return match_index
        else:
            print(type(conditions['index']))
            print(isinstance(conditions['index'], list))
            return conditions['index']

    else:
        match_index = range(0, 4)
        return match_index

print(parse_conditions(index=[1,2,3,45,5]))
print(parse_conditions())

a=[1,2,3,4,1,2,1,2,3,6,3,1]
a.sort()
print(a)

def pp(**data):
    ff = mp(**data)
    return ff
def mp(**data):
    return data.keys()
print(pp(da=2))

