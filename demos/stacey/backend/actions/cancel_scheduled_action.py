from apscheduler.schedulers.asyncio import AsyncIOScheduler

from actions.action import Action


class CancelScheduledAction(Action):
    def __init__(self, scheduler: AsyncIOScheduler, job_id: str):
        self.scheduler = scheduler
        self.job_id = job_id

    async def execute(self):
        self.scheduler.remove_job(self.job_id)

