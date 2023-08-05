# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

from heptapod.testhelpers import (
    LocalRepoWrapper,
)

from ..branch import (
    gitlab_branch_head,
    iter_gitlab_branches,
)


def make_repo(path):
    return LocalRepoWrapper.init(path,
                                 config=dict(
                                     extensions=dict(topic=''),
                                 ))


def test_named_branch_multiple_heads(tmpdir):
    wrapper = make_repo(tmpdir)
    repo = wrapper.repo

    default_branch = b'branch/default'

    # no head, no bookmark
    assert gitlab_branch_head(repo, default_branch) is None
    assert gitlab_branch_head(repo, b'zebook') is None

    # one head
    base = wrapper.write_commit('foo')
    assert gitlab_branch_head(repo, default_branch) == base
    assert list(iter_gitlab_branches(repo)) == [(default_branch, base)]

    # two heads, no bookmark
    head1 = wrapper.write_commit('foo')
    head2 = wrapper.write_commit('foo', parent=base)

    assert gitlab_branch_head(repo, default_branch) == head2
    assert set(iter_gitlab_branches(repo)) == {
        (default_branch, head2),
        (b'wild/' + head1.hex(), head1),
        (b'wild/' + head2.hex(), head2),
    }
    assert gitlab_branch_head(repo, b'wild/' + head1.hex()) == head1
    assert gitlab_branch_head(repo, b'wild/' + head2.hex()) == head2

    # one bookmarked head and one not bookmarked
    wrapper.command('bookmark', b'book2', rev=head2.hex())
    assert gitlab_branch_head(repo, default_branch) == head1
    assert set(iter_gitlab_branches(repo)) == {
        (default_branch, head1),
        (b'book2', head2),
    }
    assert gitlab_branch_head(repo, b'wild/' + head1.hex()) is None
    assert gitlab_branch_head(repo, b'wild/' + head2.hex()) is None
    assert gitlab_branch_head(repo, b'book2') == head2

    # all heads bookmarked
    wrapper.command('bookmark', b'book1', rev=head1.hex())
    assert gitlab_branch_head(repo, default_branch) is None
    assert set(iter_gitlab_branches(repo)) == {
        (b'book1', head1),
        (b'book2', head2),
    }

    # finally, a formally correct wild branch, with no corresponding changeset
    assert gitlab_branch_head(repo, b'wild/' + (b'cafe' * 10)) is None
