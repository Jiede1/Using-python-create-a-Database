from pmydb import Engine
from pmydb.core import FieldKey, FieldType
from pmydb.core.field import Field

e = Engine()
print(e.get_database())

import re
pat=re.compile(r'(INSERT|insert) (INTO|into) (.*) (\(.*\)) (VALUES|values) (\(.*\))')
print(pat.findall("INSERT INTO Persons ('dsd') VALUES ('fgg','d')"))