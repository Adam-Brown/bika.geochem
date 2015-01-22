import sys
import getopt
import urlparse
import BaseHTTPServer
from sesarwslib import categories as cat
from sesarwslib.sample import Sample
import sesarwslib.sesarwsclient as ws
import os


class IDRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def run(self):
        try:
            self.username = os.environ['SESAR_USERNAME']
            self.password = os.environ['SESAR_PASSWORD']
            self.user_code = os.environ['SESAR_USER_CODE']

            self.client = ws.IgsnClient(self.username, self.password)

            print self.path


            self.get_id()
        except:
            self.send_response(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            raise
    do_GET = run

    def get_id(self):
        batch_size = None
        command = self.command.lower()
        data = []
        if command == 'get' and self.path.find('?') != -1:
            key, qs = self.path.split('?', 1)
            data = urlparse.parse_qs(qs)
            try:
                batch_size = int(data['batch_size'][0])
            except:
                batch_size = None
        else:
            key = self.path

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        # Check that the sample type is valid:
        sample_type = data['SampleType'][0]
        try:
            # We don't actually want to use the value of the reverse mapping - just make sure it works.
            cat.SampleType.reverse_mapping[sample_type]
        except KeyError:
            sample_type = cat.SampleType.Other

        sample = Sample.sample(
            sample_type=sample_type,
            user_code=self.user_code,
            name=data['SampleName'][0],
            material=cat.Material.Rock)

        igsn = self.client.register_sample(sample)

        self.wfile.write(igsn)


# Copied and modified roundup-server code - thanks Richard Jones
def usage(message=''):
    if message:
        message = 'Error: %(error)s\n\n'%{'error': message}
    print '''%(message)sUsage:
id-server [-n hostname] [-p port] [-l file] [-d file]

  -n: sets the host name
  -p: sets the port to listen on
  -l: sets a filename to log to (instead of stdout)
  -d: run the server in the background and on UN*X write the server's PID
      to the nominated file. Note: on Windows the PID argument is needed,
      but ignored.

  Call the ID server with the key for which you want a count as path.
  E.g. calling
    http://<hostname>:<port>/Key
  repeatedly will return 0001, 0002, 00003, etc (base-36 representation).
  The sequence is handled by SESAR so ensure globally-unique IDs are
  generated.

'''%locals()
    sys.exit(0)


def abspath(path):
    ''' Make the given path an absolute path.

        Code from Zope-Coders posting of 2002-10-06 by GvR.
    '''
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    return os.path.normpath(path)


def daemonize(pidfile):
    ''' Turn this process into a daemon.
        - make sure the sys.std(in|out|err) are completely cut off
        - make our parent PID 1

        Write our new PID to the pidfile.

        From A.M. Kuuchling (possibly originally Greg Ward) with
        modification from Oren Tirosh, and finally a small mod from me.
    '''
    # Fork once
    if os.fork() != 0:
        os._exit(0)

    # Create new session
    os.setsid()

    # Second fork to force PPID=1
    pid = os.fork()
    if pid:
        pidfile = open(pidfile, 'w')
        pidfile.write(str(pid))
        pidfile.close()
        os._exit(0)         

    os.chdir("/")         
    os.umask(0)

    # close off sys.std(in|out|err), redirect to devnull so the file
    # descriptors can't be used again
    devnull = os.open('/dev/null', 0)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)


def run():
    ''' Script entry point - handle args and figure out what to to.
    '''
    # time out after a minute if we can
    import socket
    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(120)

    hostname = ''
    port = 8081
    pidfile = None
    logfile = None
    user = None
    try:
        # handle the command-line args
        try:
            optlist, args = getopt.getopt(sys.argv[1:], 'f:n:p:u:d:l:h')
        except getopt.GetoptError, e:
            usage(str(e))

        for (opt, arg) in optlist:
            if opt == '-n': hostname = arg
            elif opt == '-p': port = int(arg)
            elif opt == '-u': user = arg
            elif opt == '-d': pidfile = abspath(arg)
            elif opt == '-l': logfile = abspath(arg)
            elif opt == '-h': usage()

        if hasattr(os, 'getuid'):
            # if root, setuid to the running user
            if not os.getuid() and user is not None:
                try:
                    import pwd
                except ImportError:
                    raise ValueError, "Can't change users - no pwd module"
                try:
                    uid = pwd.getpwnam(user)[2]
                except KeyError:
                    raise ValueError, "User %(user)s doesn't exist"%locals()
                os.setuid(uid)
            elif os.getuid() and user is not None:
                print 'WARNING: ignoring "-u" argument, not root'

            # People can remove this check if they're really determined
            if not os.getuid() and user is None:
                raise ValueError, "Can't run as root!"

    except SystemExit:
        raise
    except:
        exc_type, exc_value = sys.exc_info()[:2]
        usage('%s: %s'%(exc_type, exc_value))

    # we don't want the cgi module interpreting the command-line args ;)
    sys.argv = sys.argv[:1]
    address = (hostname, port)

    # fork?
    if pidfile:
        if not hasattr(os, 'fork'):
            print "Sorry, you can't run the server as a daemon on this" \
                'Operating System'
            sys.exit(0)
        else:
            daemonize(pidfile)

    # redirect stdout/stderr to our logfile
    if logfile:
        # appending, unbuffered
        sys.stdout = sys.stderr = open(logfile, 'a', 0)

    httpd = BaseHTTPServer.HTTPServer(address, IDRequestHandler)
    print 'ID server started on %(address)s'%locals()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Keyboard Interrupt: exiting'

if __name__ == '__main__':
    run()
