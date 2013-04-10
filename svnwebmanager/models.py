
from svnwebmanager.misc import *

class currentsite:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def current_svn_revision(self):
        command = "cd %s && svn info" % self.path
        r, o, e = cmd(command)
        if r != 0:
            print "ERROR fetching svn revision for path '%s', '%s'" % (self.path, e)
            return False
        for line in o.splitlines():
            if 'Revision' in line:
                junk, revision = line.split(": ")
                return revision

    def svn_up(self, revision=None):
        command = "cd %s && svn up" % self.path
        if revision:
            command += " -r %s" % revision
        r, o, e = cmd(command)
        if r != 0:
            print "ERROR updating svn, '%s'" % e
            return False, o + e
        return True, o
