from actions.action import Action


class UpdateWhiteboard(Action):
    def __init__(self, l2_global_strategy_layer, client_name: str, contents: str):
        self.l2_global_strategy_layer = l2_global_strategy_layer
        self.client_name = client_name
        self.contents = contents

    async def execute(self):
        client_agent = await self.l2_global_strategy_layer.find_client_agent(self.client_name)
        if not client_agent:
            return "Strange, I have no client named " + self.client_name
        await client_agent.update_whiteboard(self.contents)

    def __str__(self):
        return "Update whiteboard for " + self.client_name



