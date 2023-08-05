import subprocess as sp
import json
import re
import logging

log = logging.getLogger("lu")

class Shell(object):
    def __init__(self):
        self.fmt = {}

    def __call__(self, cmd, output=False):
        cmd = cmd % self.fmt
        log.debug("shell '%s'", cmd)
        kwargs = {
            'shell': True,
            'executable': '/bin/bash',
            'universal_newlines': True
        }
        if output:
            rc = sp.check_output(cmd, **kwargs).strip()
        else:
            rc = sp.check_call(cmd, **kwargs)
        return rc

    def __getitem__(self, k):
        return self.fmt[k]

    def __setitem__(self, k, v):
        self.fmt[k] = v
        return v


class AllEncoder(json.JSONEncoder):
    reg = re.compile('\s+at\s+[^>]+')

    def no_addr(self, s):
        return self.reg.sub('', s)

    def default(self, obj):
        if hasattr(obj, '__call__'):
            return self.no_addr(str(obj))
        elif isinstance(obj, object):
            return self.no_addr(str(obj))
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            return str(obj)


def prettify(eobj):
    return json.dumps(eobj, indent=4, sort_keys=True, cls=AllEncoder)
