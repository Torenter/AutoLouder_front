import os
from os.path import basename
import multiprocessing
import sys,os,subprocess,time
import pandas as pd
import json
from os import close
import os
import time
import socket

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, translator):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.translator = translator

    def run(self):
        pname = self.name

        while True:
            if not self.task_queue.empty():
                temp_task = self.task_queue.get()
                print(pname)
                temp_task.convertation(self.translator)
            else:
                continue

class Task():
    def __init__(self,body) -> None:
        self.body = body

    def convertation(self,translator):#  передать параметры запуска транслятору.
        '''Дописать закоментированные строки'''
        params = self.get_command(self.body)
        cmd = "{}".format(translator)
        task = '{}\\{}'.format(self.body,'task.txt')
        folder_name = self.body.split('\\')[-1]
        varnum = params['Class']
        #command = subprocess.run([cmd, task, folder_name, folder_name,varnum], stdout=subprocess.PIPE)
        self.to_js(params,folder_name)


    def get_command(self,folder):
        ''' Функция считывает параметры из файла, выбирает нужный таск и создает такой же в папке с файлами исследования.'''
        param_file = os.listdir(path="{}".format(folder))#найти все файлы в папке
        params = [f for f in param_file if '_param' in f]#найти файл с параметрами
        try:
            df = pd.read_csv('{}\\{}'.format(folder,params),encoding ='utf-8',sep=';')
        except:
            return None
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

    def to_js(self,params,folder_name):
        """Собирает в json параметры для покдключения базы"""
        for_result = {}
        for_result['ID'] = folder_name
        for_result['Class'] = params['Class']
        for_result['Name'] = params['project_name']
        for_result['ExportDate'] = ''
        for_result['Country'] =''
        for_result['Start'] =''
        for_result['End'] =''
        for_result['Client'] = params['Client']
        for_result['Folder'] = params['folder']
        to_connect = {}
        to_connect['result'] = [for_result]
        with open("{}.json.done".format(folder_name), "w") as write_file:
            json.dump(to_connect, write_file)

def get_translators():
    """Получает из txt файла путь до трансляторов"""
    file_t = open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'translators.txt','r'))
    file_d = ''.join(file_t)
    file_t.close()
    file_d = file_d.split('\n')
    for _ in file_d:
        if _ == '':
            file_d.remove(_)
    return file_d   
if __name__== '__main__':
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()
    translators = get_translators()
    # spawning consumers with respect to the
    # number cores available in the system
    consumers = [Consumer(tasks, results, translator) for translator in translators]
    for consumer in consumers:
        consumer.start()

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',9090))
    server.listen(100)
    print('Server start')
    while True:
        try:
            client,addr = server.accept()
        except  KeyboardInterrupt:
            server.close()
            break
        else:
            result = client.recv(1024)
            client.close()
            tasks.put(Task(result.decode('utf-8')))


    #Cуществующие проблему
    #1)Если папка медиа будет локально открыта, ее обновление происходит очень долго, и если в этот момент будет
    #происходить загрузка, то выпадает ошибка, что пусть не найден - или решить, или нехер открывать этот каталог.
    #2) Сделать так, чтобы в "парамс" передавался не Ruby - True а именно имя таска, которое должно быть применено
    #
    #
    #
    #