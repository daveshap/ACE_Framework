import asyncio

from actions.action import Action
from channels.communication_channel import CommunicationChannel


class ScheduleAction(Action):
    def __init__(self, communication_channel: CommunicationChannel, action_to_schedule: Action, delay_seconds: int):
        print("Created ScheduleAction with scheduled action: " + str(action_to_schedule))
        self.communication_channel = communication_channel
        self.action_to_schedule = action_to_schedule
        self.delay_seconds = delay_seconds

    async def execute(self):
        print(f"Waiting {self.delay_seconds} seconds to execute scheduled action {self.action_to_schedule}....")
        await asyncio.sleep(self.delay_seconds)
        print(f"{self.delay_seconds} seconds have passed! Executing scheduled action {self.action_to_schedule}")
        await self.action_to_schedule.execute()
