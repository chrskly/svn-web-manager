
from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from config import *
from svnwebmanager.models import *

def error(request, msg):
    t = loader.get_template('error.html')
    c = RequestContext(request, { 'msg' : msg })
    return HttpResponse(t.render(c))
    

def index(request):
    siteid = request.POST.get('siteid', '')
    revision = request.POST.get('revision', '')
    if siteid and revision:
        # try and update to this rev
        if revision == 'latest':
            revision = None
        else:
            try:
                revision = int(revision)
            except Exception, e:
                return error(request, 'Um, \'%s\' isn\'t a number, dude.' % revision)
        print "Updating site '%s' to revision '%s'" % (siteid, revision)
        mysite = currentsite(siteid, sites[siteid]) 
        result, output = mysite.svn_up(revision=revision)
        print "Result %s, output %s" % (result, output)
        if not result:
            return error(request, output)
        t = loader.get_template('done.html')
        c = RequestContext(request, {
            'msg' : output,
        })
        return HttpResponse(t.render(c))
    else:
        # show form
        mysites = []
        for name, path in sites.iteritems():
            mysites.append(currentsite(name, path))
        t = loader.get_template('index.html')
        c = RequestContext(request, {
            'sites' : mysites,
        })
        return HttpResponse(t.render(c))
