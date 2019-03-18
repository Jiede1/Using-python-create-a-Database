#  coding = utf-8
#  @Author Jiede1
#  @Time 2019/03/17

from pmydb.core.database import Database
from pmydb.core import SerializedInterface
import base64

'''
(1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
(2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
'''

# 解码数据
def _decode_db(content):
    content = base64.decodebytes(content)
    return content.decode()[::-1]


# 编码数据
def _encode_db(content):
    content = content[::-1].encode()
    return base64.encodebytes(content)


# 数据库引擎
class Engine:
    def __init__(self, db_name=None, format_type ='dict', path='db.data'):
        ...
        self.__current_db = None  # 标示当前使用的数据库

        # 如果初始化时数据库名字参数不为空，调用 select_db 方法选中数据库
        if db_name is not None:
            self.select_db(db_name)
        self.__database_objs = {}       # 数据库映射表
        self.__database_names = []      # 数据库名字集合

        self.path = path

    # 创建数据库
    def create_database(self, database_name):
        # 判断数据库名字是否存在，如果存在，抛出数据库已存在异常
        if database_name in self.__database_objs:
            raise Exception('Database exist')

        # 追加数据库名字
        self.__database_names.append(database_name)

        # 关联数据库对象和数据库名
        self.__database_objs[database_name] = Database(database_name)

    def drop_database(self,database_name):
        # 判断数据库名字是否存在，如果存在，抛出数据库已存在异常
        if database_name not in self.__database_objs:
            raise Exception('Database not exist')

        self.__database_names.remove(database_name)

        self.__database_objs.pop(database_name, True)  #删除成功返回True

    # 选择数据库
    def select_db(self, db_name):
        # 如果不存在该数据库索引，抛出数据库不存在异常
        if db_name not in self.__database_objs:
            raise Exception('has not this database')

        # 将对应名字的 Database 对象赋值给 __current_db
        self.__current_db = self.__database_objs[db_name]

    def serialized(self):
        return SerializedInterface.json.dumps([ \
             database.serialized() for database in self.__database_objs.values() \
        ])

    def __dump_database(self):
        with open(self.path,'w') as f:
            # 编码json字符串
            content = _encode_db(self.serialized())
            f.write(content)





