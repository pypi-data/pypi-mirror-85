# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from mercurial import (
    error,
    node as nodemod,
    pycompat,
)
from heptapod.gitlab.branch import (
    branchmap_branch_from_gitlab_branch,
    gitlab_branch_from_branchmap_branch,
    parse_wild_gitlab_branch,
    gitlab_branch_ref,
)


def _extract_branchmap_heads(repo, entry):
    """From the given branchmap entry, extract default head and list of heads.

    The default head is what needs to be returned for a simple branchmap
    branch lookup. It can be ``None`` if all heads are invisible to GitLab
    (closed or bookmarked).

    :return: (default head, all heads visible to GitLab), all given as
             :class:`changectx` instances.
    """
    # branchmap entries results are already sorted by increasing rev number
    contexts = (repo[node] for node in entry)
    visible = [c for c in contexts if not (c.closesbranch() or c.bookmarks())]
    if not visible:
        return None, visible

    return visible[-1], visible


def changeset_branchmap_entry(repo, ctx):
    """Return the branchmap entry for branch/topic combination of a changeset

    :param ctx: the changeset, given as a :class:`changectx`.
    """
    branch, topic = ctx.branch(), ctx.topic()
    key = branch if not topic else b':'.join((branch, topic))
    return repo.branchmap()[key]


def gitlab_branch_head(repo, gl_branch):
    """Return the unique head of the given GitLab branch.

    Does not resolve other types of "revisions".

    :return: a :class:`changectx` or ``None`` if there's no changeset for
             the given ``gl_branch``.
    """
    wild_hex = parse_wild_gitlab_branch(gl_branch)
    if wild_hex is not None:
        wild_bin = nodemod.bin(wild_hex)
        try:
            wild_ctx = repo[wild_bin]
        except error.RepoLookupError:
            return None

        if wild_ctx.bookmarks():
            # a bookmarked head is never wild
            return None

        heads = _extract_branchmap_heads(
            repo, changeset_branchmap_entry(repo, wild_ctx))[1]
        return wild_ctx if len(heads) > 1 and wild_ctx in heads else None

    branchmap_key = branchmap_branch_from_gitlab_branch(gl_branch)
    if branchmap_key is not None:
        try:
            entry = repo.branchmap()[branchmap_key]
        except KeyError:
            return None
        return _extract_branchmap_heads(repo, entry)[0]

    # last chance: bookmarks
    bookmark_node = repo._bookmarks.get(gl_branch)
    if bookmark_node is None:
        return None
    return repo[bookmark_node]


def iter_gitlab_branches(repo):
    """Iterate on all visible GitLab branches

    Each iteration yields a pair ``(gl_branch, head)`` where ``gl_branch``
    is the name of the GitLab branch and ``head`` is a :class:`changectx`
    instance.
    """
    for key, entry in pycompat.iteritems(repo.branchmap()):
        default, visible = _extract_branchmap_heads(repo, entry)
        if not visible:
            continue

        yield gitlab_branch_from_branchmap_branch(key), default
        if len(visible) > 1:
            for head in visible:
                yield b'wild/' + head.hex(), head

    for key, node in pycompat.iteritems(repo._bookmarks):
        yield key, repo[node]


def iter_gitlab_branches_as_refs(repo):
    """Same as :func:`iter_gitlab_branches`, yielding full Git refs."""
    for branch, ctx in iter_gitlab_branches(repo):
        yield gitlab_branch_ref(branch), ctx
