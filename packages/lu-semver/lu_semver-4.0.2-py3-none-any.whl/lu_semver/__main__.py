#!/usr/bin/python3

"""
Print Semantic Version for Git project

"""

epilog = '''
Example 1:  'master' branch has 3 commits after '1.3.0' tag
 lu-semver                                            | 1.3.1-rc.3
 lu-semver --ver @next --fmt branch,count             | 1.3.1-rc.3
 lu-semver --ver @same --fmt branch,count             | 1.3.0-rc.3
 lu-semver --ver @latest                              | latest

Example 2: 'bionic' branch has 2 commits after '1.3.0' tag
 lu-semver                                            | 1.3.1-bionic.rc.2
 lu-semver --ver @next --fmt branch,count             | 1.3.1-bionic.rc.2
 lu-semver --ver @same --fmt branch,count             | 1.3.0-bionic.rc.2
 lu-semver --ver @latest                              | latest-bionic

Example 3: all formatting options
 lu-semver --fmt branch:omit=master,v8.0,count:pfx=dev;extra;scm:pfx=git --extra gcc.9
     1.3.1-bionic.dev.2.gcc.9.git.7d1f822
'''

############################################################
# {{{ configure logging
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)

log = logging.getLogger("lu")
if '--debug' in sys.argv:
    log.setLevel(logging.DEBUG)


# }}}

from .misc import prettify
from .scm import _default_fmt
from .scm import ScmVersion
from .git import GitVersion
import argparse


def AppArgParser():
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
        description=__doc__)
    p.add_argument("--debug", help="debug mode", action="store_true")
    p.add_argument(
        "-C",
        help='switch to this directory',
        metavar='dir',
        dest='path')
    p.add_argument(
        "--fmt",
        help="format of the the release part; default is '%s'" % _default_fmt,
        metavar='str')
    p.add_argument(
        "--extra",
        help="extra text to the release part",
        metavar='str')
    p.add_argument(
        "--ver",
        help="version, '@same' - same as last git tag, "
            "'@next' - same with minor part incremented, "
            "'@latest' - for latest docker images, "
            "string - use string verbatim",
        default='@next',
        metavar='str')

    p.add_argument("ref", help="reference to commit", nargs='?')
    return p


def main():
    p = AppArgParser()
    Args, UnknownArgs = p.parse_known_args()
    log.debug("Args: %s", prettify(vars(Args)))
    log.debug("UnknownArgs: %s", UnknownArgs)

    scm = ScmVersion.factory(Args.path)
    log.debug("scm %s", scm)
    if not scm:
        log.error("unsupported SCM")
        return

    kwargs = {}
    attrs = ['ref', 'path', "fmt", 'extra', 'ver']
    for a in attrs:
        val = getattr(Args, a)
        if val is not None:
            kwargs[a] = getattr(Args, a)
    v = scm(**kwargs)
    print(v)


if __name__ == "__main__":
    main()
