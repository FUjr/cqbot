#!/usr/bin/env python3 
import asyncio
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
from extension import onlinecheck
import request
from cqbot import cqbot


async def getmessage():
    while True:
        async with websockets.connect() as websocket:
            while True:
                try:
                    data = await websocket.recv()
                    data = json.loads(data)
                    distribute(data)
                except:
                    print('连接断开，10秒后自动重连')
                    time.sleep(10)

def distribute(data : dict) -> None:
    try:
        if data["post_type"] == 'message':
            message_handler.distribute(data)
        elif data['post_type'] == 'request':
            request_handler.distribute(data)
        elif data['post_type'] == 'notice':
            notice_handler.distribute(data)
        elif data['post_type'] == 'meta_event':
            pass
        else:
            pass
    except Exception as e:
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            traceback.print_tb(exc_traceback_obj)
            log_queue.put([5,time.time()])
            log_queue.put([5,e.args])

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


#extension
lock = threading.Lock()
server1 = threading.Thread(target=onlinecheck.http_server,args=(lock,))
server2 = threading.Thread(target=onlinecheck.return_data,args=(lock,))
server1.start()
server2.start()


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
asyncio.run(getmessage()) 



    

