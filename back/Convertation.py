import subprocess
import os

class RunTranslate:
    """Принимает
    1)Путь до траслятора
    2)Путь до таска
    3)Название варнама
    4)Название папки с иследованием
    5)Путь до папки со всеми исследованиями на сервере
    6)Путь до папки Media"""
    def __init__(self,translator,task,Class,folder,result_path,media) -> None:
        self.name = folder
        self.translator = translator
        self.task = task
        self.varnum = Class
        self.__result_dir = result_path + '\\' + folder
        self.media = media
        self.__status = None
    
    def __create_folder(self):
        if not os.path.isdir(self.__result_dir):#проверять,если папка не существует
            os.mkdir(self.__result_dir)
    
    def __run_translator(self):
        command = subprocess.run([self.translator, self.task, self.name, self.varnum], stdout=subprocess.PIPE)#запускат транслятор с передачей параметрова
        #print(command.returncode)
        if command.returncode != 0:
            self.__status = 'Ошибка конвертации(см.лог)'
        with open(f'{self.media}\\{self.name}\\log.txt','w') as f: 
            f.write(command.stdout.decode('windows-1251'))
    def convert(self):
        """Интерфейс"""
        self.__create_folder()
        self.__run_translator()
        return None, self.__status


if __name__== '__main__':
    tr = 'C:\\Program Files\\DataFriend Translator_new\\df_Translator.exe'
    tas = 'C:\\SPSSConverter\\test_new_translator\\task.txt'
    media = "C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media"
    res = 'C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media\\resours'
    s = RunTranslate(tr,tas,'md','Md66',res,media)
    print(s.convert())
        

