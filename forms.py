import app,models,utils

class Form():
  ok       = False   # form is valid or not
  fields   = {}      # input data from html form
  warn     = []      # warning messages for every broken rule
  data     = {}      # data returned to the caller {}
  view     = ''      # template name used for the web form
  url      = ''      # redirect url if form was processed
  redirect = False   # if form is to be redirected


#---- FORM VALIDATION ----

def newPollBlank(request):
  form = Form()
  poll = {
    'slots'  :5,
    'isopen' :'checked',
    'single' :'checked',
    'block'  :'checked',
    'close'  :'checked',
    'closeon':utils.nextweek()
  }
  options = [
    {'position':1,'title':''},
    {'position':2,'title':''},
    {'position':3,'title':''},
    {'position':4,'title':''},
    {'position':5,'title':''},
  ]
  form.data={'poll':poll,'options':options}
  return form


def newPoll(request):
  form   = Form()
  fields = request.getForm()

  # sanitize
  title    = utils.toStr(fields.get('title',''),120)
  image    = utils.toStr(fields.get('image',''),250)
  isopen   = fields.get('isopen',False)
  single   = fields.get('single',False)
  block    = fields.get('block' ,False)
  close    = fields.get('close' ,False)
  closeon  = utils.toDtm(fields.get('closeon',None))
  type     = 0 if single else 1
  restrict = 1 if block  else 0
  status   = 1 if isopen else 0
  closeon  = closeon if close else None
  slots    = utils.toInt(fields.get('slots',0))

  # poll
  poll={
    'title'   : title,
    'image'   : image,
    'closeon' : closeon,
    'type'    : type,
    'restrict': restrict,
    'status'  : status
  }

  # options
  pos = 0
  options=[]
  for i in range(1,slots+1):
    option = fields.get('option'+str(i),'')
    if option:
      pos+=1
      options.append({'title':option,'position':pos})

  # validate
  warn=[]
  form.ok=True
  if not title:
    form.ok=False
    warn.append('Title is required')
  if pos<2:
    form.ok=False
    warn.append('At least two options are required')

  # process
  if form.ok:
    models.registerPoll(poll,options)
    form.url = app.root+'/admin'
  else:
    poll['slots']   = pos
    poll['isopen']  = 'checked' if isopen else ''
    poll['single']  = 'checked' if single else ''
    poll['block']   = 'checked' if block  else ''
    poll['close']   = 'checked' if close  else ''
    if pos<5:
      poll['slots']=5
      for i in range(pos,5):
        options.append({'title':'','position':i+1})
    form.data={'warn':warn,'poll':poll,'options':options}
  return form


def editPoll(request,pollid):
  form   = Form()
  fields = request.getForm()

  # sanitize
  title    = utils.toStr(fields.get('title',''),120)
  image    = utils.toStr(fields.get('image',''),250)
  isopen   = fields.get('isopen',False)
  single   = fields.get('single',False)
  block    = fields.get('block' ,False)
  close    = fields.get('close' ,False)
  closeon  = utils.toDtm(fields.get('closeon',None))
  type     = 0 if single else 1
  restrict = 1 if block  else 0
  status   = 1 if isopen else 0
  closeon  = closeon if close else None
  slots    = utils.toInt(fields.get('slots',0))

  # poll
  poll={
    'pollid'  : pollid,
    'title'   : title,
    'image'   : image,
    'closeon' : closeon,
    'type'    : type,
    'restrict': restrict,
    'status'  : status
  }

  # options
  pos = 0
  options=[]
  for i in range(1,slots+1):
    option   = fields.get('option'+str(i),'')
    optionid = fields.get('optionid'+str(i),'')
    # if has title but not optionid: insert option
    # if has title and has optionid: modify option
    # if not title but has optionid: delete option
    if option and optionid:
      pos+=1
      options.append({'optionid':optionid,'title':option,'position':pos})
    elif option and not optionid:
      pos+=1
      options.append({'optionid':'','title':option,'position':pos})
    else:
      options.append({'optionid':optionid,'title':'','position':0})

  # validate
  warn=[]
  form.ok=True
  if not title:
    form.ok=False
    warn.append('Title is required')
  if pos<2:
    form.ok=False
    warn.append('At least two options are required')

  # process
  if form.ok:
    models.savePoll(poll,options)
    form.url = app.root+'/admin/viewpoll/'+pollid
  else:
    poll['slots']  = pos
    poll['isopen'] = 'checked' if isopen else ''
    poll['single'] = 'checked' if single else ''
    poll['block']  = 'checked' if block  else ''
    poll['close']  = 'checked' if close  else ''
    #remove deleted options
    clean=[]
    for item in options:
      if item['position']>0: clean.append(item)
    if pos<5:
      poll['slots']=5
      for i in range(pos,5):
        clean.append({'optionid':'','title':'','position':i+1})
    form.data={'warn':warn,'poll':poll,'options':clean}
  return form


def getPoll(pollid):
  form    = Form()
  poll    = models.getPoll(pollid)
  options = models.getOptionsByPoll(pollid)
  slots   = len(options)
  poll.slots  = slots
  poll.isopen = 'checked' if poll.status>0   else ''
  poll.single = 'checked' if poll.type==0    else ''
  poll.block  = 'checked' if poll.restrict>0 else ''
  poll.close  = 'checked' if poll.closeon    else ''
  form.data = {'poll':poll,'options':options}
  return form

#---- END ----
