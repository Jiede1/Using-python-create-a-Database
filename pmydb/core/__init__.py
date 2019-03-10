#  coding = utf-8
#  @Author Jiede1
#  @Time 2019/03/09

from enum import Enum
import json


# 数据库核心模块序列化接口
class SerializedInterface:
    json = json    # 内部定义一个 json 对象，方便后续操作不需要 import

    # 反序列化方法
    @staticmethod
    def deserialized(obj):
        raise NotImplementedError   # 抛出未实现异常

    # 序列化方法
    def serialized(self):
        raise NotImplementedError   # 抛出未实现异常

# 字段类型枚举
class FieldType(Enum):
    INT = int = 'int'  # 整型
    VARCHAR = varchar = 'str'  # 字符型
    FLOAT = float = 'float'  # 浮点型

# 数据类型映射
TYPE_MAP = {
    'int': int,
    'float': float,
    'str': str,
    'INT': int,
    'FLOAT': float,
    'VARCHAR': str
}

# 数据约束
class FieldKey(Enum):
    PRIMARY = 'PRIMARY KEY'         # 主键约束
    INCREMENT = 'AUTO_INCREMENT'    # 自增约束
    UNIQUE = 'UNIQUE'               # 唯一约束
    NOT_NULL = 'NOT NULL'           # 非空约束
    NULL = 'NULL'                   # 可空约束，作为默认的约束使用

if __name__ == '__main__':
    print(FieldKey.PRIMARY.value)

