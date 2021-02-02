import os
from os import close
import pandas as pd
def get_command(folder):
    ''' Функция считывает параметры из файла, выбирает нужный таск и создает такой же в папке с файлами исследования.'''
    param_file = os.listdir(path="{}".format(folder))
    param_file_1 =None
    for _ in param_file:
        if _[-10:] == '_param.csv':
            param_file_1 = '{}\\{}'.format(folder,_)
    df = pd.read_csv(param_file_1,encoding ='utf-8',sep=';')
    params={}
    for _ in df['Param']:
        p = df.loc[df['Param']==_].index[0]
        list = df.loc[p].tolist()
        params[list[0]] = list[1]
    if params['Task'] == 'Ruby':
        file_t = open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'task_ruby.txt','r'))
    else:
        file_t = open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'task_convert.txt','r'))
    task_f_base = open("{}\\{}".format(folder,'task.txt'), 'w')
    for line in file_t:
        if line[:4] == 'ruby':
            task_f_base.write(line.format(params['Lang']))
        else:
            task_f_base.write(line)
    file_t.close()
    task_f_base.close()
    return params

if __name__ == "__main__":
    print('Должен быть импортирован')