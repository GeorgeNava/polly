from google.appengine.dist import use_library
use_library('django','1.2')

from polly import app,forms,models,utils


class adminPanel(app.request):
  def get(self):
    polls = models.getPolls()
    votes = models.getVotes()
    data  = {'polls':polls,'votes':votes}
    self.show('admin',data)


class adminCurrentPoll(app.request):
  def get(self):
    poll = models.getLatestPoll()
    if poll: 
      pollid=poll.pollid
      status=poll.status
    else:
      pollid=''
      status=0
    data={'pollid':pollid,'status':status}
    self.show('admin_viewpoll',data)


class adminViewPoll(app.request):
  def get(self,pollid):
    poll = models.getPoll(pollid)
    if poll: 
      pollid=poll.pollid
      status=poll.status
    else:
      pollid=''
      status=0
    data={'pollid':pollid,'status':status}
    self.show('admin_viewpoll',data)


class adminNewPoll(app.request):
  def get(self):
    form=forms.newPollBlank(self)
    self.show('admin_newpoll',form.data)

  def post(self):
    form = forms.newPoll(self)
    if form.ok: self.redirect(app.root+'/admin')
    else: self.show('admin_newpoll',form.data)


class adminEditPoll(app.request):
  def get(self,id):
    form=forms.getPoll(id)
    self.show('admin_editpoll',form.data)

  def post(self,id):
    form = forms.editPoll(self,id)
    if form.ok: self.redirect(app.root+'/admin')
    else: self.show('admin_editpoll',form.data)


class adminDeletePoll(app.request):
  def post(self,id):
    models.deletePoll(id)
    self.noresponse()


class adminStatus(app.request):
  def post(self,id,status):
    models.changeStatus(id,status)
    self.noresponse()


class adminArchive(app.request):
  def get(self):
    polls = models.getPolls(100)
    data  = {'polls':polls}
    self.show('admin_archive',data)


class adminVotes(app.request):
  def get(self):
    votes = models.getVotes(100)
    data  = {'votes':votes}
    self.show('admin_votes',data)


class adminLoad(app.request):
  def get(self):
    models.loadSample()
    self.redirect(app.root+'/admin')



routes = [
  (app.root+'/admin/?'               , adminPanel),
  (app.root+'/admin/current'         , adminCurrentPoll),
  (app.root+'/admin/newpoll'         , adminNewPoll),
  (app.root+'/admin/viewpoll/(.*)'   , adminViewPoll),
  (app.root+'/admin/editpoll/(.*)'   , adminEditPoll),
  (app.root+'/admin/deletepoll/(.*)' , adminDeletePoll),
  (app.root+'/admin/status/(.*)/(.*)', adminStatus),
  (app.root+'/admin/archive'         , adminArchive),
  (app.root+'/admin/votes'           , adminVotes),
  (app.root+'/admin/load'            , adminLoad)
]


def main(): app.control(routes)
if __name__ == '__main__': main()
