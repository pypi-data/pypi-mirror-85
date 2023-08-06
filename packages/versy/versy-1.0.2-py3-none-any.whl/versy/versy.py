from . import git
from . import semver
from .changelog import ChangeLog
from .version_file import VersionFile
import contextlib
import editor
import functools
import io
import myers
import safer

PREFIX = '__version__ = '
VERSION = 'VERSION'
ACTIONS = 'patch', 'minor', 'major', 'new', 'show'
__version__ = '1.0.2'


def versy(
    action, changelog, dry_run, file, message, root, verbose, edit, push
):
    printer = _dry_printer if dry_run else _printer

    if not dry_run:
        git.check_clean_workspace()

    vfile = VersionFile(root, printer, version_file=file)
    version = semver.semver(vfile.version)

    if action == 'show':
        print('Version', version, 'found in', vfile.file)
        return

    vb = verbose and not dry_run
    cl = ChangeLog(root, version, changelog, printer, message, vb)
    files = [cl.changelog]

    if action == 'new':
        cl.new()
        print('First version', version, 'to', cl.changelog)
        new_version = str(version)

    else:
        new_version = str(semver.bump(version, action))
        cl.update(new_version)
        vfile.write(new_version)
        if dry_run or verbose:
            print()
        print('Version', version, '-->', new_version, 'to', cl.changelog)

        if dry_run or verbose:
            print()
        files.append(vfile.file)

    if edit and not dry_run:
        editor(filename=cl.changelog)

    msg = 'Version v%s' % new_version
    git.commit(files, msg, dry_run, verbose, push)


@contextlib.contextmanager
def _dry_printer(file):
    fp = io.StringIO()

    yield functools.partial(print, file=fp)

    if file.exists():
        before = file.read_text().splitlines()
    else:
        before = []
    after = fp.getvalue().splitlines()

    print()
    print(60 * '-')
    print()
    print('%s:' % file)
    print()
    print(*myers.diff(before, after, context=2, format=True), sep='\n')


@contextlib.contextmanager
def _printer(file):
    with safer.printer(file) as _print:
        yield _print
