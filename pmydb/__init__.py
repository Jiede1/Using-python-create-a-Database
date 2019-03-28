#  coding = utf-8
#  @Author Jiede1
#  @Time 2019/03/18

from pmydb.core.database import Database
from pmydb.core import SerializedInterface
import base64
import os

'''
(1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
(2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
'''

# 解码数据
def _decode_db(content):
    content = base64.decodebytes(content)
    return content.decode()[::-1]


# 编码数据 str-->bytes-->base64 逆序
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

        self.__load_databases()        # 将以前的数据库，数据表load起来

        self.__format_type = format_type  # 数据默认返回格式

        # 数据库映射表，衔接parser模块
        self.__action_map = {
            'insert': self.__insert,
            'update': self.__update,
            'search': self.__search,
            'delete': self.__delete,
            'drop': self.__drop,
            'show': self.__show,
            'use': self.__use,
            'exit': self.__exit,
            'quit':self.__quit
        }

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
        return SerializedInterface.json.dumps([
             database.serialized() for database in self.__database_objs.values()
        ])

    #保存数据库
    def __dump_databases(self):
        with open(self.path, 'wb') as f:
            # 编码json字符串
            a = self.serialized()
            content = _encode_db(a)
            f.write(content)

    def deserialized(self, content):
        data_obj = SerializedInterface.json.loads(content)

        for database in data_obj:
            database = Database.deserialized(database)
            # 获取数据库名字
            db_name = database.get_name()

            # 追加数据库名字和绑定数据库对象
            self.__database_names.append(db_name)
            self.__database_objs[db_name] = database

    # 加载数据库
    def __load_databases(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, 'rb') as f:
            content = f.read()

        if content:
            # 解码数据，并把数据传给反序列化函数
            self.deserialized(_decode_db(content))

    # 提交数据库改动
    def commit(self):
        self.__dump_databases()

    # 回滚数据库改动，目前的实现有问题，不会判断以前的数据库表是否存在
    def rollback(self):
        self.__load_databases()

    # 查询指定数据表数据
    def search(self, table_name, fields='*', sort='ASC', **conditions):
        # 通过数据表名字获取指定的 Table 对象，再调用它的 search 方法获取查询结果
        return self.__get_table(table_name).search(fields=fields, sort=sort, format_type=self.__format_type,
                                                   **conditions)

    # 获取数据表
    def __get_table(self, table_name):

        # 判断当前是否有选中的数据库
        self.__check_is_choose()

        # 获取对应的 Table 对象
        table = self.__current_db.get_table_obj(table_name)

        # 如果 Table 对象为空，抛出异常
        if table is None:
            raise Exception('not table %s' % table_name)

        # 返回 Table 对象
        return table

    # 检查是否选择数据库
    def __check_is_choose(self):
        # 如果当前没有选中的数据库，抛出为选择数据库异常
        if not self.__current_db or not isinstance(self.__current_db, Database):
            raise Exception('No database choose')

    def insert(self,table_name,**data):
        return self.__get_table(table_name).insert(**data)

    # 删除指定数据表数据
    def delete(self, table_name, **conditions):
        return self.__get_table(table_name).delete(**conditions)

    # 更新指定数据表数据
    def update(self, table_name, data, **conditions):
        self.__get_table(table_name).update(data, **conditions)

    # 实现外部接口
    # 创建数据表
    def create_table(self, name, **options):
        self.__check_is_choose()
        self.__current_db.create_table(name, **options)

    # 获取数据库名
    def get_database(self, format_type='list'):
        databases = self.__database_names

        if format_type == 'dict':
            tmp = []
            for database in databases:
                tmp.append({'name': database})

            databases = tmp

        return databases

    # 获取数据表
    def get_table(self, format_type='list'):
        self.__check_is_choose()

        tables = self.__current_db.get_table()

        if format_type == 'dict':
            tmp = []
            for table in tables:
                tmp.append({'name': table})

            tables = tmp

        return tables

    def execute(self, statement):
        pass

    def __insert(self, action):
        table = action['table']
        data = action['data']

        return self.insert(table, data=data)

    def __update(self, action):
        table = action['table']
        data = action['data']
        conditions = action['conditions']

        return self.update(table, data, conditions=conditions)

    def __search(self):
        pass

    def __delete(self):
        pass

    def __show(self):
        pass

    def __exit(self):
        pass

    def __drop(self):
        pass

    def __quit(self):
        pass

    def __use(self):
        pass









