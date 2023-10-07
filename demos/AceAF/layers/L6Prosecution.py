from .AceLayer import AceLayer
from .customagents.l6prosecution.TaskProsecution import TaskProsecution


class L6Prosecution(AceLayer):
    task_prosecution = TaskProsecution()

    def run_agents(self):
        self.result = self.task_prosecution.run(task=self.top_layer_message)
        print(self.result)
