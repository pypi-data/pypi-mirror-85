from . import versy
import argparse
import sys
import traceback

ACTIONS = versy.ACTIONS + ('<new version number>',)


def main(argv=None):
    args = parse(argv)
    try:
        versy.versy(**args)
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        if args['verbose']:
            traceback.print_exc()
        sys.exit(-1)


def parse(argv=None):
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('action', nargs='?', default='show', help=_ACTIONS_HELP)
    p.add_argument('--changelog', '-c', default=None, help=_CHANGELOG_HELP)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_HELP)
    p.add_argument('--edit', '-e', action='store_true', help=_EDIT_HELP)
    p.add_argument('--file', '-f', default=None, help=_FILE_HELP)
    p.add_argument('--message', '-m', help=_MESSAGE_HELP)
    p.add_argument('--push', '-p', action='store_true', help=_PUSH_HELP)
    p.add_argument('--root', '-r', default='.', help=_ROOT_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)

    return vars(p.parse_args(argv))


def run(**kwargs):
    versy.versy(**dict(parse([]), kwargs))


_DESCRIPTION = """
Automatically update the version number and change log for a Python repository
"""

_ACTIONS_HELP = 'Actions are: ' + ', '.join(ACTIONS)
_CHANGELOG_HELP = 'Specify the name of a new change log'
_EDIT_HELP = 'Bring up the change log in an editor'
_FILE_HELP = 'Specify the file containing __version__'
_MESSAGE_HELP = 'Set change log message'
_ROOT_HELP = 'Root directory to search for a version number'
_PUSH_HELP = 'git push after committing changes'
_VERBOSE_HELP = 'Print more stuff'
_DRY_RUN_HELP = 'Don\'t actually make the changes, just print the diffs'


if __name__ == '__main__':
    sys.exit(main())
