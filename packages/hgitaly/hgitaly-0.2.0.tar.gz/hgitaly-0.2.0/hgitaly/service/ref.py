# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import logging

from mercurial import (
    pycompat,
)

from heptapod.gitlab.branch import (
    gitlab_branch_from_ref,
    gitlab_branch_ref,
)
from hgext3rd.heptapod.branch import get_default_gitlab_branch

from ..errors import not_implemented
from ..stub.shared_pb2 import (
    Branch,
    GitCommit,
)
from ..stub.ref_pb2 import (
    FindDefaultBranchNameRequest,
    FindDefaultBranchNameResponse,
    FindAllBranchNamesRequest,
    FindAllBranchNamesResponse,
    FindAllTagNamesRequest,
    FindAllTagNamesResponse,
    FindRefNameRequest,
    FindRefNameResponse,
    FindLocalBranchesRequest,
    FindLocalBranchCommitAuthor,
    FindLocalBranchResponse,
    FindLocalBranchesResponse,
    FindAllRemoteBranchesRequest,
    FindAllRemoteBranchesResponse,
    FindAllBranchesRequest,
    FindAllBranchesResponse,
    RefExistsRequest,
    RefExistsResponse,
    FindBranchRequest,
    FindBranchResponse,
    DeleteRefsRequest,
    DeleteRefsResponse,
    ListBranchNamesContainingCommitRequest,
    ListBranchNamesContainingCommitResponse,
    ListTagNamesContainingCommitRequest,
    ListTagNamesContainingCommitResponse,
    GetTagMessagesRequest,
    GetTagMessagesResponse,
    PackRefsRequest,
    PackRefsResponse,
    FindTagRequest,
    FindTagResponse,
    FindAllTagsRequest,
    FindAllTagsResponse,
)
from ..stub.ref_pb2_grpc import RefServiceServicer

from ..branch import (
    gitlab_branch_head,
    iter_gitlab_branches,
    iter_gitlab_branches_as_refs,
)
from ..tag import (
    iter_gitlab_tags_as_refs,
)
from .. import message
from ..servicer import HGitalyServicer
from ..util import chunked

logger = logging.getLogger(__name__)
DEFAULT_BRANCH_FILE_NAME = b'default_gitlab_branch'
EXCLUDED_TAG_TYPES = (b'local', None)  # 'tip' has type None


