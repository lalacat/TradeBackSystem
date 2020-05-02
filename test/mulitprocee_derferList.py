import multiprocessing
import time
from math import *

from twisted.internet import defer, reactor


def f(x):
    return abs(cos(x))** 0.5 + sin( 2 + 3 * x)
def f1(a):
    res = []
    print(a)
    for i in a :
        res.append(f(i))
    # time.sleep(10)
    return res

@defer.inlineCallbacks
def task(a):
    print("start job: %s" %a)
    d = defer.Deferred()
    d.addCallback(f1)
    reactor.callWhenRunning(d.callback,a)
    #d.addCallback(response)
    yield d


def fun_stop(_,t):
    reactor.stop()
    t4 = time.time()
    print(t4-t)



a_1 = range(5000000)
a_2 = range(6000000)
a_3 = range(7000000)
a_4 = range(8000000)



if __name__ == '__main__':
    t1 = time.time()
    r1 = f1(a_1)
    r2 = f1(a_2)
    r3 = f1(a_3)
    r4 = f1(a_4)

    t2 = time.time()
    print(t2-t1)
    pool = multiprocessing.Pool(4)
    results = []
    for i in [a_1,a_2,a_3,a_4]:

        result = pool.apply_async(f1,(i,))
        results.append(result)

    pool.close()
    pool.join()
    t3 = time.time()
    print(t3-t2)
    print(results)
    dd = []
    for i in [a_1,a_2,a_3,a_4]:
        d = task(i)
        dd.append(d)
    ds = defer.DeferredList(dd)
    ds.addCallback(fun_stop,t3)

    reactor.run()
