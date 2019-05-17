from queue import Queue, Empty

from twisted.internet import defer, task,reactor

from twisted_frame.utils.defer import mustbe_deferred
from twisted_frame.utils.reactor import CallLaterOnce



class Event(object):
    def __init__(self,type_=None):
        self.type_ = type_
        self.dict_ = {}


class Slot(object):
    def __int__(self,close_if_idle,nextcall,scheduler):
        self.closing = False
        self.inprogress = list()  # 存放正在爬虫的网站,保证每个defer都执行完
        self.close_if_idle = close_if_idle
        self.nextcall = nextcall
        self.scheduler = scheduler
        # 不断调用方法，通过start和stop控制调用的启停
        self.heartbeat = task.LoopingCall(nextcall.schedule)

    def add_event(self, request):
        """
        :param request:
        :return:
        """
        # logger.debug("Engine:Slot <%s> 添加到inprogress中"%request)
        self.inprogress.append(request)

    def remove_event(self, request, name):
        #  当request处理完后就可以移除掉了
        self.inprogress.remove(request)
        self._maybe_fire_closing(name)

    def close(self, name):
        # logger.info("关闭 %s 的 slot！！"%name)

        self.closing = defer.Deferred()
        self._maybe_fire_closing(name)
        return self.closing

    def _maybe_fire_closing(self, name):
        """
        当执行close方法后，self.closing不为False，而且要保证在执行的爬虫任务都要完成的情况下，
        才能够停止心跳函数
        :return:
        """
        if self.closing and not self.inprogress:
            if self.nextcall:
                self.nextcall.cancel()
                if self.heartbeat.running:
                    self.heartbeat.stop()
            self.closing.callback(None)


class EventEngine(object):
    def __init__(self,interval:int =1):
        self._interval = interval
        self._queue = Queue()
        self.active_event = []
        self.nextcall = CallLaterOnce(self._next_event)
        self.heartbeat = task.LoopingCall(self.nextcall.schedule)

    def _run(self):
        self.heartbeat.start(self._interval)



    def get_data(self,ts_code,startday,endday):
        df = self.pro.daily(ts_code=ts_code, start_date=startday, end_date=endday)
        return df

    def get_error(self,_):
        print(_)

    def _next_code(self):
        try:
            # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
            ts_code = self._queue.get(block=False)
            print('取出代码 %s'%ts_code)
            self.active.append(ts_code)
            def remove_coed(_,ts_code):
                print('%s is delete' %ts_code)
                self.active.remove(ts_code)
            d = self.process(ts_code)
            d.addCallback(remove_coed,ts_code)
        except Empty:
            print('code is empty')
        except Exception as e:
            print(e)

    def process(self,ts_code):
        d = mustbe_deferred(self.get_data, ts_code, self.startday, self.endday)
        d.addCallback(lambda _: print(_.head()))
        d.addErrback(self.get_error)
        return d

    def start(self):
        print('定时开始')
        self.heartbeat.start(1)

    def stop(self):
        self.heartbeat.stop()
        reactor.stop()

    def put_data(self,ts_code):
        self._queue.put(ts_code)
a = EventEngine()

