import traceback
try:
    from api.api import get_periodos
    print(get_periodos())
except Exception as e:
    traceback.print_exc()
