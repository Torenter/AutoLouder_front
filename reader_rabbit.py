from os.path import basename
import pika, multiprocessing
import sys,os,subprocess,time
from back.tasks import get_command

def child(translator,calling,i,lock,folder):#  передать параметры запуска транслятору.
    '''Дописать закоментированные строки'''
    params =get_command(folder)
    cmd = "{}".format(translator)
    task = '{}\\{}'.format(folder,'task.txt')
    folder_name = folder.split('\\')[-1]
    varnum = params['Class']
    #command = subprocess.run([cmd, task, folder_name, folder_name,varnum], stdout=subprocess.PIPE)
    print('Всё ок')
    with lock:
        calling[i] = 1

if __name__== '__main__':
    import os
    from back.translator import get_translators
    import time

    manager = multiprocessing.Manager()
    lock = multiprocessing.Lock()

    calling = manager.dict(get_translators())
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def main(ch, method, properties, body):
        """Фукция берет блокировку, итерируется по списку странсляторов,ища свободный, после вызывает
        дочерний процесс для сбора параметров и запуска транслятора"""
        done = None
        while not done:
            with lock:
                iter=0
                for i in calling: 
                    iter+=1
                    if iter <= len(calling):
                        if calling[i]==1:
                            translator = i
                            calling[i]=2
                            translation = multiprocessing.Process(target = child,args=[translator,calling,i,lock,body.decode("utf-8")])
                            translation.start()
                            done = True
                            break
                    else:
                        break
            

    channel.basic_consume(
    queue='hello', on_message_callback=main, auto_ack=True)
    channel.start_consuming()

    #Cуществующие проблему
    #1)Если папка медиа будет локально открыта, ее обновление происходит очень долго, и если в этот момент будет
    #происходить загрузка, то выпадает ошибка, что пусть не найден - или решить, или нехер открывать этот каталог.
    #2)Если все трансляторы заняты, def main зацикливается, скорее всго это приведет к тому, что ни один из потоков
    # не сможет внести изменения, потому что объект будет заблокирован (взаимоблокировака). Но сообщения продолжают исчезать
    # из кролика, т.к. он вызывает функцию, она забирает сообщение и ничего не делает
    #  Нужно исправить этот момент