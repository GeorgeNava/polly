from __future__ import division
from google.appengine.dist import use_library
use_library('django','1.2')

from polly import app,models


class LatestPoll(app.request):
  def get(self):
    poll = models.getLatestPoll()
    if poll: self.redirect(app.root+'/v/'+poll.pollid)
    else: self.show('poll')


class ShowPoll(app.request):
  def get(self,id):
    poll    = models.getPoll(id)
    options = models.getOptionsByPoll(poll.pollid)
    options = calcResults(poll,options)
    voted   = models.alreadyVoted(poll.pollid,self.ipaddress)
    if (voted and poll.restrict>0) or poll.status>1: 
      poll.canvote  = False
      poll.showpoll = False
    else: 
      poll.canvote  = True
      poll.showpoll = True
    data = {'poll':poll,'options':options}
    self.show('poll',data)

  def post(self,id):
    form=self.getForm()
    optionid=form.get('option','')
    if optionid:
      models.newVote(id,optionid,self.ipaddress)
      self.redirect(app.root+'/r/'+id)
    else:
      self.redirect(app.root+'/v/'+id)


class ShowResults(app.request):
  def get(self,id):
    poll    = models.getPoll(id)
    options = models.getOptionsByPoll(poll.pollid)
    options = calcResults(poll,options)
    voted   = models.alreadyVoted(poll.pollid,self.ipaddress)
    if (voted and poll.restrict>0) or poll.status>1: poll.canvote = False
    else: poll.canvote = True
    poll.showpoll = False
    data = {'poll':poll,'options':options}
    self.show('poll',data)


class NotFound(app.request):
  def get(self):
    self.show('notfound')


def calcResults(poll,options):
  for item in options: 
    if poll.counter>0: item.percent=float(item.counter*100/poll.counter)
    else: item.percent=0.0
  return options



routes = [
  (app.root+'/?'     , LatestPoll),
  (app.root+'/v/(.*)', ShowPoll),
  (app.root+'/r/(.*)', ShowResults),
  (app.root+'.*'     , NotFound)
]


def main(): app.control(routes)
if __name__ == '__main__': main()
