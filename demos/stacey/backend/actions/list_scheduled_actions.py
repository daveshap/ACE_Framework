from apscheduler.schedulers.asyncio import AsyncIOScheduler

from actions.action import Action


class GetScheduledActions(Action):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def execute(self):
        scheduled_jobs = self.scheduler.get_jobs()
        return str(scheduled_jobs)