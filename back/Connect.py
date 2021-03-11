import json

class Connect:
    """Создает json в папке автоконнект.
    При создании эксземляра
    1)Передается путь до папки автоконнект
    2)Название папки с Базой
    3)Словарь (файл Param)
    Основной метод connect"""
    def __init__(self,path_to_connect,params,folder) -> None:
        self.name = folder #имя папки с исследованием
        self.path = path_to_connect #папка куда закинуть файл
        self.params = params #текст файла(параметра подключения)
    def __create_json(self):
        for_result = {}
        for_result['ID'] = self.name #
        for_result['Class'] = self.params['class']#
        for_result['Name'] = self.params['project_name']#
        # for_result['ExportDate'] = self.params['']#
        # for_result['Country'] = self.params['']
        try:
            for_result['Start'] = self.params['start']
        except:
            for_result['Start'] = ""
        try:
            for_result['End'] = self.params['end']
        except:
            for_result['End'] = ""
        for_result['Client'] = self.params['client']#
        for_result['Folder'] = self.params['folder']#
        to_connect = {}
        to_connect['results'] = [for_result]
        with open("{}\\{}.json".format(self.path,self.name), "w") as write_file: #дописать полный путь до папки автоконнекта
            json.dump(to_connect, write_file)
    def connect(self):
        try:
            self.__create_json()
            return None, None
        except:
            return None, 'Ошибка подключения.Неверный файл Param'

if __name__== '__main__':
    pass

        