class RefServicer(RefServiceServicer, HGitalyServicer):
    """RefService implementation.

    The ordering of methods in this source file is the same as in the proto
    file.
    """
    def FindDefaultBranchName(
            self,
            request: FindDefaultBranchNameRequest,
            context) -> FindDefaultBranchNameResponse:
        repo = self.load_repo(request.repository, context)
        branch = get_default_gitlab_branch(repo)
        if branch is None:
            # not set, 'branch/default' is not worse than the 'master'
            # that standard GitLab has for Git repos
            branch = b'branch/default'
            logger.warning("FindDefaultBranchName: no information stored "
                           "for repo at %r, returning harcoded default %r",
                           repo, branch)

        return FindDefaultBranchNameResponse(name=gitlab_branch_ref(branch))

    def FindAllBranchNames(self,
                           request: FindAllBranchNamesRequest,
                           context) -> FindAllBranchNamesResponse:
        repo = self.load_repo(request.repository, context)
        for chunk in chunked(iter_gitlab_branches_as_refs(repo)):
            yield FindAllBranchNamesResponse(names=(br[0] for br in chunk))

    def FindAllTagNames(self,
                        request: FindAllTagNamesRequest,
                        context) -> FindAllTagNamesResponse:
        repo = self.load_repo(request.repository, context)
        # TODO SPEC it's not clear whether GitLab actually expect the
        # tags to be in any ordering. At a quick glance it doesn't, but
        # maye we'll end up with confused users because it'd make no sense
        # in the UI.
        tags = (t for t in repo.tags()
                if repo.tagtype(t) not in EXCLUDED_TAG_TYPES)
        for chunk in chunked(iter_gitlab_tags_as_refs(tags)):
            yield FindAllTagNamesResponse(names=chunk)

    def FindRefName(self,
                    request: FindRefNameRequest,
                    context) -> FindRefNameResponse:
        """Find the name of refs that are relevant for a commit.

        This interpretation is not obvious from the comments in the proto
        file, but here's the corresponding Repository method in the Ruby
        client code::

            # Returns a RefName for a given SHA
            def ref_name_for_sha(ref_path, sha)
              raise ArgumentError, "sha can't be empty" unless sha.present?

              gitaly_ref_client.find_ref_name(sha, ref_path)
            end

        In ``gitaly_ref_client``, `sha` is mapped to ``commit_id`` while
        ``ref_path`` is mapped to ``prefix``.

        In other words, making ``commit_id`` mandatory means that the point
        is to find the refs that "contain" a given commit. Translated
        in Mercurial, that would mean:

        - find the branch/topics of the changeset, compare to the branchmap
          to filter out cases where the changeset would be ancestor of
          a closed head or a wild head not selected to be presented as the
          GitLab branch
        - find whether the changeset is ancestor of a bookmark (thankfully
          for performance, we shouldn't have many bookmarks on a typical
          Heptapod repo.

        Also, GitLab expects refs such as keeparounds and MR source heads,
        these should also be taken into account, even if it's trivial for
        Mercurial or worked around the client side.

        As of GitLab 12.10, there is no caller for this Repository method
        in the whole Rails application.
        """
        not_implemented(context, issue=9)  # pragma no cover

    def FindLocalBranches(self,
                          request: FindLocalBranchesRequest,
                          context) -> FindLocalBranchesResponse:
        repo = self.load_repo(request.repository, context)
        for chunk in chunked(iter_gitlab_branches(repo)):
            yield FindLocalBranchesResponse(
                branches=(find_local_branch_response(name, head)
                          for name, head in chunk),
            )

    def FindAllBranches(self,
                        request: FindAllBranchesRequest,
                        context) -> FindAllBranchesResponse:
        Branch = FindAllBranchesResponse.Branch
        repo = self.load_repo(request.repository, context)
        for chunk in chunked(iter_gitlab_branches(repo)):
            yield FindAllBranchesResponse(
                branches=(Branch(name=name, target=message.commit(head))
                          for name, head in chunk))

    def FindAllTags(self,
                    request: FindAllTagsRequest,
                    context) -> FindAllTagsResponse:
        repo = self.load_repo(request.repository, context)
        for chunk in chunked(
                item for item in pycompat.iteritems(repo.tags())
                if repo.tagtype(item[0]) not in EXCLUDED_TAG_TYPES):
            yield FindAllTagsResponse(tags=[message.tag(name, repo[node])
                                            for name, node in chunk])

    def FindTag(self,
                request: FindTagRequest,
                context) -> FindTagResponse:
        repo = self.load_repo(request.repository, context)
        name = request.tag_name
        if repo.tagtype(name) in EXCLUDED_TAG_TYPES:
            # TODO SPEC confirm that this is the accepted response for
            # not found tag.
            return FindTagResponse(tag=None)

        node = repo.tags()[name]
        return FindTagResponse(tag=message.tag(name, repo[node]))

    def FindAllRemoteBranches(self,
                              request: FindAllRemoteBranchesRequest,
                              context) -> FindAllRemoteBranchesResponse:
        """There is no concept of "remote branch" in Mercurial."""
        return iter(())

    def RefExists(self,
                  request: RefExistsRequest,
                  context) -> RefExistsResponse:
        ref = request.ref
        if not ref.startswith(b'refs/'):
            # TODO SPEC commment in ref.proto says `ref` must start with
            # refs/ but doesn't say if False should be returned or an error
            # be set.
            return RefExistsResponse(value=False)

        repo = self.load_repo(request.repository, context)

        gl_branch = gitlab_branch_from_ref(ref)
        if gl_branch is not None:
            return RefExistsResponse(
                value=gitlab_branch_head(repo, gl_branch) is not None)

        gl_tag = gitlab_tag_from_ref(ref)
        if gl_tag is not None:
            return RefExistsResponse(
                value=repo.tagtype(gl_tag) not in EXCLUDED_TAG_TYPES)

        # TODO special references like keeparounds etc?

    def FindBranch(self,
                   request: FindBranchRequest,
                   context) -> FindBranchResponse:
        repo = self.load_repo(request.repository, context)
        name = request.name
        if name.startswith(b'refs/'):
            name = gitlab_branch_from_ref(request.name)

        if name is None:
            # TODO SPEC check if we really must exclude other refs
            return FindBranchResponse(branch=None)

        head = gitlab_branch_head(repo, name)
        return FindBranchResponse(
            branch=Branch(name=name, target_commit=message.commit(head)))

    def DeleteRefs(self,
                   request: DeleteRefsRequest,
                   context) -> DeleteRefsResponse:
        return DeleteRefsResponse(
            git_error="Refs cannot be manually deleted in Mercurial")

    def ListBranchNamesContainingCommit(
            self,
            request: ListBranchNamesContainingCommitRequest,
            context) -> ListBranchNamesContainingCommitResponse:
        repo = self.load_repo(request.repository, context)

        gl_branches_by_heads = {}
        for gl_branch, head in iter_gitlab_branches(repo):
            rev = head.rev()
            gl_branches_by_heads.setdefault(rev, []).append(gl_branch)

        heads = repo.revs(b'%ld and %s::', gl_branches_by_heads,
                          request.commit_id)
        # TODO SPEC since there's a limit, we'll have to know what is
        # the expected ordering.
        #
        # In Gitaly sources, this is in refnames.go, which in turns call
        # `git for-each-ref` without a `sort` option. Then according to
        # the man page:
        #  --sort=<key>
        #      A field name to sort on. Prefix - to sort in descending order
        #      of the value. When unspecified, refname is used.
        for chunk in chunked((gl_branch
                              for head in heads
                              for gl_branch in gl_branches_by_heads[head]),
                             limit=request.limit):
            yield ListBranchNamesContainingCommitResponse(
                branch_names=chunk)

    def ListTagNamesContainingCommit(
            self,
            request: ListTagNamesContainingCommitRequest,
            context) -> ListTagNamesContainingCommitResponse:
        # TODO support ordering, see similar method for branches
        repo = self.load_repo(request.repository, context)
        revs = repo.revs("%s:: and tag()", request.commit_id)
        tag_names = (name for rev in revs for name in repo[rev].tags()
                     if repo.tagtype(name) not in EXCLUDED_TAG_TYPES)
        for chunk in chunked(tag_names, limit=request.limit):
            yield ListTagNamesContainingCommitResponse(tag_names=chunk)

    def GetTagMessages(self,
                       request: GetTagMessagesRequest,
                       context) -> GetTagMessagesResponse:
        """Return messages of the given tags.

        In Mercurial, all tags have messages, and these are descriptions
        of the changests that give them values.

        For now, we'll consider that the id of a tag is the nod id of the
        changeset that gives it its current value.
        """
        repo = self.load_repo(request.repository, context)
        # TODO check that the given id is indeed for a tag, i.e. a
        # changeset that affects .hgtags?
        for tag_id in request.tag_ids:
            yield GetTagMessagesResponse(tag_id=tag_id,
                                         message=repo[tag_id].description())

    def ListNewCommits(self, request, context):
        """Not relevant for Mercurial

        From ``ref.proto``:
            Returns commits that are only reachable from the ref passed

        But actually, the request has a ``commit_id`` field, and it's not
        ``bytes``, hence can't be used for a ref.

        The reference Gitaly implementation is in `list_new_commits.go`.
        It boils down to::

          git rev-list --not --all ^oid

        with ``oid`` being ``request.commit id`` (not really a ref, then).
        additional comment: "the added ^ is to negate the oid since there is
        a --not option that comes earlier in the arg list"

        Note that ``--all`` includes Git refs that are descendents of the
        given commit. In other words, the results are ancestors of the
        given commit that would be garbage collected unless they get a ref
        soon.

        In the whole of the GitLab FOSS code base (as of GitLab 12.10),
        this is used only in pre-receive changes checks, i.e, before any ref
        has been assigned to commits that are new, indeed.

        We'll need a Mercurial specific version of the pre-receive check
        anyway.

        With HGitaly, all Mercurial changesets are at least ancestors of
        a GitLab branch head, the only exception not being closed heads,
        which are not mapped, so the results should boil down to something like
        ``reverse(::x and ::(heads() and closed()))``
        """
        raise NotImplementedError(
            "Not relevant for Mercurial")  # pragma: no cover

    def ListNewBlobs(self, request, context):
        """Not relevant for Mercurial.

        This is the same as :meth:`ListNewCommits()`, returning the blobs.
        In Gitaly sources, this is done by adding ``--objects`` to the
        otherwise same call to ``git rev-list`` as for :meth:`ListNewCommits`.

        As of GitLab 12.10, this is used only in
        ``GitAccess#check_changes_size`` (enforcing size limits for pushes).
        """
        raise NotImplementedError(
            "Not relevant for Mercurial")  # pragma: no cover

    def PackRefs(self, request: PackRefsRequest, context) -> PackRefsResponse:
        """Not relevant for Mercurial, does nothing.
        """
        # repr(Repository) contains newlines
        logger.warning("Ignored irrelevant call to PackRefs method "
                       "for Mercurial repository %r on storage %r",
                       request.repository.relative_path,
                       request.repository.storage_name)
        return PackRefsResponse()


def flbr_author(commit: GitCommit):
    """Extract commit intro specific fields of FindLocalBranchCommitAuthor."""
    return FindLocalBranchCommitAuthor(
        name=commit.name,
        email=commit.email,
        date=commit.date,
        timezone=commit.timezone,
    )


def find_local_branch_response(name, head):
    commit = message.commit(head)
    return FindLocalBranchResponse(
        name=name,
        commit_id=commit.id,
        commit_subject=commit.subject,
        commit_author=flbr_author(commit.author),
        commit_committer=flbr_author(commit.committer),
        commit=commit,
    )


TAG_REF_PREFIX = b'refs/tags/'


def gitlab_tag_from_ref(ref):
    if ref.startswith(TAG_REF_PREFIX):
        return ref[len(TAG_REF_PREFIX):]
