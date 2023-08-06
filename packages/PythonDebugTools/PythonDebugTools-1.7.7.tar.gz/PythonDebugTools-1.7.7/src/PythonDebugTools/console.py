import pprint
import traceback




__all__ = ['PRINT', 'getPPrintStr', 'print_exception']
debug = __debug__

pp = pprint.PrettyPrinter(indent=4, width=125, sort_dicts=False)
def PRINT(title: str, *args, _pp: pprint.PrettyPrinter = None, **kwargs):
    if not debug: return
    print(f"\n ---------------- {title} ---------------- \n\r")
    (_pp or pp).pprint(dict(args=args, kwargs=kwargs))



def getPPrintStr(o: any, *, _pp: pprint.PrettyPrinter = None) -> str: return (_pp or pp).pformat(o)



def print_exception(e: Exception):
    if not debug: return
    traceback.print_exception(type(e), e, e.__traceback__)
