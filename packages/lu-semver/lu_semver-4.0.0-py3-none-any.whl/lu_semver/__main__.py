#!/usr/bin/python3

"""
Print Semantic Version for Git project

"""


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
        help="version, '@same' - same as workdir, "
            "'@next' - same with minor part incremented, "
            "'@latest' - for latest docker images, "
            "string - use verbatim",
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
