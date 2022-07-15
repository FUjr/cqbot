#!/usr/bin/env python3
import asyncio
from csv import unregister_dialect
import traceback
import websockets
import json
import threading
import requests
from queue import Queue
import time
import sys
import notice
import message
import socket
import request
import re

ws = 'ws://192.168.3.5:6700'
http_get = 'http://192.168.3.5:678/'
log_level = 0

async def getmessage():
    async with websockets.connect(ws) as websocket:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            distribute(data)

def distribute(data : dict) -> None:
    if data["post_type"] == 'message':
        try:
            message_handler.distribute(data)
        except Exception as e:
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            traceback.print_tb(exc_traceback_obj)
            log_queue.put([5,time.time()])
            log_queue.put([5,e.args])
            
    elif data['post_type'] == 'request':
        request_handler.distribute(data)
    elif data['post_type'] == 'notice':
        notice_handler.distribute(data)
    elif data['post_type'] == 'meta_event':
        pass
    else:
        pass

def query_api( api_queue : Queue,api_res_queue : Queue) -> None:
    while True:
        data = api_queue.get()
        post_data = data[1]
        url = http_get + data[0]
        res = requests.post(url,json = post_data)
        api_res_queue.put(res.text)


def log_thread( log_queue :Queue):
    while True:
        log = log_queue.get()
        if log[0] > log_level:
            print(log[1])


def http_server(lock):
        global user_data
        #创建socket对象
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #创建一个简易http服务器线程，通过管道通信
        #设置监听端口和地址
        port = 8080
        addr = '0.0.0.0'
        #绑定端口
        s.bind((addr,port))
        
        #监听端口
        s.listen(20)
        
        with open ('mypic.jpg','rb') as f:
            send_data = f.read()
        send = 'HTTP/1.1 200 OK\r\n'
        send += 'Content-Type:image/jpeg\r\n\r\n'
        while True:
            conn , addr = s.accept()
            #接收客户端发送的数据
            data = conn.recv(1024)
            #编码客户端数据
            data = data.decode('utf-8')
            x_forward_re = r'X-Forwarded-For:(.*?)\r\n'
            path_re = r'GET (.*?) HTTP/1.1\r\n'
            ua_re = r'User-Agent:(.*?)\r\n'
            x_forward = re.findall(x_forward_re,data)
            path = re.findall(path_re,data)
            ua = re.findall(ua_re,data)
            conn.send(send.encode('utf-8'))
            conn.send(send_data)
            conn.close()
            if len(x_forward) > 0:
                x_forward = x_forward[0]
            else:
                continue
            if len(path) > 0:
                path = path[0]
            else:
                continue
            if len(ua) > 0:
                ua = ua[0]
            else:
                ua = 'unknown'
            report = {'ip':x_forward.replace(' ',''),'path':path,'ua':ua,'time':time.time()}
            user_data.append(report)
user_data = []
lock = threading.Lock()
log_queue = Queue()
api_queue = Queue()
api_res_queue = Queue()
online_queue = Queue()
notice_handler = notice.distribute.distribute(api_queue,api_res_queue,log_queue)
message_handler = message.distribute.distribute(api_queue,api_res_queue,log_queue)
request_handler = request.distribute.distribute(api_queue,api_res_queue,log_queue)
query_api = threading.Thread(target=query_api,args=(api_queue,api_res_queue))
query_api.start() 
print_log = threading.Thread(target=log_thread,args=(log_queue,))
print_log.start()
http_server = threading.Thread(target=http_server,args=(lock,))
http_server.start()
asyncio.run(getmessage()) 



    

