import os
import json

childrenMap = '{"name":"%s","type":"file","children":[]}'

directory = {
        'name':'pmydb',
        'type':'dir',
        'children':[
            {'name':'__init__.py','type':'file','children':[]},
            {'name':'__main__.py','type':'file','children':[]},
            {'name':'case','type':'dir','children':[
                json.loads(childrenMap%('__init__.py'))
            ]},
            {'name':'core','type':'dir','children':[
                json.loads(childrenMap%('__init__.py')),
                json.loads(childrenMap%('database.py')),
                json.loads(childrenMap%('field.py')),
                json.loads(childrenMap%('table.py')),
            ]},
            {'name':'exceptions','type':'dir','children':[
                json.loads(childrenMap%('__init__.py'))
            ]},
            {'name':'parser','type':'dir','children':[
                json.loads(childrenMap%('__init__.py'))
            ]},
        ]
}
def gen_dir(absPath,directory):  #absPath为当前路径
    if directory['type'] == 'dir':
        path = os.path.join(absPath, directory['name'])
        os.mkdir(path)
        for next in directory['children']:
            gen_dir(path, next)
    else:
        f = open(os.path.join(absPath, directory['name']), 'w')
        f.close()

if  __name__ ==  '__main__':
    path = os.getcwd()
    gen_dir(path, directory)

