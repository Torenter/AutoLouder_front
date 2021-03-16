import socket, json
import time
body = {'path':'C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media','key':'2021-03-05 10:56:19.795050',
'comand':'Ruby','name':'sts','lang':'RU'}
body2 = json.dumps(body)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('127.0.0.1',50000))
sock.send(body2.encode('utf-8'))
sock.close()
# body = {'path':'C:\\Users\\Egor.Grivtsov\\Documents\\GitHub\\Prod\\AutoLouder_front\\media','key':'2021-03-05 13:09:55.621710',
# 'comand':'Ruby','name':'testing','lang':'RU'}
# body2 = json.dumps(body)
# sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sock.connect(('127.0.0.1',50000))
# sock.send(body2.encode('utf-8'))
# sock.close()