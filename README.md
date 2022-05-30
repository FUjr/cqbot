# python QQ机器人框架-（需要内核为go-cqhttp）

本框架的入口程序为main.py。通过异步ws连接go-cqhttp核心，将获取到cqhttp报告的四种基本事件【message、notice、requests、meta_event】分发给相应的类处理。而四种基本事件对应的类会将子事件再次分发给相应的类处理。

同时，该程序还创建了两个线程，分别是log线程和requests线程，均通过消息队列与主线程通信。

## requests 线程

为了简化代码，避免分发 模块请求接口的响应 ，我创建了一个requests线程，通过api_queue传入get请求的资源地址（服务地址和端口已经写死了，队列里只需要传入路径和参数即可），每次put 了api_queue的都需要get一下api_res_queue，否则消息队列会乱掉。

## log 线程

log约定为0-5，共6个等级，数字越大等级越高。约定0为没有必要记录的log，用于程序开发时候的调试，5为error，是必须记录的日志。开发插件时，可以设置不同的等级，用于调试和日常记录。

调用方法：

为了开发方便，在实例化四种基本事件类的时候，已经往初始化的类传入了log的消息队列，并且调用子事件的时候也传入了log队列，因此通常在对象里可以直接调用

```` python
self.log_queue.put([消息等级:int,消息内容])
#消息内容会直接传给print函数。
````

也可以在模块进入main命名空间，直接调用queue

````python
import __main__
__main__.log_queue.put([消息等级:int,消息内容])
````



 