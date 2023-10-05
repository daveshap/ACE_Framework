import uuid
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from actions.action import Action
from channels.communication_channel import CommunicationChannel


class ScheduleAction(Action):
    def __init__(self,
                 scheduler: AsyncIOScheduler,
                 communication_channel: CommunicationChannel,
                 action_to_schedule: Action,
                 delay_seconds: int):
        print("Created ScheduleAction with scheduled action: " + str(action_to_schedule))
        self.scheduler = scheduler
        self.communication_channel = communication_channel
        self.action_to_schedule = action_to_schedule
        self.delay_seconds = delay_seconds

    async def execute(self):
        run_date = datetime.now() + timedelta(seconds=self.delay_seconds)
        action_id = str(uuid.uuid4())
        self.scheduler.add_job(
            self.action_to_schedule.execute,
            args=(),
            trigger='date',
            run_date=run_date,
            id=action_id,
            name=str(self.action_to_schedule)
        )

    def __str__(self):
        return "schedule_action for action: " + str(self.action_to_schedule)
