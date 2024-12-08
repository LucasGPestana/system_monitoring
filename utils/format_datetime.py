import datetime as dt

def convertToDatetimeFormat(seconds: float) -> str:

  datetime_obj: dt.datetime = dt.datetime.fromtimestamp(seconds)

  return datetime_obj.strftime("%d/%m/%Y %H:%M:%S")