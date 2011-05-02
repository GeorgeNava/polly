import string,random,time
from google.appengine.ext import db
from google.appengine.api import channel


class PollsArchive(db.Model):
  created   = db.DateTimeProperty(auto_now_add=True)
  pollid    = db.StringProperty()
  title     = db.StringProperty()
  image     = db.StringProperty()
  closeon   = db.DateTimeProperty()
  counter   = db.IntegerProperty(default=0)
  type      = db.IntegerProperty(default=0)  # 0.single  1.multiple
  restrict  = db.IntegerProperty(default=0)  # 0.none    1.ipaddress  2.cookie
  status    = db.IntegerProperty(default=0)  # 0.draft   1.open       2.closed

  def __str__(self): 
    return self.title

  @property
  def statusText(self): 
    return ['Draft','Open','Closed'][self.status]


class PollsOptions(db.Model):
  pollid    = db.StringProperty()
  optionid  = db.StringProperty()
  title     = db.StringProperty()
  position  = db.IntegerProperty(default=0)
  counter   = db.IntegerProperty(default=0)
  percent   = db.FloatProperty(default=0.0)

  def __str__(self): 
    return self.title

class PollsVotes(db.Model):
  created   = db.DateTimeProperty(auto_now_add=True)
  voteid    = db.StringProperty()
  pollid    = db.StringProperty()
  optionid  = db.StringProperty()
  token     = db.StringProperty()
  ipaddress = db.StringProperty()
  isvalid   = db.IntegerProperty(default=0)  # 0.valid  1.invalid

  def __str__(self): 
    return '%s:%s:%s:%s'%(self.pollid,self.optionid,self.voteid,self.ipaddress)

  @property
  def poll(self): 
    poll = getPoll(self.pollid)
    if poll: return poll.title
    else: return ''

  @property
  def option(self): 
    option = getOption(self.optionid)
    if option: return option.title
    else: return ''


#-------- UTILS --------

def newKey(n=8):
  return ''.join(random.choice(string.ascii_lowercase) for x in xrange(n))

def newSerial():
  return str(int(time.time()))+str(random.randint(100,999))


#-------- POLLS --------

def newPoll(data):
  key = newSerial()
  rec = PollsArchive(key_name=key)
  rec.pollid = key
  rec.title  = data['title']
  rec.status = data['status']
  rec.put()
  return rec

def getPolls(n=10):
  recs = PollsArchive.all().order('-created').fetch(n)
  return recs

def getPoll(pollid):
  if not pollid: return None
  rec = PollsArchive.get_by_key_name(pollid)
  return rec

def getLatestPoll():
  recs = PollsArchive.all().order('-created').fetch(5)
  last = None
  for rec in recs:
    if rec.status>0: 
      last = rec
      break
  return last

def registerPoll(poll,options):
  # save poll
  pollid = newSerial()
  p = PollsArchive(key_name=pollid)
  p.pollid   = pollid
  p.title    = poll.get('title','')
  p.image    = poll.get('image','')
  p.closeon  = poll.get('closeon',None)
  p.counter  = 0
  p.type     = poll.get('type',0)
  p.restrict = poll.get('restrict',0)
  p.status   = poll.get('status',0)
  p.put()

  # save options
  n=0
  all=[]
  for item in options:
    n+=1
    key = newSerial()
    o = PollsOptions(key_name=key)
    o.pollid   = pollid
    o.optionid = key
    o.position = item.get('position',n)
    o.title    = item.get('title','')
    o.counter  = 0
    o.percent  = 0.0
    all.append(o)
  db.put(all)
  return p

