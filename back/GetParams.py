import os
import pandas as pd
from abc import ABC, abstractmethod

class IParam(ABC):
    @abstractmethod
    def get_params(self):
        pass


class ParsePram():
    """Класс разбирает файл param на словарь"""
    def __init__(self,comand) -> None:
        self.path = f"{comand['path']}\\{comand['name']}"
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
    def __init__(self,comand) -> None:
        self.comand = comand
        self.__vals = None
        self.__wt = None
        # self.status = None
        self.__db = None

    def __check(self):
        self.__vals = self.__len_file(self.comand["no_vals"])
        self.__wt = self.__len_file(self.comand["wt"])
        self.__db = self.__len_file(self.comand["bd"])
        if self.__vals == '':
            self.comand["no_vals"] = 'get_vals'
        else:
            self.comand["no_vals"] = ''
        if self.__wt == '':
            self.comand["wt"] = ''
        else:
            self.comand["wt"] = 'wt'
        if self.__db.split('.')[1] == 'sav':
            self.comand["bd"] = 'sav'
        else:
            self.comand["bd"] = 'csv'

    def __len_file(self,f):
        try:
            f = f.split('/')
        except:
            return ''
        if len(f)<2:
            if f[0] != None:
                if len(f[0])==0:
                    return f[0]
                elif len(f[0])>0:
                    return f[0]
            elif f[0] == None:
                return ""
        elif len(f)>1:
            return f[1]
    
    def check(self) -> dict:
        """Интерфейс"""
        self.__check()
        return self.comand


class Param(ParsePram,CheckFile,IParam):
    """Коллектор функционала по сбору параметров на подключение и формирование таска загрузки
    Основной метод get_params - выдает словарь с информацией о наличии и форматах файлов + разбор param
    При создании экземпляра требует указать путь до папки с файлами"""
    def __init__(self,comand) -> None:
        ParsePram.__init__(self,comand)
        self.__get_param = super().get_param()
        CheckFile.__init__(self,comand)
        self.__check = super().check()
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
    p = {"comand":"Ruby",'bd':'lkjahfg.sav','wt':"","no_vals":None,"lang":'RU','path':'C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media','name':'Md1'}
    v,s = Param(p).get_params()
    print(v)
    print(s)
    # v = v.get_param()
    # print(Param('C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media\\Md').get_param())
    # p = {"comand":"Ruby",'bd':'lkjahfg.sav','wt':"","no_vals":None,"lang":'RU'}
    # v = CheckFile(p).check()
    # print(v)