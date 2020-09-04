import datetime
import inspect


def print_log(msg: str, level: str = "debug"):
    stack = inspect.stack()
    class_name = stack[1][0].f_locals["self"].__class__.__name__
    method_name = stack[1][0].f_code.co_name
    print("[{level}] {timestamp}: {cls_name}.{func_name}(): {msg}".format(
        level=level.upper(),
        timestamp=datetime.datetime.now().strftime("%m/%d %H:%M:%S.%f")[:-3],
        cls_name=class_name,
        func_name=method_name,
        msg=msg,
    ))



