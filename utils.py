import datetime,re,hashlib
from google.appengine.ext import db

def toStr(s,max=None):
  if not s or s=='' or s=='None': return ''
  if max: s=s[:max]
  s = s.strip().replace('\r\n',' ').replace('\n',' ').replace('\r',' ')
  return s
    
def toTxt(s,max=None):
  if not s or s=='' or s=='None': return ''
  s = re.sub(' +',' ',s)
  if max: s=s[:max]
  return s

def toPsw(s,min=0,max=None):
  # chars and numbers only
  if not s or s=='' or s=='None': return ''
  if len(s)<min: return ''
  if max: s=s[:max]
  s=re.sub(r'[^a-zA-Z0-9]','',s)
  return s

def toInt(s):
  if not s or s=='' or s=='None': return 0
  try:    num=int(s)
  except: num=0
  return num

def toFlt(s):
  if not s or s=='' or s=='None': return 0.0
  try:    num=float(s)
  except: num=0.0
  return num

def toDat(s):
  # yyyy-mm-dd
  if not s or s=='' or s=='None': return None
  try:    
    date=(int(s[0:4]),int(s[5:7]),int(s[8:10]))
    date=datetime.date(*date)
  except: date=None
  return date

def toDtm(s,m=0):
  # yyyy-mm-dd
  # yyyy-mm-dd hh:mm
  # yyyy-mm-dd hh:mm:ss.123456
  # m=1 is for one second before midnight 23.59.59.999
  if not s or s=='' or s=='None': return None
  n=len(s)
  try:    
    if n==10: 
      if m==0:  time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),0,0,0,0)
      else:     time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),23,59,59,0)
    elif n==16: time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),0,0)
    elif n==19: time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:19]),0)
    elif n==26: time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:19]),int(rpad(s[20:26],6,'0')))
    date=datetime.datetime(*time)
  except: date=None
  return date

def md5(data):
  return hashlib.md5(data).hexdigest()

def sortList(list,name):
  from operator import itemgetter
  sort = sorted(list,key=itemgetter(name))
  return sort

def now(dateonly=0):
  if dateonly: return datetime.date.today()
  else: return datetime.datetime.now()

def today(dateonly=0):
  if dateonly: return datetime.date.today()
  else: return datetime.datetime.now()

def tomorrow(dateonly=0):
  if dateonly: return datetime.date.today()+datetime.timedelta(days=1)
  else: return datetime.datetime.now()+datetime.timedelta(days=1)

def yesterday(dateonly=0):
  if dateonly: return datetime.date.today()-datetime.timedelta(days=1)
  else: return datetime.datetime.now()-datetime.timedelta(days=1)

def nextweek(dateonly=0):
  if dateonly: return datetime.date.today()+datetime.timedelta(days=7)
  else: return datetime.datetime.now()+datetime.timedelta(days=7)


#---- END ----
