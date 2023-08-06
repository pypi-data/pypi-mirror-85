# -*- coding: utf-8 -*-
import hashlib
import os
import pickle


JCACHE_ROOT_DIR = os.getenv('JCACHE_ROOT_DIR', '.jcache-data')


def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def cache_key(f, *args, **kwargs):

    if not os.path.exists(JCACHE_ROOT_DIR):
        os.makedirs(JCACHE_ROOT_DIR)

    s = '%s-%s-%s' % (f.__name__, str(args), str(kwargs))
    return os.path.join(JCACHE_ROOT_DIR, '%s.p' % md5(s))


def cache(f):
    def wrap(*args, **kwargs):
        fn = cache_key(f, *args, **kwargs)
        if os.path.exists(fn):
            # print('loading cache')
            with open(fn, 'rb') as fr:
                return pickle.load(fr)

        obj = f(*args, **kwargs)
        with open(fn, 'wb') as fw:
            pickle.dump(obj, fw)
        return obj

    return wrap


@cache
def add(a, b):
    return a + b


if __name__ == '__main__':
    print(add(3, 4))
    print(add(3, 4))
    print(add(8, 4))
    print(add(4, 8))
