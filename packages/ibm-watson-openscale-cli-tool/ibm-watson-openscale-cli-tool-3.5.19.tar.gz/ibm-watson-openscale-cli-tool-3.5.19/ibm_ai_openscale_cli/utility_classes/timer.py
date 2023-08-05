import time


def timer(event):
    def wrapper(func):
        def sub_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print('TIMER: {} in {:.3f} seconds'.format(event, elapsed))
            return result
        return sub_wrapper
    return wrapper
