# 该文件用于创建测试用的数据库，笔者已经创建，不用运行了，如果读者想运行，先删除同一目录下的db.data
# db.data是序列化后的测试数据库

'''
from pmydb import Engine
from pmydb.core import FieldKey,FieldType
from pmydb.core.field import Field


e = Engine()
e.create_database('test_db')
e.select_db('test_db')
print(e.get_database())

e.create_table(
    name='t_test',
    f_id=Field(data_type=FieldType.INT, keys=[FieldKey.PRIMARY, FieldKey.INCREMENT]),
    f_name=Field(data_type=FieldType.VARCHAR, keys=FieldKey.NOT_NULL),
    f_age=Field(data_type=FieldType.INT, keys=FieldKey.NOT_NULL)
)
# 向数据表 t_test 中插入数据
e.insert(table_name='t_test', f_name='shiyanlou_001', f_age=20)
e.insert(table_name='t_test', f_name='shiyanlou_002', f_age=10)

ret = e.search('t_test')
for row in ret:
    print('row:', row)

# 保存数据库内容到本地默认的 db.data 文件中
e.commit()    # 将数据存起来，覆盖掉以前的数据
#e.rollback()   # 将以前的数据load起来
print(e.get_database())
'''