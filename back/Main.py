# from . import GetParams, CreateTask, Convertation, Connect, UpDateStatus
from GetParams import Param
from UpDateStatus import ConsumerSQL

from CreateTask import TaskCreate
from Convertation import RunTranslate
from Connect import Connect
import threading, socket, time, os, configparser, queue, json

class Consumer(threading.Thread):

    def __init__(self, task_queue, result_queue, translator,resours,autoconnect):
        """Инициализирует процесс. Поключается к двум очередям принимает на вход параметр - транслятор"""
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.translator = translator
        self.resours_path = resours
        self.autoconnect = autoconnect


    def run(self):
        """Ходит в бесконечном цикле, если в очереди есть задача, берет ее
        и передает во внутрь путь до транслятора"""
        pname = self.name

        while True:
            if not self.task_queue.empty():
                comand = self.task_queue.get()#взять задачу
                full_path = str(comand['path']+'\\'+comand['name']) #слепить полный путь до папки с файлами
                params,status= Param(full_path).get_params()
                comand = {**comand,**params}
                if status == None:
                    task = TaskCreate(comand,full_path).createTask()
                    if status == None:
                        convert,status = RunTranslate(self.translator,task,params['class'],comand['name'],self.resours_path,comand['path']).convert()
                        if status == None:
                            connect,status = Connect(self.autoconnect,comand['name'],params).connect()
                            if status == None:
                                self.result_queue.put(f'{comand["key"]}||0||Complited')
                            else:
                                self.result_queue.put(f'{comand["key"]}||100||{status}')
                        else:
                            self.result_queue.put(f'{comand["key"]}||100||{status}')
                    else:
                        self.result_queue.put(f'{comand["key"]}||100||{status}')
                else:
                    self.result_queue.put(f'{comand["key"]}||100||{status}')
            else:
                continue


if __name__== '__main__':
    # from back.GetParams import Param
   
    """Сбор параметров"""
    config = configparser.ConfigParser()
    config.read('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),"conf.ini"))
    translators = [value for key, value in config['Translators'].items() ]
    autoconnect = config['Path']['autoconnect']
    resours = config['Path']['resours']
    db = config['DataBase']['db']

    """Инициализация объектов"""
    TaskCreate.readTask()
    tasks = queue.Queue()
    results = queue.Queue()
    # spawning consumers with respect to the
    # number cores available in the system
    consumers = [Consumer(tasks, results, translator, resours,autoconnect) for translator in translators] #запускаем по процессу на каждый транслятор
    consumers.append(ConsumerSQL(results,db)) # добавляем поток с изменением статусов в БД
    for consumer in consumers:
        # consumer.daemon = True
        consumer.start()# запускаем поток

    """Запуск сервера"""
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',50000))
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
            result = json.loads(result.decode('utf-8')) # Превращение json строки обратно в словарь
            tasks.put(result)