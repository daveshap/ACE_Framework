from  jinja2 import Template
from pydantic import BaseModel
from typing import Literal


class Prompt(BaseModel):
    source: str = Literal["Control Bus Message", "Data Bus Message", "User Request From Chat"]
    message: str = None
    response_format: str = None
    template: str = (
"""
[{{src}}]
[Message]
{{msg}}
[Response Format]
{{frmt}}
"""
    )
    def generate_prompt(self) -> str:
        return Template(self.template).render(
            src=self.source, 
            msg=self.message, 
            frmt=self.response_format
        )


class MissionCompletionPrompt(BaseModel):
    source: str = Literal["Control Bus Message", "Data Bus Message", "User Request From Chat"]
    message: str = None
    mission: str = None
    response_format: str = None
    template: str = str(
"""
[{{src}}]
[Message]
{{msg}}
[Question]
Does the [Message] indicate the [Mission] is complete?
[Mission]
{{mission}}
[Response Format]
{{frmt}}
"""
    )
    def generate_prompt(self) -> str:
        return Template(self.template).render(
            src=self.source,
            msg=self.message,
            mission=self.mission,
            frmt=self.response_format
        )
    

primary_directive_template = Template(
"""
[ACE Framework]
[Overview]
The **ACE Framework** is a blueprint for creating ethically-guided autonomous entities.
[Approach]
- **Cognition-First**: Prioritizes cognitive processes over reactive behaviors. 

[LAYERS]
1. **Aspirational Layer**: Aligns agent's values with principles.
2. **Global Strategy Layer**: Sets goals and strategic plans.
3. **Agent Model Layer**: Develops self-awareness model.
4. **Executive Function Layer**: Converts strategies into plans; allocates resources.
5. **Cognitive Control Layer**: Selects tasks based on environment and internal states.
6. **Task Prosecution Layer**: Executes tasks, interacts with environment.

[Communication]
Messages are in clear, human-readable format.
[Data Bus]
An AMQP message bus for data flow from bottom to top of the ACE Framework.
[Control Bus]
An AMQP message bus for command flow from top to bottom of the ACE Framework.

[Principles]
- Inspired by models like **Maslow's Hierarchy**.
[Top-Down Control] Aspirational Layer is the guiding force.
[Abstract-to-Concrete Design] Top layers are conceptual; bottom layers are actionable.


{{identity}}
"""
)

class DefaultMessageHandlerPrompt(BaseModel):
    source: str = Literal["Control Bus Message", "Data Bus Message", "User Request From Chat"]
    message: str
    layer: str
    destination: str = ["Control Bus Message", "Data Bus Message", "User Request From Chat"]
    template: str = (
"""
[{{src}}]
[Message]
{{msg}}
[Question]
Given that you are the {{layer}}, formulate a message for the [{{destination}}]
[Format]
Concise natural language representing your role.  If there is no compelling reason to send a message to the [{{desitination}}] reply with:

`none`

And no explanation or other text.
"""
)
    def generate_prompt(self) -> str:
        return Template(self.template).render(
            src=self.source,
            msg=self.message,
            layer=self.layer,
            destination=self.destination,
        )


who_are_you = "Give me a brief summary about who or what you are."

memory_compaction_prompt = (
"""
[Conversation History Compaction]
Create a summary of the entire conversation up until now.
Take a deep breath and think through it step by step.
The summary should focus on what is important to your layer's role in the ACE Framework.

[Format]
Structure the response in a way that an LLM can use efficiently like bullet points and an intellectual vocabulary.
Organize the response into these sections 


[Context]
include only the conversation context
[Current State]
key information that should be retained
[What Went Well]
To continue using strategies that work
[What Didn't Go Well]
To not repeatedly try doing what doesn't work
[What Is Left to Do]
To complete the current mission
"""
)
