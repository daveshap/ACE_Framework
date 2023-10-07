from .AceLayer import AceLayer
from .customagents.l4executive.TaskCreation import TaskCreation


class L4Executive(AceLayer):
    task_creation = TaskCreation()

    def run_agents(self):
        self.result = self.task_creation.run(strategy=self.top_layer_message)
