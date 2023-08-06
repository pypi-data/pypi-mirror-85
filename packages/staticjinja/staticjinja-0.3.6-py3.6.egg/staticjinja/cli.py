#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""staticjinja

Usage:
  staticjinja build [--srcpath=<srcpath> --outpath=<outpath> --static=[deprecated, use is_static]<a,b,c> --is_template='.*\.html'' --is_static='.*\.(jpg|css|js)' --is_ignored='(^|.*\/)\..*' --is_partial='(^|.*\/)_.*']
  staticjinja watch [--srcpath=<srcpath> --outpath=<outpath> --static=[deprecated, use is_static]<a,b,c> --is_template='.*\.html'' --is_static='.*\.(jpg|css|js)' --is_ignored='(^|.*\/)\..*' --is_partial='(^|.*\/)_.*']
  staticjinja (-h | --help)
  staticjinja --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from __future__ import print_function
from docopt import docopt
import os
from staticjinja import Site
import sys


def render(args):
    """
    Render a site.

    :param args:
        A map from command-line options to their values. For example:

            {
                '--help': False,
                '--outpath': None,
                '--srcpath': None,
                '--static': None,
                '--is_template': None
                '--is_static': None
                '--is_ignored': None
                '--is_partial': None
                '--version': False,
                'build': True,
                'watch': False
            }
    """
    srcpath = (
        os.path.join(os.getcwd(), 'templates') if args['--srcpath'] is None
        else args['--srcpath'] if os.path.isabs(args['--srcpath'])
        else os.path.join(os.getcwd(), args['--srcpath'])
    )

    if not os.path.isdir(srcpath):
        print("The templates directory '%s' is invalid."
              % srcpath)
        sys.exit(1)

    if args['--outpath'] is not None:
        outpath = args['--outpath']
    else:
        outpath = os.getcwd()

    if not os.path.isdir(outpath):
        print("The output directory '%s' is invalid."
              % outpath)
        sys.exit(1)

    staticdirs = args['--static']
    staticpaths = None

    if staticdirs:
        staticpaths = staticdirs.split(",")
        for path in staticpaths:
            path = os.path.join(srcpath, path)
            if not os.path.isdir(path):
                print("The static files directory '%s' is invalid." % path)
                sys.exit(1)

    is_template = args.get('--is_template', None)
    is_static = args.get('--is_static', None)
    is_ignored = args.get('--is_ignored', None)
    is_partial = args.get('--is_partial', None)

    site = Site.make_site(
        searchpath=srcpath,
        outpath=outpath,
        staticpaths=staticpaths,
        is_template=is_template,
        is_static=is_static,
        is_ignored=is_ignored,
        is_partial=is_partial,
    )

    use_reloader = args['watch']

    site.render(use_reloader=use_reloader)


def main():
    render(docopt(__doc__, version='staticjinja 0.3.0'))


if __name__ == '__main__':
    main()
