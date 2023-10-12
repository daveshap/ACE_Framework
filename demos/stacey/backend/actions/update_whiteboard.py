from actions.action import Action


class UpdateWhiteboard(Action):
    def __init__(self, l3_agent_layer, contents: str):
        self.l3_agent_layer = l3_agent_layer
        self.contents = contents

    async def execute(self):
        await self.l3_agent_layer.update_whiteboard(self.contents)

    def __str__(self):
        return "Update whiteboard"
