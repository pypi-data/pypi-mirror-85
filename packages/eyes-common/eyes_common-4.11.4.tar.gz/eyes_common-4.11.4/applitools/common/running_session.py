from typing import Optional, Text

import attr

from applitools.common.ultrafastgrid import RenderingInfo
from applitools.common.utils.json_utils import JsonInclude


@attr.s
class RunningSession(object):
    """
    Encapsulates data for the session currently running in the agent.
    """

    id = attr.ib(metadata={JsonInclude.THIS: True})  # type: Text
    session_id = attr.ib(metadata={JsonInclude.THIS: True})  # type: Text
    batch_id = attr.ib(metadata={JsonInclude.THIS: True})  # type: Text
    baseline_id = attr.ib(metadata={JsonInclude.THIS: True})  # type: Text
    url = attr.ib(metadata={JsonInclude.THIS: True})  # type: Text
    rendering_info = attr.ib(
        type=RenderingInfo, default=None
    )  # type: Optional[RenderingInfo]
    is_new_session = attr.ib(
        default=False, metadata={JsonInclude.NAME: "isNew"}
    )  # type: bool
