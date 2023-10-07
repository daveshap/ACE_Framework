from .AceLayer import AceLayer
from .customagents.l5cogntiive.TaskSelectionAgent import TaskSelectionAgent


class L5Cognitive(AceLayer):
    task_selection = TaskSelectionAgent()

    def run_agents(self):
        self.result = self.task_selection.run(task_list=self.top_layer_message)
