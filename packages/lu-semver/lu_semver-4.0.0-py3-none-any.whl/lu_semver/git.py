import os
from .misc import Shell
from .scm import ScmVersion
from .scm import _branch_env
import tempfile
import logging

log = logging.getLogger("lu")


_git_fmt_next ='branch:omit=master,count:pfx=rc,scm,extra'
_git_fmt_common ='branch:omit=master,count:pfx=dev,scm,extra'

class GitVersion(ScmVersion):

    @staticmethod
    def supported(path):
        sh = Shell()
        if not path:
            path = '.'
        sh['path'] = path
        try:
            sh('git -C %(path)s rev-parse --git-dir >& /dev/null')
            return True
        except:
            return False


    def __init__(self, ref='HEAD', path='.', fmt=None,
            extra=None, ver='@next', quiet=True):
        self.ref = ref
        self.shell = Shell()
        self.shell['git'] = 'git -C ' + path
        self.shell['ref'] = self.ref
        self.shell['quiet'] = '>& /dev/null' if quiet else ''
        if fmt is None:
            if ver == '@next':
                fmt = _git_fmt_next
            else:
                fmt = _git_fmt_common
        ScmVersion.__init__(
            self,
            path=path,
            fmt=fmt,
            extra=extra,
            ver=ver
        )

    def get_count(self):
        if not self.tag:
            c = self.shell('%(git)s rev-list %(ref)s --count', output=True)
        else:
            self.shell['tag'] = self.tag
            c = self.shell('%(git)s rev-list %(tag)s..%(ref)s --count', output=True)
        log.debug("count %s", c)
        return int(c)

    def get_branch(self):
        # FIXME: make brnach_env configurable, currently it's for Gitlab
        if _branch_env in os.environ:
            branch = os.environ[_branch_env]
        else:
            branch = self.shell('%(git)s rev-parse --abbrev-ref %(ref)s || true',
                output=True)
        return branch

    def get_tag(self):
        def _get_tag():
            rc = self.shell('%(git)s describe --abbrev=0 %(ref)s 2>/dev/null || true',
                output=True)
            return rc

        tag = _get_tag()
        if tag:
            return tag
        # FIXME: run only on CI servers with shallow clone
        if _branch_env in os.environ:
            self.shell['branch'] = os.environ[_branch_env]
            for d in [100, 200, 300, 400]:
                tag = _get_tag()
                if tag:
                    return tag
                self.shell['depth'] = d
                cmd = '%(git)s fetch --depth %(depth)s --tags origin %(branch)s %(quiet)s'
                self.shell(cmd)

    def fmt_scm(self, pfx='git'):
        c = self.shell('%(git)s rev-parse --short %(ref)s', output=True)
        if pfx:
            return '%s.%s' % (pfx, c)
        else:
            return '%s' % c


class GitRepo(object):
    def __init__(self, url=None, depth=None, quiet=True):
        self.count = 0
        self.path = tempfile.mkdtemp()
        self.shell = Shell()
        self.shell['path'] = self.path
        self.shell['git'] = 'git -C ' + self.path
        if quiet:
            self.shell['quiet'] = '>& /dev/null'
        else:
            self.shell['quiet'] = ''

        if url:
            if url.startswith('/'):
                url = 'file://' + url
            self.shell['url'] = url
            self.shell['depth'] = depth
            self.shell('git clone --depth %(depth)s %(url)s %(path)s %(quiet)s')
        else:
            self.shell('%(git)s init %(quiet)s')
        self.shell('%(git)s config --local user.email "you@example.com"')
        self.shell('%(git)s config --local user.name "Jon Doe"')
        # self.add_commit()


    def add_commit(self, msg=None):
        if not msg:
            if self.count:
                msg = "sync %d" % self.count
            else:
                msg = "initial commit"
            self.count += 1
        self.shell['msg'] = msg
        self.shell('%(git)s commit --allow-empty -m "%(msg)s" %(quiet)s')
        rc = self.shell('%(git)s rev-parse --short HEAD', output=True)
        log.debug("new commit %s", rc)
        return rc

    def add_tag(self, tag):
        self.shell['tag'] = tag
        self.shell('%(git)s tag -a -m %(tag)s %(tag)s')

    def checkout(self, branch):
        self.shell['branch'] = branch
        self.shell('%(git)s checkout %(branch)s %(quiet)s || '
            '%(git)s checkout -b %(branch)s %(quiet)s')

    def log(self):
        self.shell('%(git)s log --graph --decorate --oneline --all || true')

    def __str__(self):
        return '<git at %s>' % self.path

    def __del__(self):
        # self.log()
        self.shell('rm -rf %(path)s')
