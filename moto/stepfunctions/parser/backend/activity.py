import datetime
from collections import deque
from typing import Deque, Optional

from moto.stepfunctions.parser.api import (
    ActivityListItem,
    Arn,
    DescribeActivityOutput,
    Name,
    Timestamp,
)


class ActivityTask:
    task_input: str
    task_token: str

    def __init__(self, task_token: str, task_input: str):
        self.task_token = task_token
        self.task_input = task_input


class Activity:
    arn: Arn
    name: Name
    creation_date: Timestamp
    _tasks: Deque[ActivityTask]

    def __init__(self, arn: Arn, name: Name, creation_date: Optional[Timestamp] = None):
        self.arn = arn
        self.name = name
        self.creation_date = creation_date or datetime.datetime.now(
            tz=datetime.timezone.utc
        )
        self._tasks = deque()

    def add_task(self, task: ActivityTask):
        self._tasks.append(task)

    def get_task(self) -> Optional[ActivityTask]:
        return self._tasks.popleft()

    def to_describe_activity_output(self) -> DescribeActivityOutput:
        return DescribeActivityOutput(
            activityArn=self.arn, name=self.name, creationDate=self.creation_date
        )

    def to_activity_list_item(self) -> ActivityListItem:
        return ActivityListItem(
            activityArn=self.arn, name=self.name, creationDate=self.creation_date
        )
