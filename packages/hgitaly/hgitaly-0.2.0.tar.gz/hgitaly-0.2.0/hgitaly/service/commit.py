# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import logging
from grpc import StatusCode

from mercurial import (
    error,
    pycompat,
)

from ..errors import not_implemented
from ..stub.commit_pb2 import (
    CommitIsAncestorRequest,
    CommitIsAncestorResponse,
    TreeEntryRequest,
    TreeEntryResponse,
    CommitsBetweenRequest,
    CommitsBetweenResponse,
    CountCommitsRequest,
    CountCommitsResponse,
    CountDivergingCommitsRequest,
    CountDivergingCommitsResponse,
    GetTreeEntriesRequest,
    GetTreeEntriesResponse,
    ListFilesRequest,
    ListFilesResponse,
    FindCommitRequest,
    FindCommitResponse,
    CommitStatsRequest,
    CommitStatsResponse,
    FindAllCommitsRequest,
    FindAllCommitsResponse,
    FindCommitsRequest,
    FindCommitsResponse,
    CommitLanguagesRequest,
    CommitLanguagesResponse,
    RawBlameRequest,
    RawBlameResponse,
    LastCommitForPathRequest,
    LastCommitForPathResponse,
    ListLastCommitsForTreeRequest,
    ListLastCommitsForTreeResponse,
    CommitsByMessageRequest,
    CommitsByMessageResponse,
    ListCommitsByOidRequest,
    ListCommitsByOidResponse,
    ListCommitsByRefNameRequest,
    ListCommitsByRefNameResponse,
    FilterShasWithSignaturesRequest,
    FilterShasWithSignaturesResponse,
    GetCommitSignaturesRequest,
    GetCommitSignaturesResponse,
    GetCommitMessagesRequest,
    GetCommitMessagesResponse,
)
from ..stub.commit_pb2_grpc import CommitServiceServicer

from .. import message
from ..revision import gitlab_revision_changeset
from ..servicer import HGitalyServicer
from ..util import chunked

logger = logging.getLogger(__name__)


