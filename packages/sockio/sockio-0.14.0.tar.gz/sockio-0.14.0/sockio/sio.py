import asyncio
import functools
import threading
import urllib.parse

from . import aio


class BaseProxy:
    def __init__(self, ref):
        self._ref = ref

    def __getattr__(self, name):
        return getattr(self._ref, name)


def ensure_running(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.master and self.thread is None:
            self.start()
        return f(self, *args, **kwargs)

    return wrapper


class EventLoop:
    def __init__(self, loop=None):
        self.master = loop is None
        self.thread = None
        self.loop = loop
        self.proxies = {}

    def start(self):
        if self.thread:
            raise RuntimeError("event loop already started")
        if self.loop:
            raise RuntimeError("cannot run non master event loop")

        def run():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            started.set()
            self.loop.run_forever()

        started = threading.Event()
        self.thread = threading.Thread(name="AIOTH", target=run)
        self.thread.daemon = True
        self.thread.start()
        started.wait()

    def stop(self):
        if self.loop is None:
            if self.thread is None:
                raise RuntimeError("event loop not started")
        else:
            if self.thread is None:
                raise RuntimeError("cannot stop non master event loop")
        self.loop.call_soon_threadsafe(self.loop.stop)

    @ensure_running
    def run_coroutine(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def _create_coroutine_threadsafe(self, corof, resolve_future):
        @functools.wraps(corof)
        def wrapper(obj, *args, **kwargs):
            coro = corof(obj._ref, *args, **kwargs)
            future = self.run_coroutine(coro)
            return future.result() if resolve_future else future

        return wrapper

    def _create_proxy_for(self, klass, resolve_futures=True):
        class Proxy(BaseProxy):
            pass

        for name in dir(klass):
            if name.startswith("_"):
                continue
            member = getattr(klass, name)
            if asyncio.iscoroutinefunction(member):
                member = self._create_coroutine_threadsafe(member, resolve_futures)
            setattr(Proxy, name, member)
        return Proxy

    @ensure_running
    def proxy(self, obj, resolve_futures=True):
        klass = type(obj)
        key = klass, resolve_futures
        Proxy = self.proxies.get(key)
        if not Proxy:
            Proxy = self._create_proxy_for(klass, resolve_futures)
            self.proxies[key] = Proxy
        return Proxy(obj)

    @ensure_running
    def tcp(self, host, port, resolve_futures=True, **kwargs):
        async def create():
            return aio.TCP(host, port, **kwargs)

        sock = self.run_coroutine(create()).result()
        return self.proxy(sock, resolve_futures)


DefaultEventLoop = EventLoop()
TCP = DefaultEventLoop.tcp


def socket_for_url(url, *args, **kwargs):
    addr = urllib.parse.urlparse(url)
    scheme = addr.scheme
    if scheme == "tcp":
        return TCP(addr.hostname, addr.port, *args, **kwargs)
    raise ValueError("unsupported sync scheme {!r} for {}".format(scheme, url))
