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
import pandas
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, translator):
        """Инициализирует процесс. Поключается к двум очередям принимает на вход параметр - транслятор"""
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.translator = translator

    def run(self):
        """Ходит в бесконечном цикле, если в очереди есть задача, берет ее
        и передает во внутрь путь до транслятора"""
        pname = self.name

        while True:
            if not self.task_queue.empty():
                temp_task = self.task_queue.get()#взять задачу
                # print(pname)
                time.sleep(10)# костыль, т.к. файловая система еще может быть не обновилась
                masseg = temp_task.convertation(self.translator)#передает во внутрь путь до транслятора
                self.result_queue.put(masseg)#передача результата конвертации
            else:
                continue

class ConsumerSQL(multiprocessing.Process):

    def __init__(self, result_queue):
        """Инициализирует процесс для изменения статусов в SQLite"""
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue

    def run(self):
        """Ходит в бесконечном цикле, если в очереди есть задача"""
        pname = self.name
        engine = create_engine('sqlite:///D:\\AutoLouder_front\\mydatabase', echo=False) # создаем соединение с БД
        while True:
            if not self.result_queue.empty():
                Session = sessionmaker()
                Session.configure(bind=engine)  
                session = Session() # создание сессии
                temp_task = self.result_queue.get()#взять задачу
                date,code,status = temp_task.split('||')
                ourUser = session.query(Line).filter_by(created=date).first() # запрос на нужную строку
                if code=='0':
                    ourUser.status = 'Complite'#смена статуса
                    session.commit()# внесение изменений в БД
                else:
                    ourUser.status = status#смена статуса
                    session.commit()# внесение изменений в БД
            else:
                continue

class Task():
    """Класс реализует собой полный цикл конвертации данных и подключения исследования"""
    def __init__(self,body) -> None:
        self.body = body # принимает на вход путь до папки с файлами
        self.date = None
        self.status = None

    def convertation(self,translator):#  передать параметры запуска транслятору.
        '''Дописать закоментированные строки'''
        self.body,self.date=self.body.split(';')
        params = self.get_command(self.body)
        if self.status == None:
            try:
                cmd = "{}".format(translator)# параметр - какой транслятор запустить
                task = '{}\\{}'.format(self.body,'task.txt')# параметр - какой таск использовать для транслятора
                folder_name = self.body.split('\\')[-1]# параметр определяет конечную папку куда выгрузит файлы транслятор, так же определяет ID для подключения исследования
                # #print(folder_name)
                varnum = params['class']# определяет какой варнам использовать
                self.create_folder(f'D:\\DataFriend\\resources\\{folder_name}')#создать папку для выходных файлов
                command = subprocess.run([cmd, task, folder_name,varnum], stdout=subprocess.PIPE)#запускат транслятор с передачей параметрова
            except:
                self.status = '100||Внутренняя ошибка трасляции. Обрадитесь за поддержкой-DataFriend@ipsos.com'
                return self.date +'||'+ self.status
        # весь вывод транслтора принимает в себя.
            self.status = str(command.returncode)+'||'+str(command.stdout) #оптимизировать выход транслятора-слишком длинный
            self.to_js(params,folder_name)#после конвертации базы создает json для подлюкчения ее в DF
            return self.date +'||'+ self.status
        else:
            return self.date +'||'+ self.status

    def get_command(self,folder):
        ''' Функция считывает параметры из файла, выбирает нужный таск и создает такой же в папке с файлами исследования.'''
        param_file = os.listdir(path="{}".format(folder))#найти все файлы в папке
        param = [f for f in param_file if '_param' in f]#найти файл с параметрами
        try:
            param = param[0]#по сути там один файл, но нужно строка, а не лист
            df = pd.read_csv('{}\\{}'.format(folder,param),encoding ='utf-8',sep=';')
            df['Param'] = df['Param'].str.lower()# преобразует значения в колонке в нижний регистр(уменьшает шанс ошибки пользователя)
        except:
            self.status = '100||отсутствует файл Param.Проверьте правильность формата и названия'
            return None
        params={}

        try:
            for _ in df['Param']:# обходит файл собирая словарь ключ берет из колонки ПАрам, а значение из второй
                p = df.loc[df['Param']==_].index[0]
                list = df.loc[p].tolist()
                params[list[0]] = list[1]
            if params['task'] == 'Ruby': # проверяет какой таск для загрузки нужно использовать
                file_t = open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'task_ruby.txt','r'))
            else:
                file_t = open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'task_convert.txt','r'))
            task_f_base = open("{}\\{}".format(folder,'task.txt'), 'w') #создает пустой таск в папке с файлами базы в media
            for line in file_t:
                if line[:4] == 'ruby':# находит строку для вставки языка
                    task_f_base.write(line.format(params['lang']))
                else:
                    task_f_base.write(line)
            file_t.close()
            task_f_base.close()
            return params
        except:
            self.status = '100||ошибка в файле Param.Проверьте его содержимое'
            return None

    def to_js(self,params,folder_name):
        """Собирает в json параметры для покдключения базы"""
        for_result = {}
        for_result['ID'] = folder_name #
        for_result['Class'] = params['class']#
        for_result['Name'] = params['project_name']#
        for_result['ExportDate'] = ''#
        for_result['Country'] =''
        for_result['Start'] =''
        for_result['End'] =''
        for_result['Client'] = params['client']#
        for_result['Folder'] = params['folder']#
        to_connect = {}
        to_connect['results'] = [for_result]
        with open("C:\\Autoloader\\Autoconnect\\{}.json.done".format(folder_name), "w") as write_file: #дописать полный путь до папки автоконнекта
            json.dump(to_connect, write_file)
    
    def create_folder(self,direct):
        if not os.path.isdir(direct):#проверять,если папка не существует
            os.mkdir(direct)



Base = declarative_base() # декларативный способ связи таблицы с классом
class Line(Base):
    """Декларирование таблицы SQLite"""
    __tablename__ = 'profile_user_customfile' #имя таблицы
    id = Column(Integer, primary_key=True)# первичный ключ, без него не удастся выделить одну единственную строку
    user_id = Column(Integer)
    file_user_vars = Column(String)
    file_user_vals = Column(String)
    file_user_base = Column(String)
    file_user_weight = Column(String)
    created = Column(String)
    status = Column(String)
    name = Column(String)
    
    def __init__(self, status, created, file_user_base, file_user_vars, file_user_vals, file_user_weight, user_id, name):
        self.status = status
        self.created = created
        self.file_user_base = file_user_base
        self.file_user_vars = file_user_vars
        self.file_user_vals = file_user_vals
        self.file_user_weight = file_user_weight
        self.user_id = user_id 
        self.name = name
    def __repr__(self):
        return "<Line('%s','%s','%s')>" % (self.status, self.created,self.name)



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
    consumers = [Consumer(tasks, results, translator) for translator in translators] #запускаем по процессу на каждый транслятор
    consumers.append(ConsumerSQL(results)) # добавляем процесс с изменением статусов в БД
    for consumer in consumers:
        consumer.daemon = True
        consumer.start()# запускаем процессы

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