class CommitServicer(CommitServiceServicer, HGitalyServicer):

    def CommitIsAncestor(self,
                         request: CommitIsAncestorRequest,
                         context) -> CommitIsAncestorResponse:
        repo = self.load_repo(request.repository, context)
        # TODO status.Errorf(codes.InvalidArgument, "Bad Request
        # (empty ancestor sha)") and same for child
        ancestor = repo[request.ancestor_id]
        child = repo[request.child_id]
        return CommitIsAncestorResponse(value=ancestor.isancestorof(child))

    def TreeEntry(self, request: TreeEntryRequest,
                  context) -> TreeEntryResponse:
        return not_implemented(context, TreeEntryResponse,
                               issue=16)  # pragma no cover

    def CommitsBetween(self,
                       request: CommitsBetweenRequest,
                       context) -> CommitsBetweenResponse:
        """Stream chunks of commits "between" two GitLab revisions.

        One may believe the meaning of "between" to be based on DAG ranges,
        but actually, what the Gitaly reference Golang implementation does is
        ``git log --reverse FROM..TO``, which is indeed commonly used to obtain
        exclusive DAG ranges (would be `FROM::TO - FROM`) but gitrevisions(1)
        actually says:
           you can ask for commits that are reachable
           from r2 excluding those that are reachable from r1 by ^r1 r2
           and it can be written as r1..r2.

        So the true Mercurial equivalent revset is actually `TO % FROM`,
        which is quite different if FROM is not an ancestor of TO.

        Sadly, we happen to know `%` to be less efficient than DAG ranges.

        TODO: assuming the most common use case is indeed to obtain DAG ranges,
        (for which GitLab would actually have to check ancestry first), maybe
        introduce a direct call for DAG ranges later.
        """
        repo = self.load_repo(request.repository, context)
        # TODO ERROR. Treat the case when rev_from or rev_to doesn't exist
        # (and is there a default value btw? In Git CLI that would be HEAD)
        rev_from = gitlab_revision_changeset(repo, getattr(request, 'from'))
        rev_to = gitlab_revision_changeset(repo, request.to)
        revs = repo.revs('only(%s, %s)', rev_to, rev_from)
        for chunk in chunked(revs):
            yield CommitsBetweenResponse(
                commits=(message.commit(repo[rev]) for rev in chunk))

    def CountCommits(self,
                     request: CountCommitsRequest,
                     context) -> CountCommitsResponse:
        # TODO: yet to finish this method to support all lookups
        repo = self.load_repo(request.repository, context)
        revision = request.revision
        if revision:
            ctx = gitlab_revision_changeset(repo, revision)
            revs = repo.revs('::%s', ctx)
            count = len(revs)
        else:
            # Note: if revision is not passed, we return all revs for now.
            # `revision` and `all` are mutually exclusive
            count = len(repo)
        max_count = request.max_count
        if max_count and count > max_count:
            count = max_count
        return CountCommitsResponse(count=count)

    def CountDivergingCommits(self,
                              request: CountDivergingCommitsRequest,
                              context) -> CountDivergingCommitsResponse:
        return not_implemented(context, CountDivergingCommitsResponse,
                               issue=17)  # pragma no cover

    def GetTreeEntries(self, request: GetTreeEntriesRequest,
                       context) -> GetTreeEntriesResponse:
        return not_implemented(context, GetTreeEntriesResponse,
                               issue=16)  # pragma no cover

    def ListFiles(self, request: ListFilesRequest,
                  context) -> ListFilesResponse:
        return not_implemented(context, ListFilesResponse,
                               issue=13)  # pragma no cover

    def CommitStats(self, request: CommitStatsRequest,
                    context) -> CommitStatsResponse:
        return not_implemented(context, CommitStatsResponse,
                               issue=18)  # pragma no cover

    def FindCommit(self,
                   request: FindCommitRequest, context) -> FindCommitResponse:
        repo = self.load_repo(request.repository, context)
        revision = request.revision
        logger.debug("FindCommit revision=%r", revision)
        ctx = gitlab_revision_changeset(repo, revision)

        commit = None if ctx is None else message.commit(ctx)
        return FindCommitResponse(commit=commit)

    def FindAllCommits(self, request: FindAllCommitsRequest,
                       context) -> FindAllCommitsResponse:
        return not_implemented(context, FindAllCommitsResponse,
                               issue=19)  # pragma no cover

    def FindCommits(self, request: FindCommitsRequest,
                    context) -> FindCommitsResponse:
        # TODO: yet to finish this method to support all lookups
        repo = self.load_repo(request.repository, context)
        revision = request.revision
        if revision:
            ctx = gitlab_revision_changeset(repo, revision)
            revs = repo.revs('::%s', ctx)
        else:
            # Note: if revision is not passed, we return all revs for now.
            # `revision` and `all` are mutually exclusive
            revs = repo.revs('all()')
        # order revision from top to bottom i.e (tip:0)
        revs.reverse()
        limit = request.limit
        if limit and len(revs) > limit:
            revs = revs.slice(0, limit)
        for chunk in chunked(revs):
            yield FindCommitsResponse(
                commits=(message.commit(repo[rev]) for rev in chunk))

    def CommitLanguages(self, request: CommitLanguagesRequest,
                        context) -> CommitLanguagesResponse:
        return not_implemented(context, CommitLanguagesResponse,
                               issue=12)  # pragma no cover

    def RawBlame(self, request: RawBlameRequest,
                 context) -> RawBlameResponse:
        return not_implemented(context, RawBlameResponse,
                               issue=20)   # pragma no cover

    def LastCommitForPath(self,
                          request: LastCommitForPathRequest,
                          context) -> LastCommitForPathResponse:
        repo = self.load_repo(request.repository, context)
        revision, path = request.revision, request.path
        logger.debug("LastCommitForPath revision=%r, path=%r", revision, path)
        ctx = gitlab_revision_changeset(repo, revision)
        # gracinet: just hoping that performance wise, this does the right
        # thing, i.e do any scanning from the end
        # While we can be reasonably confident that the file exists
        # in the given revision, there are cases where deduplication implies
        # that the filelog() predicate would not see any new file revision
        # in some subgraph, because it's identical to another one that's not
        # in that subgraph. Hence using the slower `file` is the only way
        # to go.
        rev = repo.revs('file(%s) and ::%s', b'path:' + path, ctx).last()
        commit = None if rev is None else message.commit(repo[rev])
        return LastCommitForPathResponse(commit=commit)

    def ListLastCommitsForTree(self, request: ListLastCommitsForTreeRequest,
                               context) -> ListLastCommitsForTreeResponse:
        return not_implemented(context, ListLastCommitsForTreeResponse,
                               issue=14)  # pragma no cover

    def CommitsByMessage(self, request: CommitsByMessageRequest,
                         context) -> CommitsByMessageResponse:
        return not_implemented(context, CommitsByMessageResponse,
                               issue=21)  # pragma no cover

    def ListCommitsByOid(self, request: ListCommitsByOidRequest,
                         context) -> ListCommitsByOidResponse:
        repo = self.load_repo(request.repository, context)
        for chunk in chunked(pycompat.sysbytes(oid) for oid in request.oid):
            try:
                yield ListCommitsByOidResponse(
                    commits=[message.commit(repo[rev])
                             for rev in repo.revs(b'%ls', chunk)])
            except (error.LookupError, error.RepoLookupError) as exc:
                context.set_code(StatusCode.NOT_FOUND)
                context.set_details(repr(exc.args))

    def ListCommitsByRefName(self, request: ListCommitsByRefNameRequest,
                             context) -> ListCommitsByRefNameResponse:
        return not_implemented(context, ListCommitsByRefNameResponse,
                               issue=23)  # pragma no cover

    def FilterShasWithSignatures(self,
                                 request: FilterShasWithSignaturesRequest,
                                 context) -> FilterShasWithSignaturesResponse:
        return not_implemented(context, FilterShasWithSignaturesResponse,
                               issue=24)  # pragma no cover

    def GetCommitSignatures(self, request: GetCommitSignaturesRequest,
                            context) -> GetCommitSignaturesResponse:
        return not_implemented(context, GetCommitSignaturesResponse,
                               issue=24)  # pragma no cover

    def GetCommitMessages(self, request: GetCommitMessagesRequest,
                          context) -> GetCommitMessagesResponse:
        return not_implemented(context, GetCommitMessagesResponse,
                               issue=25)  # pragma no cover
