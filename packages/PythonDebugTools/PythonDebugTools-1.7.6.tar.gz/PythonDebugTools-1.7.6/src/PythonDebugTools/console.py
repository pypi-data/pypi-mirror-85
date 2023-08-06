import pprint
import traceback




__all__ = ['PRINT', 'getPPrintStr', 'print_exception']
debug = __debug__

pp = pprint.PrettyPrinter(indent=4, width=200, sort_dicts=False)
def PRINT(title: str, *args, **kwargs):
    if not debug: return
    print(f"\n ---------------- {title} ---------------- \n\r")
    pp.pprint(dict(args=args, kwargs=kwargs))



def getPPrintStr(o: any) -> str: return pp.pformat(o)



def print_exception(e: Exception):
    if not debug: return
    traceback.print_exception(type(e), e, e.__traceback__)
