from collections import defaultdict

from twisted.internet import defer, reactor, task
import tushare as ts
from queue import Empty,Queue

from twisted_frame.utils.defer import mustbe_deferred
from twisted_frame.utils.reactor import CallLaterOnce


class SimpleFrameWork(object):

    def __init__(self):
        print('框架初始化')

        self._handlers = defaultdict(list)
        nextcall = CallLaterOnce(self._next_event)
        self._queue = Queue()
        self.active = []
        self.heartbeat = task.LoopingCall(nextcall.schedule)



    def get_error(self,_):
        print(_)

    def _next_event(self):
        try:
            # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
            event = self._queue.get(block=False)
            print('取出event %s'%event.name)
            self.active.append(event)

            def remove_event(_,event):
                print('%s is delete' %event.name)
                self.active.remove(event)
            d = self.process(event)
            d.addCallback(remove_event,event)

        except Empty:
            print('event is empty')
        except Exception as e:
            print(e)

    def process(self,event):
        # TODO 判断event的类型
        for handle in self._handlers[event._type]:
            result = handle(event)
        return result

    def start(self):
        print('定时开始')
        self.heartbeat.start(1)

    def stop(self):
        self.heartbeat.stop()
        reactor.stop()

    def put(self,event):
        self._queue.put(event)


    def register(self, type, handler):
        handler_list = self._handlers[type]

        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type_, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handlerList = self.__handlers[type_]

        # 如果该函数存在于列表中，则移除
        if handler in handlerList:
            handlerList.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handlerList:
            del self.__handlers[type_]

    def registerGeneralHandler(self, handler):
        """注册通用事件处理函数监听"""
        if handler not in self.__generalHandlers:
            self.__generalHandlers.append(handler)

    def unregisterGeneralHandler(self, handler):
        """注销通用事件处理函数监听"""
        if handler in self.__generalHandlers:
            if handler in self.__generalHandlers:
                self.__generalHandlers.remove(handler)



def put_data(obj,data):
    for d in data:
        obj.put_data(d)


class TestGetData(object):
    def __init__(self):
        print('框架初始化')
        self.token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'
        self.ts_code = '002192.SZ'
        self.startday = '20190326'
        self.endday = '20190328'
        self.pro = ts.pro_api(self.token)

    def get_data(self,ts_code,startday,endday):
        df = self.pro.daily(ts_code=ts_code, start_date=startday, end_date=endday)
        return df

    def process(self,event):

        d = mustbe_deferred(self.get_data, event._code, self.startday, self.endday)
        d.addCallback(self.ouput,event)
        d.addErrback(self.get_error)
        return d

    def ouput(self,result,event):
        event.result = result
        print(result.head())
        return

    def get_error(self,_):
        print(_)

class TestEvent(object):

    def __init__(self,name,code,_type = 'backtrade'):
        self._type = _type
        self._code = code
        self.name = name

sfw = SimpleFrameWork()
code = ['002677.SZ','002405.SZ','002299.SZ']
tgd = TestGetData()

sfw.register('backtrade',tgd.process)
te1 = TestEvent('RJ','002677.SZ')
te2 = TestEvent('T2','002405.SZ')

te3 = TestEvent('T3','002299.SZ')

sfw.start()
reactor.callLater(4, sfw.put, te1)
reactor.callLater(4, sfw.put, te2)
reactor.callLater(4, sfw.put, te3)
reactor.callLater(10,sfw.stop)

reactor.run()
