import sys, os, inspect
import pytz, datetime
import pprint
import decimal
import pandas as pd
import dateutil.parser

class DefaultAppConfig:
  # time
  local_timezone      = 'Asia/Bangkok'

  # logging
  log_level           = 2
  log_file_path       = os.path.join('..', 'logs', 'log.txt')
  log_level           = 2 # 0 : none, 1 : incremental progress log, 2 : time it
  default_log_level   = 1 # default log level if no log_level specified when calling helper.ptint_log()

class Helper:

  AppConfig = None

  def __init__(self, AppConfig):
    if AppConfig is not None:
      self.AppConfig = AppConfig
    else:
      self.AppConfig = DefaultAppConfig
      print('### WARNING : Falling back to use default AppConfig')

  ########################## GENERAL FUNCTIONS ##########################

  def parse_datetime(dt, tz:str=None, fmt:str=None):
    '''
      pass "tz" to get datetime in specific timezone or "False" for UTC. The default is "Asia/Bangkok" \n
      pass "fmt" to get datetime formatted into specific format. The default is "%Y-%m-%d %H:%M:%S.%f"
    '''
    fmt = fmt or '%Y-%m-%d %H:%M:%S.%f'
    tz  = tz  if tz is not None else pytz.timezone(self.AppConfig.local_timezone)
    result = datetime.datetime.strptime(dt, fmt)
    if tz != False: result = result.astimezone(tz)
    return result

  def get_iso_datetime(self, dt_obj=None, tz=None, return_obj=False):
    return_obj = return_obj or False
    if tz is None: 			tz 			= self.AppConfig.local_timezone
    dt_obj = dt_obj or pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None)
    dt_obj = dt_obj.astimezone(pytz.timezone(tz)) if tz is not None else dt_obj
    return dt_obj.isoformat()

  def localize_utc(self, dt_obj, tz=None):
    utc 	= pytz.utc
    dt_obj 	= utc.localize(dt_obj)
    if tz is None: tz = self.AppConfig.local_timezone
    return dt_obj.astimezone(pytz.timezone(tz))

  def localize_utc_timestamp(self, ts, return_obj=False):
    result = pytz.utc.localize(datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f')).astimezone(pytz.timezone(self.AppConfig.local_timezone))
    if not return_obj:
      return result.strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
      return result

  def localize_iso8601_utc_timestamp(self, ts, return_obj=False):
    result = dateutil.parser.parse(ts).astimezone(pytz.timezone(self.AppConfig.local_timezone))
    if not return_obj:
      return result.strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
      return result

  def print_me(self) -> str:
    '''
      This is a function to print my signature via command line
    '''
    if self.AppConfig.log_level > 0:
      k = 'Petch'
      x = ('Z\x06\x15\x12\tp\x06\x15\x04\x10p\x06\x15\x04\t|o\x15\x04\t'
        'pETCH0ETCHZ\x06T\x04\x180bTCH0EqCEpE~\x04\tp\r'
        '#\x04Ep\x06\x15\x13\t~\r'
        '~\x04\tp\x06\x15\x0b'
        '\x17-\x06$\x12\x10Z\x06\x15\x04\tp\x06\x15\x0b'
        '\x17wo')
      msg = []
      for i, c in enumerate(x):
        key_c = ord(k[i % len(k)])
        enc_c = ord(c)
        msg.append(chr((enc_c - key_c) % 127))
      print( ''.join(msg) )

  def print_log(self, log_level=None, end=None, *args):
    this_log_level = log_level or self.AppConfig.default_log_level
    if self.AppConfig.log_level > 0:
      if self.AppConfig.log_level >= this_log_level:
        if self.AppConfig.log_to_stdout:
          print(self.get_datetime(), *args, end=end)
        if self.AppConfig.log_to_file:
          with open(self.AppConfig.log_file_path, "a+") as f:
            print(self.get_datetime(), *args, end=end, file=f)

  def remove_log_file(self):
    if os.path.exists(self.AppConfig.log_file_path):
      os.remove(self.AppConfig.log_file_path)

  ########################## CLASS METHODS ##########################

  @classmethod
  def to_quoted_string(cls, lst):
    if type(lst) is str: raise ValueError('{} type "{}" is not compatible with this function'.format(cls.get_datetime(), type(lst)))
    if len(lst) > 0:
      result = ",".join(['"'+str(x)+'"' for x in lst])
    else: result = '""'
    return result

  @classmethod
  def to_ticked_string(cls, lst):
    if type(lst) is str: raise ValueError('{} type "{}" is not compatible with this function'.format(cls.get_datetime(), type(lst)))
    result = ",".join(['`'+str(x)+'`' for x in lst])
    return result

  @classmethod
  def format_whole_numbers(cls, amount):
    return cls.format_decimals(amount, decimals=0, comma=True)

  ########################## STATIC METHODS ##########################

  @staticmethod
  def get_machine_name():
    keys = os.environ.keys()
    if 'COMPUTERNAME' in keys:
      machine_name = os.environ['COMPUTERNAME']
    elif 'KUBERNETES_PORT' in keys:
      machine_name = 'KUBERNETES'
    else:
      machine_name = 'NA'
    return machine_name

  @staticmethod
  def format_decimals(amount, decimal_places):
    decimal_places  = int(decimal_places) or 2
    comma 			    = comma if comma is not None else True
    comma 			    = ',' or ''
    pattern         = "{0:" + comma + '.' + str(decimal_places) + "f}"
    return pattern.format(amount)

  @staticmethod
  def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
      magnitude += 1
      num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' K', ' M', ' B', ' T'][magnitude])

  @staticmethod
  def get_datetime(dt_obj=None, fmt=None, tz=None, return_obj:bool=False):
    '''
      tz could be string. If tz is set to false, the function will return UTC
    '''
    tz = (tz if tz == False else (tz or 'Asia/Bangkok'))
    dt_obj = dt_obj or datetime.datetime.utcnow()
    dt_obj = pytz.utc.localize(dt_obj, is_dst=None)
    if tz != False:
      dt_obj = dt_obj.astimezone(pytz.timezone(tz))

    if not return_obj:
      fmt    = fmt or '%Y-%m-%d %H:%M:%S'
      dt_obj = dt_obj.strftime(fmt)

    return dt_obj

  @staticmethod
  def get_utc(return_obj=False):
    result = datetime.datetime.utcnow()
    if not return_obj:
      result = result.strftime('%Y-%m-%d %H:%M:%S.%f')
    return result

  @staticmethod
  def pprint_(x):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)

  @staticmethod
  def save_pickle(obj, name):
    import pickle
    with open(name, 'wb') as f:
      pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

  @staticmethod
  def load_pickle(name):
    import pickle
    with open(name, 'rb') as f:
      return pickle.load(f)

  @staticmethod
  def update_progress(job_title, progress, blank_padding=0):
    length = 30 # modify this to change the length
    block = int(round(length*progress))
    if progress < 1:
      msg = "\r{0}: [{1}] {2}%{3}".format(job_title, "#"*block + "-"*(length-block), '{0:.02f}'.format(round(progress*100, 2)),' '*blank_padding)
    else:
      msg = "\r{0}{1}\r\n".format(job_title," "*length)
    sys.stdout.write(msg)
    sys.stdout.flush()

  @staticmethod
  def get_last_month_end():
    now = datetime.datetime.now()
    res = datetime.datetime(now.year, now.month, now.day) + pd.tseries.offsets.MonthEnd(-1)
    return res

  @staticmethod
  def get_last_month_begin():
    return get_last_month_end() + pd.tseries.offsets.MonthBegin(-1)

  @staticmethod
  def get_this_month_begin():
    return get_last_month_end() + pd.Timedelta(days=1)

if __name__ == '__main__':
  pass