# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from mercurial import (
    error,
    scmutil,
)
from hgext3rd.heptapod.branch import get_default_gitlab_branch

from .branch import (
    gitlab_branch_head
)


def gitlab_revision_changeset(repo, revision):
    """Find the changeset for a given GitLab revision.

    In theory, a GitLab revision could be any Git valid revspec, that
    we'd had to translate into its Mercurial counterpart.

    At this point, we support changeset IDs in hex, GitLab branches, tags and
    ``HEAD`` (default GitLab branch).

    :return: the changeset as a :class:`changectx` instance, or ``None``
             if not found.
    """
    if revision == b'HEAD':
        revision = get_default_gitlab_branch(repo)

    ctx = gitlab_branch_head(repo, revision)
    if ctx is not None:
        return ctx

    try:
        # TODO we should probably give precedence to tags, as Mercurial
        # does, although we should check what Git(aly) really does in
        # case of naming conflicts
        return scmutil.revsingle(repo, revision)
    except error.RepoLookupError:
        return None  # voluntarily explicit
