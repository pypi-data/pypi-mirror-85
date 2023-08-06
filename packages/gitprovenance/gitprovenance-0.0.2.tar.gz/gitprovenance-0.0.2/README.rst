gitprovenance
=============

Keep track of git repository commits, which correspond to figures generated via
matplotlib.  This is a pedestrian approach, for cases where a full provenance
tracking system is overkill.

Usage
-----

Use ``gitprovance.savefig`` instead of ``plt.savefig``:

    >>> import matplotlib.pyplot as plt, gitprovenance
    >>> plt.plot([1,2,3,4])
    >>> gitprovenance.savefig("foo.pdf")

This adds a commit to a hidden branch in the current git repository,
which contains the current state of the tree::

    $ git log refs/provenance/main
    def11c6 (refs/provenance/main) Provenance commit
    cd66bed (HEAD -> master, origin/master, origin/HEAD) Add files

The saved figure contains an embedded stamp that refers to the provenance
commit, and the head of the current branch at the time, plus a diff
between the provenance commit and the branch head::

    $ grep PROVENANCE-STAMP foo.pdf
    %% @@PROVENANCE-STAMP:commit:def11c6410e78925eaef7feceaadf07fffcbc4f8:head:cd66beda90ddb285d7140cabb4a2a4e504980897:diff:diff --git a/gitprovenance.py b/gitprovenance.py
    %% index 011c5f8..a566740 100644
    %% --- a/gitprovenance.py
    %% +++ b/gitprovenance.py
    ...

