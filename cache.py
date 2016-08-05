import time
from functools import wraps
from functools import lru_cache#python内置的cache装饰器
def cache(instance):
    def dec(fn):
        @wraps(fn)
        def wrap(*args,**kwargs):
            #key =>fn_name::params
            pos = ','.join((str(x) for x in args))
            kw = ','.join('{}={}'.format(k,v) for k,v in sorted(kwargs.items()))
            key = '{}::{}::{}'.format(fn.__name__,pos,kw)#生成key
            ret = instance.get(key)#判断key是否在cache中
            #print(key)
            #print(ret)
            if ret is not None:#从cache中得到
                return ret
            ret = fn(*args,**kwargs)#到数据库取数据
            instance.set(key,ret)#放进缓存
            return ret
        return wrap
    return dec

class DictCache:
    def __init__(self):
        self.cache = dict()

    def get(self,key):
        return self.cache.get(key)

    def set(self,key,value):
        self.cache[key] = value

    def __str__(self):
        return str(self.cache)

    def __repr__(self):
        return repr(self.cache)

if __name__ == '__main__':

    cache_instance = DictCache()

    @cache(cache_instance)
    def long_time_fun(x):
        time.sleep(x)
        return x

    x = long_time_fun(3)
    print(x)
    y = long_time_fun(3)
    print(y)


    #拿标准库来实现
    @lru_cache()#具有换出策略lru
    def time_fun(x):
        time.sleep(x)
        return x

    x = time_fun(3)
    print(x)
    y = time_fun(3)
    print(y)

