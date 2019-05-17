import time

from twisted.internet import defer, reactor, task
import logging

from twisted.python import failure

logger = logging.getLogger(__name__)


def defer_fail(_failure):
    """Same as twisted.internet.defer.fail but delay calling errback until
    next reactor loop

    It delays by 100ms so reactor has a chance to go through readers and writers
    before attending pending delayed calls, so do not set delay to zero.
    """
    d = defer.Deferred()
    reactor.callLater(0.1, d.errback, _failure)
    return d

def defer_succeed(result):
    """Same as twisted.internet.defer.succeed but delay calling callback until
    next reactor loop

    It delays by 100ms so reactor has a chance to go trough readers and writers
    before attending pending delayed calls, so do not set delay to zero.
    """
    d = defer.Deferred()
    reactor.callLater(0.1, d.callback, result)
    return d


def defer_result(result):
    if isinstance(result, defer.Deferred):
        return result
    elif isinstance(result, failure.Failure):
        return defer_fail(result)
    else:
        return defer_succeed(result)


def mustbe_deferred(f, *args, **kw):
    """Same as twisted.internet.defer.maybeDeferred, but delay calling
    callback/errback to next reactor loop
    """
    try:
        result = f(*args, **kw)
    # FIXME: Hack to avoid introspecting tracebacks. This to speed up
    # processing of IgnoreRequest errors which are, by far, the most common
    # exception in Scrapy - see #125
    except Exception as e:
        return defer_fail(failure.Failure(e))
    except:
        return defer_fail(failure.Failure())
    else:
        return defer_result(result)


def process_parallel(callbacks, input, *a, **kw):
    """
    并行处理
    返回一个Deferred，它的result是一个list，list里的内容是所有callbacks方法执行后的结果
    1.succeed的作用是返回一个Deferred,并直接执行了callback(input)，
    相当于返回一个带有result的Deferred,可以等价于执行：
    dfds = []
    for i in callbacks:
        d = Deferred()
        d.addCallback(i)
        d.callback(input)
        n += 1
        dfds.append(d)
    2.并行处理的目的是为了同时得到所有callbacks的执行结果，DeferredList执行后返回的结果就是一个list分别对应相应的Deferred,
    而每个result都是一个truple类型，(True, result),因此通过lambda函数处理，构造一个只有result的列表
    """
    dfds = [defer.succeed(input).addCallback(x, *a, **kw) for x in callbacks]
    d = defer.DeferredList(dfds, fireOnOneErrback=1, consumeErrors=1)
    d.addCallbacks(lambda r: [x[1] for x in r], lambda f: f.value.subFailure)
    return d


def process_chain(callbacks, input, *a, **kw):
    """
    返回一条串行处理的方法链，真对数据需要不同函数依次处理，最后返回一个带着处理后的result的Deferred
    :param callbacks: 回调函数
    :param input: defer之间传输的result
    :return: Deferred
    """
    d = defer.Deferred()
    for x in callbacks:
        d.addCallback(x, *a, **kw)
    d.callback(input)
    return d


def process_chain_both(callbacks,errbacks,input,*a,**kw):
    d = defer.Deferred()
    for cb,eb in zip(callbacks,errbacks):
        d.addCallbacks(cb,eb,callbackArgs=a,callbackKeywords=kw,
                       errbackArgs=a,errbackKeywords=kw)
    if isinstance(input,failure.Failure):
        d.errback(input)
    else:
        d.callback(input)
    return d

def parallel(iterable, count, callable, *args, **named):
    """
    实现同时控制处理，多个defer的功能
    Cooperator是实现Cooperative task的，这是一个能够迭代的iterator，能够提供一个最基本的实现work。当处于yield状态的时候，
    Cooperator能够决定下个执行的task是哪个，如果yield，是一个deferred，work会一直等到这个deffered链执行完。
    当Cooperator有多个task的时候，它能够分配这些work在这些tasks中来回切换，相当于实现并行操作。
    cooperate返回是一个CooperativeTask，它的作用是启动一个给定的iterator作为一个长期执行的cooperative task
    这个task能够pause,resumed和waited on
    coiterate是添加一个iterator到正在运行的Cooperator的iterator list中去，等同于cooperate，但是返回的是一个Deferred
    """
    coop = task.Cooperator()
    work = (callable(elem, *args, **named) for elem in iterable)
    return defer.DeferredList([coop.coiterate(work) for _ in range(count)])

def iter_errback(iterable, errback, *a, **kw):
    """Wraps an iterable calling an errback if an error is caught while
    iterating it.
    """
    try:
        it = iter(iterable)
    except Exception as e :
        raise Exception(e)
    while True:
        try:
            yield next(it)
        except StopIteration:
            break
        except:
            errback(failure.Failure(), *a, **kw)

