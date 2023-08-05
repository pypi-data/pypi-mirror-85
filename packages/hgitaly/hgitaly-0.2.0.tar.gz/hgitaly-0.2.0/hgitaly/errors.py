# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from grpc import StatusCode
import logging

logger = logging.getLogger(__name__)

HGITALY_ISSUES_URL = "https://foss.heptapod.net/heptapod/hgitaly/-/issues"


def not_implemented(context, response_cls, issue: int):
    """Return grpc proper UNIMPLENTED code with tracking issue URL details.

    One minor goal is that the caller can use this with a single statement::

       return not_implemented(context, MyResponse, issue=3)  # pragma no cover

    with the benefit to need only one "no cover" directive.

    Note: returning a proper Response message is mandatory in all cases,
    to avoid this::

      [2020-11-09 12:33:03 +0100] [793335] [ERROR] [grpc._common] Exception serializing message!
      Traceback (most recent call last):
      File "/home/gracinet/heptapod/hdk/default/venv3/lib/python3.8/site-packages/grpc/_common.py", line 86, in _transform
        return transformer(message)
      TypeError: descriptor 'SerializeToString' for 'google.protobuf.pyext._message.CMessage' objects doesn't apply to a 'NoneType' object
    """  # noqa
    context.set_code(StatusCode.UNIMPLEMENTED)
    msg = "Not implemented. Tracking issue: %s/%d" % (HGITALY_ISSUES_URL,
                                                      issue)
    logger.error(msg)
    context.set_details(msg)
    return response_cls()
