#  coding = utf-8
#  @Author Jiede1
#  @Time 2019/03/27


import re

from pmydb.case import *

class SQLParser:
    def __init__(self):
        self.__action_map = {
            'SELECT': self.__select,
            'UPDATE': self.__update,
            'DELETE': self.__delete,
            'INSERT': self.__insert
        }
        self.__pattern_map = {
            'SELECT': r'(SELECT|select) (.*) (FROM|from) (.*)',
            'UPDATE': r'(UPDATE|update) (.*) (SET|set) (.*)',
            'INSERT': r'(INSERT|insert) (INTO|into) (.*) \((.*)\) (VALUES|values) \((.*)\)'
        }
        self.SYMBOL_MAP = {
            'IN': InCase,
            'NOT_IN': NotInCase,
            '>': GreaterCase,
            '<': LessCase,
            '=': IsCase,
            '!=': IsNotCase,
            '>=': GAECase,
            '<=': LAECase,
            'LIKE': LikeCase,
            'RANGE': RangeCase
        }
    def __filter_space(self,obj):
        ret = []
        for x in obj:
            if x.strip() == '' or x.strip() == 'AND':
                continue
            ret.append(x)
        return ret

    def parse(self,statement):
        if 'where' in statement:
            statement = statement.split("where")
        else:
            statement = statement.split("WHERE")
        base_statement = self.__filter_space(statement[0].split(" "))

        # SQL 语句一般由最少三个关键字组成，这里设定长度小于 2 时，又非退出等命令，则为错误语法
        if len(base_statement) < 2 and base_statement[0] not in ['exit', 'quit']:
            raise Exception('Syntax Error for: %s' % statement)

        # 在定义字典 __action_map 时，字典的键使用的是大写字符，此处转换为大写格式
        action_type = base_statement[0].upper()

        if action_type not in self.__action_map:
            raise Exception('Syntax Error for: %s' % statement)

        # 根据字典得到对应的值
        action = self.__action_map[action_type](base_statement)

        if action is None or 'type' not in action:
            raise Exception('Syntax Error for: %s' % statement)


    def __get_comp(self, action):
        return re.compile(self.__action_map[action])

    def __select(self, statement):
        comp = self.__get_comp('SELECT')
        ret = comp.findall(' '.join(statement))

        if ret and len(ret[0]) == 4:
            fields = ret[0][1]
            table = ret[0][3]

            if fields != '*':
                fields = [ field for field in fields.split(',') ]
            return {
                'type': 'search',
                'table': table,
                'fields': fields
            }
        return None
    def __update(self,statement):
        comp = self.__get_comp('UPDATE')
        ret = comp.findall(' '.join(statement))

        if ret and len(ret[0]) == 4:
            data = {
                'type': 'update',
                'table': ret[0][1],
                'data': {}
            }
            set_statement =ret[0][3].split(',')
            for s in set_statement:
                s = s.split('=')
                field = s[0].strip()
                value = s[1].strip()
                if "'" in value or '"' in value:
                    value = value.replace('"','').replace(",",'').strip()
                else:
                    try:
                        value = int(value.strip())
                    except:
                        return None
                data['data'][field] = value
            return data
        return None

    def __delete(self,statement):
        pass

