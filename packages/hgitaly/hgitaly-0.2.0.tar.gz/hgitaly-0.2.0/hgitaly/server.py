# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Server startup logic.

While the exposition as a Mercurial extension is certainly convenient for
many reasons, it is best to separate what is specific to the extension context
and what is just generic gRPC server code.
"""
from concurrent import futures
import grpc
import logging
from urllib.parse import urlparse

from .service.commit import CommitServicer
from .service.ref import RefServicer
from .service.repository_service import RepositoryServiceServicer

from .stub.commit_pb2_grpc import add_CommitServiceServicer_to_server
from .stub.ref_pb2_grpc import add_RefServiceServicer_to_server
from .stub.repository_service_pb2_grpc import (
    add_RepositoryServiceServicer_to_server
)

logger = logging.getLogger(__name__)


class UnsupportedUrlScheme(ValueError):
    pass


class BindError(RuntimeError):
    pass


class InvalidUrl(ValueError):
    pass


def init(listen_urls, storages):
    """Return server object for given parameters"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_CommitServiceServicer_to_server(CommitServicer(storages), server)
    add_RefServiceServicer_to_server(RefServicer(storages), server)
    add_RepositoryServiceServicer_to_server(
        RepositoryServiceServicer(storages), server)

    for url in listen_urls:
        try:
            parsed_url = urlparse(url)
        except ValueError as exc:
            raise InvalidUrl(url, *exc.args)
        try:
            if parsed_url.scheme == 'tcp':
                port = server.add_insecure_port(parsed_url.netloc)
                info = ("Listening on %r, final port is %d", url, port)
            elif parsed_url.scheme == 'unix':
                server.add_insecure_port(url)
                info = ("Listening on Unix Domain socket at %r",
                        parsed_url.path)
            else:
                raise UnsupportedUrlScheme(parsed_url.scheme)
        except RuntimeError:
            raise BindError(url)

        # outside of exception handling, to avoid potential masking effects
        logger.info(*info)
    return server


def run_forever(listen_urls, storages):  # pragma no cover
    """Run the server, never stopping

    :param listen_urls: list of URLs, given as in the same form as in
       GitLab configuration files.
    :param storages: a :class:`dict`, mapping storage names to the
       corresponding root directories for repositories.
    """
    server = init(listen_urls, storages)
    server.start()
    logger.info("Server started")
    server.wait_for_termination()
