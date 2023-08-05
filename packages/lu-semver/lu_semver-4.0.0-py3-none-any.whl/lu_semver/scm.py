import re
import logging

log = logging.getLogger("lu")

_branch_env = 'CI_COMMIT_BRANCH'
_default_fmt ='branch,count,scm,extra'

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


class ScmVersion(object):
    def __init__(self, path, ver, fmt, extra):
        self.path = path
        if not (ver in ['@same', '@next', '@latest'] or isinstance(ver, str)):
            ver = '@next'
        self.ver = ver
        self.fmt = fmt
        self.extra = extra
        self.tag = self.get_tag()
        self.count = self.get_count()
        self.branch = self.get_branch()
        self.next_ver = self.get_next_ver()
        self.rel = self.fmt_rel()

    def __str__(self):
        ver = self.next_ver
        if self.rel:
            ver += '-' + self.rel
        return ver

    @classmethod
    def factory(cls, path):
        rc = all_subclasses(cls)
        log.debug("factory %s", rc)
        for c in all_subclasses(cls):
            rc = c.supported(path)
            log.debug("%s supports path %s: %s", c, path, rc)
            if rc:
                return c

    def get_next_ver_next(self, ver):
        def repl(m):
            i = m.group(0)
            l = len(i)
            fmt = "%%0%dd" % l
            i = int(i) + 1
            i = fmt % i
            return i

        reg = '(?<=\.)\d+$'
        rc = re.sub(reg, repl, ver)
        log.debug("next ver: '%s' %s", rc, type(rc))
        return rc

    def get_next_ver(self):
        log.debug("next ver: ver '%s', tag '%s'", self.ver, self.tag)
        if self.ver == '@latest':
            return 'latest'
        tag = self.tag if self.tag else '0.1.0'
        if self.ver == '@next':
            if self.count:
                return self.get_next_ver_next(tag)
            else:
                return tag
        if self.ver == '@same':
            return tag
        return self.ver

    def sanitize_name(self, name):
        rc = []
        for c in name:
            if c.isalnum():
                rc.append(c)
            elif c in '.-':
                rc.append(c)
            else:
                rc.append('-')
        return ''.join(rc)

    def fmt_scm(self):
        return ''

    def fmt_extra(self):
        return self.extra

    def fmt_count(self, pfx='dev'):
        c = self.count
        if pfx:
            return '%s.%d' % (pfx, c)
        else:
            return '%d' % c

    def fmt_branch(self, omit='master'):
        branch = self.branch
        if branch == 'HEAD':
            return ''
        omit = omit.split(',')
        if branch in omit:
            return ''
        return self.sanitize_name(branch)

    def fmt_rel(self):
        if self.ver == '@latest':
            return self.fmt_branch()
        if self.count == 0:
            return ''

        relrc = []
        for el in self.fmt.split(','):
            # log.debug("fmt: plugin '%s'", el)
            el = el.split(':')
            name = el[0]
            del el[0]

            func = getattr(self, 'fmt_' + name, None)
            if not func:
                log.error("unknown plugin '%s'", name)
                exit(1)
            kwargs = {}
            for k in el:
                k = k.split('=')
                # log.debug("param %s", k)
                kwargs[k[0]] = k[1]
            rc = func(**kwargs)
            log.debug("fmt: plugin '%s', args %s, rc '%s'", name, kwargs, rc)
            if rc:
                relrc.append(rc)

        relrc = '.'.join(relrc)
        log.debug("fmt: final '%s'", relrc)
        return relrc
