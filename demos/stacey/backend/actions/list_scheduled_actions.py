from apscheduler.schedulers.asyncio import AsyncIOScheduler

from actions.action import Action


class GetScheduledActions(Action):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def execute(self):
        scheduled_jobs = self.scheduler.get_jobs()
        job_descriptions = list(map(self.describe_job, scheduled_jobs))
        return "\n".join(job_descriptions)

    def describe_job(self, job):
        return f"Job ID: {job.id}, Next Run Time: {job.next_run_time}, Action: {job.name}"
