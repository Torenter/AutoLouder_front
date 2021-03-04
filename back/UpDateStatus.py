from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading
from abc import ABC, abstractmethod

class IResponsDB(ABC):
    def __init__(self) -> None:
        self.__vals = None
        self.__wt = None
        self.__db = None
        self.__taks = None
        self.__param = None
        self.__engine = create_engine(f'sqlite:///{self.db}', echo=False) # создаем соединение с БД
    @abstractmethod
    def __get_vals(self):
        pass
    @abstractmethod
    def __get_wt(self):
        pass
    @abstractmethod
    def __get_db(self):
        pass
    @abstractmethod
    def __get_task(self):
        pass
    @abstractmethod
    def __get_class(self):
        pass
    @abstractmethod
    def get_param(self):
        pass

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
    # def __repr__(self):
    #     return "<Line('%s','%s','%s')>" % (self.status, self.created,self.name)


class ConsumerSQL(threading.Thread):

    def __init__(self, result_queue,db: str):
        """Инициализирует процесс для изменения статусов в SQLite
        Из очереди берет задачу в формате <описать формат>"""
        threading.Thread.__init__(self)
        self.result_queue = result_queue
        self.db = db

    def run(self):
        """Ходит в бесконечном цикле, если в очереди есть задача"""
        pname = self.name
        engine = create_engine(f'sqlite:///{self.db}', echo=False) # создаем соединение с БД
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

if __name__== '__main__':
    import os
    import configparser
    import queue
    config = configparser.ConfigParser()
    config.read('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),"conf.ini"))
    translators = [value for key, value in config['Translators'].items() ]
    autoconnect = config['Path']['autoconnect']
    resours = config['Path']['resours']
    db = config['DataBase']['db']
    results = queue.Queue()

    s = ConsumerSQL(results,db)

    s.start()
    results.put('2021-02-09 15:15:13.452821||100||dsagfas')
