# Using-python-create-a-Database

先直接上数据库完成后的测试图：  
运行test4.py  
![运行test4.py](https://github.com/Jiede1/Using-python-create-a-Database/blob/master/picture/test.PNG)  
![运行test4.py](https://github.com/Jiede1/Using-python-create-a-Database/blob/master/picture/test1.PNG)  
![运行test3.py](https://github.com/Jiede1/Using-python-create-a-Database/blob/master/picture/test30.PNG)  
![运行test3.py](https://github.com/Jiede1/Using-python-create-a-Database/blob/master/picture/test31.PNG)  
  
### 前言  
在实现该数据库之前，先整理一下我对关系型数据库的理解：  
* 关系型数据库存储的是结构化的数据，数据是有顺序的，不能打乱  
* 关系型数据库每列定长，且每列对应着一个唯一列名  
* 关系型数据支持SQL语言的操作，增删查改   
   
**该数据库的实现是基于关系型数据库，因此会拥有上面所有的特性。**
  
### 数据库拥有特性
* 支持增删查改，不支持join，groupBy等高级操作，后期会加
* 数据存储跟关系型数据库格式一致，结构化，有严格顺序，每列每行都等长
* 数据库支持数据约束，包含自增约束，唯一约束，非空约束，主键约束
* 数据库只支持基本的数据类型，int,float,str  

目前，支持增删查改的命令如下：  

**增：INSERT INTO table_name (列1, 列2,…) VALUES (值1, 值2,…)**  
**删： DELETE FROM 表名称 WHERE 列名称 = 值**  
**更新：UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值**    
**查：SELECT 列名称 FROM 表名称 WHERE 列名称 = 值**    
  
**where后面的条件判断可以是 （>,>=,<.<=,!=,=,like,range(…),in,not in**   
  
  
以上数据库属性皆可完善。可能在后期逐步添加。
  
### 数据库架构  

#### **数据库的详细架构内容，笔者在博客上阐述了。有意者前往（要不readme.md要敲很多字），博客地址：https://blog.csdn.net/jiede1/article/details/88921007**  
  
![架构图](https://github.com/Jiede1/Using-python-create-a-Database/blob/master/picture/%E6%9E%B6%E6%9E%84.PNG)
### 数据库各个模块功能需求  
1.数据库的组成
数据库包括七个模块，数据库模块，数据表模块，数据字段模块，数据引擎模块，条件模块，SQL 语句解析模块，异常处理模块

1.1 数据字段模块实现  
* 一个存放值的 List 列表
* 可定义 数据类型
* 可定义 数据约束 
* 支持 序列化 和 反序列化
* 支持 增、删、改、查 基础操作

数据类型目前只会实现基本类型(int,float,str)，数据约束只会实现非空，唯一，自增主键约束。  

1.2 数据表模块实现  
* 一个存放 Field 对象的键值对字典
* 添加字段操作
* 支持 增、删、改、查 操作
* 序列化 和 反序列化

1.3.数据库模块实现  
* 纪录绑定的数据表名与数据表对象
* 删除和新建数据表
* 支持 序列化 和 反序列化  

1.4.数据库引擎模块实现（难度较大）
* 保存与加载本地数据
* 数据操作
* 操作回滚与提交
* 数据库的创建与删除  

1.5.数据库条件模块实现（相对来说，难度比较大）
* 控制数据更新，删除和查询的条件匹配 

1.6 SQL 语法解析模块  
* 将数据库各种操作映射为SQL操作  
* 命令行形式需要 prettytable 支持  

### 数据库测试

这一部分非常重要，宣告一个数据库是否通过 最简单的办法就是测试其增删查改操作  
 test1.py 测试数据库是否可以正确创建，插入数据，查询数据，保存数据（主目录下的db.data）  
 test3.py 全面测试数据库的查询  
 test4.py 基于SQL命令测试数据库操作  

目前初步测试通过 

### 读者如果有问题，可以在GitHub上留言我，也可以去我博客下留言