def savePoll(poll,options):
  if not poll or not options: return None
  # save poll
  pollid = poll.get('pollid','')
  p = PollsArchive.get_by_key_name(pollid)
  if not p: return None
  p.title    = poll.get('title','')
  p.image    = poll.get('image','')
  p.closeon  = poll.get('closeon',None)
  p.type     = poll.get('type',0)
  p.restrict = poll.get('restrict',0)
  p.status   = poll.get('status',0)
  p.put()

  # save options
  pos=0
  for option in options:
    if option['title'] and option['optionid']:
      pos+=1
      option['pollid']  =pollid
      option['position']=pos
      saveOption(option)
    elif option['title'] and not option['optionid']:
      pos+=1
      option['pollid']  =pollid
      option['position']=pos
      newOption(option)
    elif option['optionid'] and not option['title']: 
      deleteOption(option['optionid'])
    else:
      pass
  return p

def deletePoll(pollid):
  poll = PollsArchive.get_by_key_name(pollid)
  if not poll: return
  votes   = PollsVotes.all().filter('pollid =',pollid).fetch(999999)
  options = PollsOptions.all().filter('pollid =',pollid).fetch(999)
  db.delete(votes)
  db.delete(options)
  db.delete(poll)
  return True

def changeStatus(pollid,status):
  if not pollid or not status: return
  poll = PollsArchive.get_by_key_name(pollid)
  if not poll: return
  status = int(status)
  if status not in [0,1,2]: return
  poll.status = status
  poll.put()
  return poll


#-------- OPTIONS --------

def getOption(optionid):
  if not optionid: return None
  rec = PollsOptions.get_by_key_name(optionid)
  return rec

def getOptions(n=20):
  recs = PollsOptions.all().fetch(n)
  return recs

def getOptionsByPoll(pollid,n=99):
  recs = PollsOptions.all().filter('pollid =',pollid).order('position').fetch(n)
  return recs

def newOption(data):
  key = newSerial()
  rec = PollsOptions(key_name=key)
  rec.optionid = key
  rec.pollid   = data['pollid']
  rec.position = data['position']
  rec.title    = data['title']
  rec.put()
  return rec

def saveOption(data):
  pollid   = data.get('pollid','')
  optionid = data.get('optionid','')
  if not pollid or not optionid: return None
  rec = PollsOptions.get_by_key_name(optionid)
  rec.position = data['position']
  rec.title    = data['title']
  rec.put()
  return rec

def deleteOption(optionid):
  if not optionid: return None
  rec = PollsOptions.get_by_key_name(optionid)
  rec.delete()
  return True


#-------- VOTES --------

def newVote(pollid,optionid,ipaddress):
  key = newKey()
  rec = PollsVotes(key_name=key)
  rec.voteid    = key
  rec.optionid  = optionid
  rec.pollid    = pollid
  rec.ipaddress = ipaddress
  rec.isvalid   = 1
  rec.put()
  countVote(pollid,optionid)
  return rec

def getVotes(n=10):
  recs = PollsVotes.all().order('-created').fetch(n)
  return recs

def getVotesByPoll(pollid,n=999):
  recs = PollsVotes.all().filter('pollid =',pollid).fetch(n)
  return recs

def countVote(pollid,optionid):
  option=PollsOptions.get_by_key_name(optionid)
  if not option: return False
  option.counter+=1
  poll=PollsArchive.get_by_key_name(pollid)
  if not poll: return False
  poll.counter+=1
  db.put([poll,option])
  return True

def alreadyVoted(pollid,ipaddress):
  vote = PollsVotes.all(keys_only=True).filter('pollid =',pollid).filter('ipaddress =',ipaddress).fetch(1)
  if vote: return True
  else: return False


#-------- SETUP --------
def loadSample():
  p = newPoll({'title':'Do you like polls?','status':1})
  o = newOption({'pollid':p.pollid,'position':1,'title':'Yes, I like polls a lot'})
  o = newOption({'pollid':p.pollid,'position':2,'title':'No, I hate polls to death'})
  o = newOption({'pollid':p.pollid,'position':3,'title':'It depends on the subject'})
  o = newOption({'pollid':p.pollid,'position':4,'title':'Is this a test poll?'})


#-------- END --------
