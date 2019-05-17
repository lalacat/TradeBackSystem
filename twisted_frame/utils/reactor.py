from twisted.internet import reactor
class CallLaterOnce(object):
    """Schedule a function to be called in the next reactor loop, but only if
    it hasn't been already scheduled since the last time it ran.
    """

    def __init__(self, func, *a, **kw):
        self._func = func
        self._a = a
        self._kw = kw
        self._call = None

    def schedule(self, delay=0):
        if self._call is None:

            # 注册self到callLater中,调用的是func
            # callLater返回的值，可以调用cancel()delay()reset()
            self._call = reactor.callLater(delay, self)

    def cancel(self):
        if self._call:
            self._call.cancel()

    def __call__(self):
        # 上面注册的是self,所以会执行__call__
        self._call = None
        return self._func(*self._a, **self._kw)