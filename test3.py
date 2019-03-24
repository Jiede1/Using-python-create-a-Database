from pmydb import Engine
from pmydb.case import *


e = Engine()                    # 实例化数据库引擎对象
e.select_db('test_db')          # 选择数据库 test_db
'''
# 向表 `t_test` 中添加一些数据
e.insert(table_name='t_test', f_name='shiyanlou_003', f_age=30)
e.insert(table_name='t_test', f_name='shiyanlou_004', f_age=40)
e.insert(table_name='t_test', f_name='xiaoming', f_age=50)
e.insert(table_name='t_test', f_name='echo', f_age=50)
'''

print("-"*5, "这里是表 t_test 的全部数据", "-"*5)
all_data = e.search("t_test")
for i in all_data:
    print(i)
print("-" * 30)


print("-"*5, "查询年龄在三十岁以上的用户", "-"*5)
test1_data = e.search(table_name="t_test", f_age=GreaterCase(30))
for i in test1_data:
    print(i)
print("-" * 30)
print("-"*5, "查询年龄在[10,40,50,60],id在[1,2,3,4]的用户", "-"*5)
test1_data = e.search(table_name="t_test", f_age=InCase([10,40,50,60]),f_id=InCase([1,2,3,4]))
for i in test1_data:
    print(i)
print("-" * 30)
print("-"*5, "查询id在range(5)的用户", "-"*5)
test1_data = e.search(table_name="t_test", f_id=RangeCase(0,5))
for i in test1_data:
    print(i)
print("-" * 30)
print("-"*5, "查询f_name类似ou_001的用户", "-"*5)
test1_data = e.search(table_name="t_test", f_name=LikeCase('ou_001'))
for i in test1_data:
    print(i)
print("-" * 30)


# 保存更改到数据库中
#e.commit()
