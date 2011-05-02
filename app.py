import os,sys,traceback
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
template.register_template_library('polly.filters')

root='/polly'  # Change this to installation folder if different

class request(webapp.RequestHandler):
  ipaddress = os.environ['REMOTE_ADDR'] if 'REMOTE_ADDR' in os.environ.keys() else '127.0.0.1'

  def setPlain(self):
    self.response.headers["Content-Type"] = "text/plain"

  def out(self,text):
    self.response.out.write(text)

  def write(self,text):
    self.response.out.write(text+'\n')

  def show(self,view,data={}):
    if not '.' in view: view=view+'.html'
    path=os.path.join(os.path.dirname(__file__),view)
    data['root']=root
    self.response.out.write(template.render(path,data))

  def getForm(self):
    data = dict((key,self.request.get(key,'')) for key in self.request.arguments())
    return data

  def getFile(self,input):
    return self.request.get(input,None)

  def getFileName(self,input):
    name=''
    file=self.request.POST.get(input)
    if file!='': name=os.path.basename(file.filename)
    return name

  def noresponse(self):
    self.response.set_status(204)


def run(url,main):
  run_wsgi_app(webapp.WSGIApplication([(url,main)],debug=True))

def control(controller):
  run_wsgi_app(webapp.WSGIApplication(controller,debug=True))

