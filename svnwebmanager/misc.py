
import subprocess

def cmd(command, get_ret = True, get_err = True, filter_warnings = False):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read()
    error = ""
    if get_err:
        error = proc.stderr.read()
    returncode = 0
    if get_ret:
        returncode = proc.wait()
    return returncode, output, error

def svn_up(path, revision=None):
    command = "cd %s && svn up" % path
    if revision:
        command += " -r %s" % revision
    r, o, e = cmd(command)
    if r != 0:
        print "ERROR updating svn, '%s'" % e
        return False
    return True

