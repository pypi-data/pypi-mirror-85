"""
gitprovenance

Track git version that generated figures.
"""
from __future__ import print_function, absolute_import, division

import os
import sys
import subprocess
import shutil

__version__ = "0.0.1"


_STAMP_HDR = b"\0@@PROVENANCE-STAMP:"
_STAMP_TRAIL = b":PROVENANCE-STAMP@@\0"
_STAMP_TEMPLATE = _STAMP_HDR + b"commit:%s:head:%s:diff:%s:" + _STAMP_TRAIL


def savefig(fname, **kw):
    stamp = kw.pop('stamp', None)

    format = kw.get('format')
    if format in (None, 'auto'):
        if isinstance(fname, str):
            if fname.endswith('.pdf'):
                format = 'pdf'

    import matplotlib.pyplot as plt
    plt.savefig(fname, **kw)
    if format == 'pdf':
        stamp_pdf(fname, stamp=stamp)


def stamp_pdf(filename, stamp=None):
    _stamp_append(filename, prefix=b"%% ", suffix=b"\n", stamp=stamp)


def get_stamp():
    head = git('rev-parse', 'HEAD').decode('ascii')
    if git.is_tree_changed():
        diff = git('diff', 'HEAD')
        diff += b'\n'
        tree = git.get_current_tree()
        commit = _record_tree(tree)
    else:
        commit = head
        diff = b''

    if len(diff) > 5000:
        diff = diff[:5000] + b'...'

    stamp = _STAMP_TEMPLATE % (commit.encode('ascii'),
                               head.encode('ascii'),
                               diff)
    return stamp
    

def _stamp_append(filename, prefix=b"", suffix=b"", stamp=None):
    with open(filename, 'rb') as f:
        try:
            f.seek(-256, 2)
        except IOError:
            f.seek(0, 0)
        data = f.read()
        if _STAMP_TRAIL in data:
            # Nothing to do
            return

    if stamp is None:
        stamp = get_stamp()

    if prefix:
        stamp = stamp.replace(b'\n', b'\n' + prefix)

    with open(filename, 'ab') as f:
        if prefix:
            f.write(prefix)
        f.write(stamp)
        if suffix:
            f.write(suffix)


def _record_tree(tree):
    # create commit
    commit = git('commit-tree', tree, '-p', 'HEAD',
                 input=b"Provenance commit")
    commit = commit.decode('ascii')

    branch = 'refs/provenance/main'

    # enable reflog
    reflog = os.path.join(git.get_gitdir(), 'logs', branch)
    if not os.path.isfile(reflog):
        os.makedirs(os.path.dirname(reflog))
        open(reflog, 'wb').close()

    # record branch
    git('update-ref', '-m', 'provenance', branch, commit)

    return commit


class Git(object):
    def is_tree_changed(self):
        result = self('status', '--porcelain').strip()
        return bool(result)

    def get_current_tree(self):
        gitdir = self.get_gitdir()
        tmp_index = os.path.join(gitdir, "index-provenance-tmp")
        old_index = os.environ.get('GIT_INDEX_FILE', os.path.join(gitdir, "index"))
        try:
            env = dict(os.environ)
            env['GIT_INDEX_FILE'] = tmp_index
            shutil.copyfile(old_index, tmp_index)
            self('add', '--all', env=env)
            return self('write-tree', env=env).decode('ascii')
        finally:
            if os.path.isfile(tmp_index):
                os.unlink(tmp_index)

    def get_gitdir(self):
        res = self('rev-parse', '--git-dir')
        res = res.decode(sys.getfilesystemencoding())
        return os.path.abspath(res)

    def __call__(self, *a, **kw):
        return _run_cmd(['git'] + list(a), **kw).rstrip(b"\n")


def _run_cmd(cmd, input=None, okreturn=(0,), env=None):
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env=env)
    out, err = p.communicate(input=input)
    if p.returncode not in okreturn:
        raise RuntimeError("Error (%d): %r\n%s\n%s" % (p.returncode, cmd,
                                                       out, err))
    return out


git = Git()
