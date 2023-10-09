from apscheduler.schedulers.asyncio import AsyncIOScheduler

from actions.action import Action


class CancelAllScheduledActions(Action):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def execute(self):
        self.scheduler.remove_all_jobs()

