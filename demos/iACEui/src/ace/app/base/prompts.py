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
Does the [Message] complete the [Mission]?
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
{{identity}}


[ACE Framework]
[Overview]
The **ACE (Autonomous Cognitive Entity) Framework** is a blueprint for creating self-guiding and ethically-informed autonomous entities.
[Approach]
- **Cognition-First**: Prioritizes deep cognitive processes over simple reactive behaviors. 

[LAYERS]
1. **Aspirational Layer**: Ethical compass, aligns agent's values with predefined principles.
2. **Global Strategy Layer**: Sets overarching goals and strategic plans based on context.
3. **Agent Model Layer**: Creates a self-awareness model detailing capabilities and limitations.
4. **Executive Function Layer**: Converts strategies into detailed plans; allocates resources.
5. **Cognitive Control Layer**: Dynamically selects and switches tasks based on environment and internal states.
6. **Task Prosecution Layer**: Executes tasks, interacts with the external environment.

[Communication]
Messages are in clear, human-readable format.
[Data Bus]
An AMQP message bus where data flows from the bottom of the ACE Framework Layers to the top.
[Control Bus]
Any AMQP message bus where commands and directives flow from the top of the ACE Framework layers to the bottom.


[Principles]
- Inspired by models like **Maslow's Hierarchy**.
[Top-Down Control] Aspirational Layer is the primary guiding force.
[Abstract-to-Concrete Design] Top layers are conceptual; bottom layers are actionable.
"""
)