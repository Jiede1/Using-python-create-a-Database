#  coding = utf-8
#  @Author Jiede1
#  @Time 2019/03/09

from pmydb.core import FieldKey,FieldType,TYPE_MAP
from pmydb.core import SerializedInterface

class Field(SerializedInterface):
    def __init__(self, data_type, keys=FieldKey.NULL, default=None):
        self.__type = data_type  # 字段的数据类型
        self.__keys = keys  # 字段的数据约束  list类型
        self.__default = default  # 默认值
        self.__values = []  # 字段数据
        self.__rows = 0  # 字段数据长度

        # 如果约束只有一个，并且非 list 类型，则转换为 list
        if not isinstance(self.__keys, list):
            self.__keys = [self.__keys]

        # 如果类型不属于 FieldType，抛出异常
        if not isinstance(self.__type, FieldType):
            raise TypeError('Data-Type require type of "FieldType"')

        # 如果类型不属于 FieldKey，抛出异常
        for key in self.__keys:
            if not isinstance(key, FieldKey):
                raise TypeError('Data-Key require type of "FieldKey"')

        # 如果有自增约束，判断数据类型是否为整型和是否有主键约束
        if FieldKey.INCREMENT in self.__keys:
            # 如果不是整型，抛出类型错误异常
            if self.__type != FieldType.INT:
                raise TypeError('Increment key require Data-Type is integer')

            # 如果没有主键约束，抛出无主键约束异常
            if FieldKey.PRIMARY not in self.__keys:
                raise Exception('Increment key require primary key')

        # 如果默认值不为空并且设置了唯一约束，抛出唯一约束不能设置默认值异常
        if self.__default is not None and FieldKey.UNIQUE in self.__keys:
            raise Exception('Unique key not allow to set default value')

    # 判断数据类型是否符合
    def __check_type(self, value):
        # 如果该值的类型不符合定义好的类型，抛出类型错误异常
        if value is not None and not isinstance(value, TYPE_MAP[self.__type.value]):
            raise TypeError('data type error, value must be %s' % self.__type)

    # 判断指定位置数据是否存在
    def __check_index(self, index):
        # 如果指定位置不存在，抛出不存在该元素异常
        if not isinstance(index, int) or not 0 <= self.__rows > index:
            raise Exception('Not this element')
        return True

    # 键值约束
    def __check_keys(self, value):
        # 如果字段包含自增键，则选择合适的值自动自增
        if FieldKey.INCREMENT in self.__keys:
            # 如果值为空，则用字段数据长度作为基值自增
            if value is None:
                value = self.__rows + 1

            # 如果值已存在，则抛出一个值已经存在的异常
            if value in self.__values:
                raise Exception('value %s exists' % value)

        # 如果字段包含主键约束或者唯一约束，判断值是否存在
        if FieldKey.PRIMARY in self.__keys or FieldKey.UNIQUE in self.__keys:
            # 如果值已存在，抛出存在异常
            if value in self.__values:
                raise Exception('value %s exists' % value)

        # 如果该字段包含主键或者非空键，并且添加的值为空值，则抛出值不能为空异常
        if (FieldKey.PRIMARY in self.__keys or FieldKey.NOT_NULL in self.__keys) and value is None:
            raise Exception('Field Not Null')

        return value

    # 获取有多少条数据
    def length(self):
        return self.__rows

    # 获取数据
    def get_data(self, index=None):
        # 如果 index 参数为整型，则返回指定位置数据，反之返回所有数据
        if index is not None and self.__check_index(index):
            return self.__values[index]

        # 返回所有数据
        return self.__values

    # 添加数据
    def add(self, value):

        # 如果插入的数据为空，则赋值为默认值
        if value is None:
            value = self.__default

        # 判断数据是否符合约束要求
        value = self.__check_keys(value)

        # 检查插入数据的类型是否符合
        self.__check_type(value)

        # 追加数据
        self.__values.append(value)

        # 数据长度加一
        self.__rows += 1

    # 删除指定位置数据
    def delete(self, index):

        # 如果删除的位置不存在，抛出不存在该元素异常
        self.__check_index(index)

        # 删除数据
        self.__values.pop(index)

        # 数据长度减一
        self.__rows -= 1

    # 修改指定位置数据
    def modify(self, index, value):

        # 如果修改的位置小于0或者大于数据总长度，抛出不存在该元素异常
        self.__check_index(index)

        # 判断数据是否符合约束要求
        value = self.__check_keys(value)

        # 如果修改的值类型不符合定义好的类型，抛出类型错误异常
        self.__check_type(value)

        # 修改数据
        self.__values[index] = value

    def serialized(self):
        return SerializedInterface.json.dumps({
            'value': self.__values,
            'type': self.__type,
            'keys': self.__keys,
            'default': self.__default,
        })

    @staticmethod
    def deserialized(data):
        # 将数据转化为 Json 对象
        json_data = SerializedInterface.json.loads(data)

        # 转换 Json 对象中 key 的值为枚举类 FieldKey 中的属性
        keys = [FieldKey(key) for key in json_data['key']]

        # 传入解析出来的数据类型和字段键并实例化一个 Field 对象
        obj = Field(FieldType(json_data['type']), keys, default=json_data['default'])

        # 为 Field 对象绑定数据
        for value in json_data['values']:
            obj.add(value)

        # 返回该 Field 对象
        return obj



