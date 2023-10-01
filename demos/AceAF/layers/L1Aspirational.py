from .AceLayer import AceLayer
from agentforge.config import Config
from .TestAgent import TestAgent

testini = """As an AI language model, I don't have real-time data or access to specific statistics. However, I can provide some general observations on how Overwatch's popularity has declined over time based on previous reports and discussions.

1. Saturation and competition: Overwatch was initially released in 2016 and gained significant popularity due to its unique blend of first-person shooter and team-based gameplay. However, over time, the market became saturated with similar games, leading to increased competition for player attention. This saturation may have contributed to a decline in Overwatch's popularity.

2. Lack of content updates: Overwatch's popularity was also affected by a perceived lack of regular content updates. While the game received new heroes, maps, and events periodically, some players felt that the updates were not substantial enough to keep them engaged in the long term. This lack of fresh content may have led to a decline in player interest.

3. Balancing issues and meta fatigue: Balancing a game with a diverse roster of heroes can be challenging, and Overwatch faced criticism for its balancing issues. Certain heroes or strategies dominating the meta for extended periods could lead to frustration and fatigue among players. This could have contributed to a decline in popularity as players sought more balanced and dynamic experiences.

4. Community toxicity: Like many online multiplayer games, Overwatch has faced issues with toxic behavior within its community. Toxicity, including harassment, abusive language, and unsportsmanlike conduct, can drive players away and negatively impact the game's popularity. While efforts have been made to address this issue, it may have still contributed to a decline in player numbers.

5. Shifting player preferences: Gaming trends and player preferences can change over time. Some players may have simply moved on to other games or genres that align better with their current interests. This natural shift in player preferences could have contributed to a decline in Overwatch's popularity.

It's important to note that while Overwatch may have experienced a decline in popularity, it still maintains a dedicated player base and continues to receive updates and support from its developers."""


class L1Aspirational(AceLayer):

    constitution = None
    agent = TestAgent()

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        self.constitution = self.config.data['Constitution']

    def run_agents(self):
        # Override Agents
        # testo = self.agent.run()
        # print(testo)
        self.update_bus(bus="SouthBus", message=self.constitution)
        self.interface.output_message(self.layer_number, testini)



