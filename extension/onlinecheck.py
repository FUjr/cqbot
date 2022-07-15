import socket
import re
import time
import json
import threading
get_data = []
def http_server(lock):
        global get_data
        #创建socket对象
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #创建一个简易http服务器线程，通过管道通信
        #设置监听端口和地址
        port = 679
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
            print(data)
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
            lock.acquire()
            get_data.append(report)
            lock.release()


def return_data(lock):
    global get_data
    #创建socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #设置监听端口和地址
    port = 680
    addr = '0.0.0.0'
    #绑定端口
    s.bind((addr,port))
    
    #监听端口
    s.listen(20)
    send = 'HTTP/1.1 200 OK\r\nContent-Type:plain/text\r\n\r\n'
    while True:
        conn , addr = s.accept()
        #接收客户端发送的数据
        data = conn.recv(1024)
        #编码客户端数据
        data = data.decode('utf-8')
        print(data)
        path_re = r'GET (.*?) HTTP/1.1\r\n'
        
        path_re = re.findall(path_re,data)
        
        if len(path_re) > 0:
            path_re = path_re[0]
            print(path_re)
            buffer = []
            print(get_data)
            for i in get_data:
                print(i)
                if i['path'] == path_re:
                    buffer.append(i)
                    lock.acquire()
                    get_data.remove(i)
                    lock.release()
                    continue
                if time.time() -  i['time'] > 30:
                    lock.acquire()
                    get_data.remove(i)
                    lock.release()
            json_data = json.dumps(buffer)
            conn.send(send.encode('utf-8'))
            conn.send(json_data.encode('utf-8'))
            conn.close()
        else:
            send = 'HTTP/1.1 404 Not Fount\r\nContent-Type:plain/text\r\n\r\n'
            conn.send(send.encode('utf-8'))
            conn.close()
            continue
        
        

