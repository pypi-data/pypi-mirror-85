from .action import Action

import os
import logging
import typing

from typing import Union
from datatorch.agent.directory import agent_directory
from .config import ActionConfig


if typing.TYPE_CHECKING:
    from ..step import Step


__all__ = ["Action", "get_action"]


logger = logging.getLogger("datatorch.agent.action")


async def get_action(action: Union[str, dict], step: "Step" = None) -> Action:
    config = ActionConfig(action)

    # Get actions directory
    action_dir = agent_directory.action_dir(config.name, config.version)
    folder_exists = os.path.exists(action_dir)

    if folder_exists:
        logger.debug(
            "Action found locally ({}@{}).".format(config.name, config.version)
        )
    else:
        logger.debug("Downloading action {}@{}.".format(config.name, config.version))
        await config.download()

    return Action(config, action_dir, step=step)
