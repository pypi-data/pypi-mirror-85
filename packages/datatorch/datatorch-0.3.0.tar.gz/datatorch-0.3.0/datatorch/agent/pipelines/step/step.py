from typing import List
from datetime import datetime, timezone
from ..action import get_action, Action
from ..template import Variables
from typing import TYPE_CHECKING, Union
import asyncio


if TYPE_CHECKING:
    from ..job import Job
    from ...client import Log


UPLOAD_LOGS_EVERY_SECONDS = 10


def _pick(dic: dict, keys: List[str]):
    return {key: dic[key] for key in keys}


class Step(object):
    @classmethod
    def from_dict_list(cls, steps: List[dict], job: "Job" = None):
        return [cls.from_dict(s, job) for s in steps]

    @classmethod
    def from_dict(cls, step: dict, job: "Job" = None):
        return cls(
            id=step.get("id"),
            action=step.get("action", ""),
            name=step.get("name", ""),
            inputs=step.get("inputs", {}),
            job=job,
        )

    def __init__(
        self,
        id: str = None,
        action: Union[str, dict] = "",
        name: str = "",
        inputs: dict = {},
        job: "Job" = None,
    ):
        self._action = action
        self.id = id
        self.logs: "List[Log]" = []
        self.name = name
        self.inputs = inputs
        self.job = job

    async def action(self) -> Action:
        return await get_action(self._action, step=self)

    async def update(
        self, inputs: dict = None, status: str = None, outputs: dict = None
    ):
        if self.api is None or self.id is None:
            return

        if inputs is not None:
            inputs = _pick(inputs.copy(), list(self.inputs.keys()))

        iso_date = datetime.now(timezone.utc).isoformat()[:-9] + "Z"
        variables = {
            "id": self.id,
            "inputs": inputs,
            "outputs": outputs,
            "status": status,
            "startedAt": iso_date if status == "RUNNING" else None,
            "finishedAt": iso_date
            if status == "SUCCESS" or status == "FAILED"
            else None,
        }
        await self.api.update_step(variables)

    async def run(self, variables: Variables) -> dict:

        # Upload logs in the background.
        task = asyncio.create_task(self.log_uploader())

        variables.set_step(self)

        # Add specified inputs
        for k, v in self.inputs.items():
            variables.add_input(k, v)

        # Outputs will be updated by the action as it casts them into the
        # correct format.
        await self.update(status="RUNNING")

        action = await self.action()
        outputs = await action.run(variables)

        for k, v in outputs.items():
            variables.add_input(k, v)

        task.cancel()
        await self.update(outputs=outputs, status="SUCCESS")
        await self.upload_logs()

        return outputs

    async def log_uploader(self):
        await asyncio.sleep(UPLOAD_LOGS_EVERY_SECONDS)
        await self.upload_logs()

    @property
    def api(self):
        """ Agent API Client if it exists. """
        return self.job and self.job.api

    def log(self, message: str):
        """ Records a log message. """
        iso_date = datetime.now(timezone.utc).isoformat()[:-9] + "Z"
        self.logs.append(dict(createdAt=iso_date, message=message))  # type: ignore

    async def upload_logs(self):
        """ Uploads saved logs to webserver. """
        if self.id and len(self.logs) > 0:
            logs = self.logs
            self.logs = []
            await self.api.upload_step_logs(self.id, logs)
