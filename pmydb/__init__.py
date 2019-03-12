#  coding = utf-8
#  @Author Jiede1
#  @Time 2019/03/12

from pmydb.core.database import Database
from pmydb.core import SerializedInterface

# 数据库引擎
class Engine:
    def __init__(self, db_name=None, format_type='dict'):
        ...
        self.__current_db = None  # 标示当前使用的数据库

        # 如果初始化时数据库名字参数不为空，调用 select_db 方法选中数据库
        if db_name is not None:
            self.select_db(db_name)
        self.__database_objs = {}       # 数据库映射表
        self.__database_names = []      # 数据库名字集合

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



