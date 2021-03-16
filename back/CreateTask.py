import json
import os

class TaskCreate():
    __text = None
    @staticmethod
    def readTask():
        with open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'task.json','r')) as f: # путь должен быть получен из конфига
            TaskCreate.__text = json.load(f)
    def __init__(self,param,path) -> None:
        self.task = TaskCreate.__text
        self.param = param
        self.task_result = None
        self.path = path
    
    def __createLines(self,el,arg: list,last="") -> str:
        """Рекурсивно обходит json с таском"""
        s=''
        for key,value in el.items():
            if (last in arg) and (key==arg[last]) and type(value)!=str:
                s = s + self.__createLines(value,arg,last=key)
            elif type(value)==str:
                    if (last in arg) and (key==arg[last]):
                        s = s + value
                    elif (last in arg) and (key!=arg[last]):
                        continue
                    else:
                        s = s + value
            elif (last in arg) and (key!=arg[last]) and type(value)!=str:
                continue
            else:
                s = s + self.__createLines(value,arg,last=key)
        return s
    
    def __saveTask(self):
        with open(f"{self.path}\\task.txt",'w') as f:
            f.write(self.task_result)
    def createTask(self):
        self.task_result = self.__createLines(self.task,self.param)
        self.__saveTask()
        return f"{self.path}\\task.txt"
if __name__== '__main__':

    p = {"comand":"Ruby",'bd':'sav','wt':"","no_vals":"get_vals","lang":'RU'}
    path = 'C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media\\Md1'
    TaskCreate.readTask()
    v = TaskCreate(p,path)
    s = v.createTask()
    print(v.task_result)

