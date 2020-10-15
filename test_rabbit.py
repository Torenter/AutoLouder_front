import pika

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
        )
channel = connection.channel()
channel.queue_declare(queue= 'hello')
channel.basic_publish(exchange='', routing_key='hello', body='C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\AutoLouder_front\\media\\Md')
channel.basic_publish(exchange='', routing_key='hello', body='C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\AutoLouder_front\\media\\Md1') 
channel.basic_publish(exchange='', routing_key='hello', body='C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\AutoLouder_front\\media\\Md2')
channel.basic_publish(exchange='', routing_key='hello', body='C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\AutoLouder_front\\media\\Md3')#отправка сообщения с дирректорией и названием файла
channel.close()