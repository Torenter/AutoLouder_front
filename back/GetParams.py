import os
import pandas as pd
from abc import ABC, abstractmethod

class IParam(ABC):
    @abstractmethod
    def get_params(self):
        pass


class ParsePram():
    """Класс разбирает файл param на словарь"""
    def __init__(self,path) -> None:
        self.path = path
        self.status_param = None
        self.__param = {}
        self.status = None

    def __parse(self):
        param_file = os.listdir(path="{}".format(self.path))#найти все файлы в папке
        param = [f for f in param_file if '_param' in f]#найти файл с параметрами
        try:
            df = pd.read_csv('{}\\{}'.format(self.path,param[0]),encoding ='utf-8',sep=';')
            df['Param'] = df['Param'].str.lower()# преобразует значения в колонке в нижний регистр(уменьшает шанс ошибки пользователя)
            df = df.fillna('') # заменить nan на пустую строку
        except:
            self.status_param ='отсутствует файл Param.Проверьте правильность формата и названия'
        try:
            for _ in df['Param']:# обходит файл собирая словарь ключ берет из колонки ПАрам, а значение из второй
                p = df.loc[df['Param']==_].index[0]
                list = df.loc[p].tolist()
                self.__param[list[0]] = list[1]
        except:
            self.status_param = 'Отсутствует колонка "Param"'

    def get_param(self) -> dict:
        """Интерфейс"""
        self.__parse()
        return self.__param


class CheckFile():
    """Класс проверяет наличие и расширение файлов для корректного форамирования таска в будущем"""
    def __init__(self,path) -> None:
        self.path = path
        self.__vals = None
        self.__wt = None
        # self.status = None
        self.__db = None

    def __check(self):
        files = os.listdir(path="{}".format(self.path))#найти все файлы в папке
        vals = bool([i for i in files if '_vals' in i])
        if vals == False:
            self.__vals = {'no_vals':'get_vals'}
        else:
             self.__vals = {'no_vals':''}
        wt = bool([i for i in files if '_wt' in i])
        if wt == True:
            self.__wt = {'wt':'wt'}
        else:
            self.__wt = {'wt':''}
    
    def __checkBD(self):
        """Проверят в каком формате БД и возвращает ее формат как ключ для таска.
        Если баз несколько, выбирает ту, что была загружена позже"""
        files = os.listdir(path="{}".format(self.path))#найти все файлы в папке
        name = self.path.split('\\')[-1]
        self.__db = [i for i in files if i == f'{name}.sav' or i == f'{name}.csv'] #ищет все файлы с названием как у БД, в формате sav и csv 
        if len(self.__db) > 1: # если файлов больше чем один, то выбирает тот, что был загружен последним
            one = os.path.getctime(f'{self.path}\\{self.__db[0]}') #получает дату создания
            two = os.path.getctime(f'{self.path}\\{self.__db[1]}')
            if one > two:
                self.__db = {'bd':self.__db[0].split('.')[-1]} #Запишет в атрибут только расширение БД
            else:
                self.__db = {'bd':self.__db[1].split('.')[-1]} #Запишет в атрибут только расширение БД
        elif len(self.__db) == 1:
            self.__db = {'bd':self.__db[0].split('.')[-1]} #Запишет в атрибут только расширение БД
        else:
            self.__db = {'bd':""} #Если ни один файл не был найден, значит некорректное имя БД
            self.status = 'Не найдет файл с базой.'
    
    def check(self) -> dict:
        """Интерфейс"""
        self.__check()
        self.__checkBD()
        return {**self.__vals, **self.__wt, **self.__db}


class Param(ParsePram,CheckFile,IParam):
    """Коллектор функционала по сбору параметров на подключение и формирование таска загрузки
    Основной метод get_params - выдает словарь с информацией о наличии и форматах файлов + разбор param
    При создании экземпляра требует указать путь до папки с файлами"""
    def __init__(self,path) -> None:
        super().__init__(path)
        self.__check = super().check()
        self.__get_param = super().get_param()
        self.__params = {**self.__get_param, **self.__check}
        self.__status_main = None
    
    def __status(self):
        if self.status == None and self.status_param != None:
            self.__status_main = self.status_param
        elif self.status != None and self.status_param == None:
            self.__status_main = self.status
        elif self.status != None and self.status_param != None:
            self.__status_main = f'{self.status_param};{self.status}'
        else:
            self.__status_main = None

    def get_params(self) -> dict:
        """Интерфейс"""
        self.__status()
        return self.__params,self.__status_main


if __name__== '__main__':
    v,s = Param('C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media\\Md1').get_params()
    print(v)
    print(s)
    # v = v.get_param()
    # print(Param('C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media\\Md').get_param())
    """Есть нет Param - возвращать ошибку - доделать, а может и не стоит, т.к. это не сказывается на конвертации.
    Можно вернуть статус, что всё готово но не подключено из-за ошибки в парам"""