from  jinja2 import Template


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

action_prompt_template = Template(
"""
# Given Your Role as the {{ role_name }} in the ACE framework
Consider the INPUT, YOUR REASONING about it, and BUS RULES to decide what, if any, message you should place on the {{destination_bus}}

## INPUT
Input source bus = {{ source_bus }}

## YOUR REASONING
{{ reasoning_completion }}

## BUS RULES
{{ bus_rules }}
"""
)

def get_action_prompt(
    role_name: str,
    source_bus: str,
    destination_bus: str,
    reasoning_completion: str,
    bus_rules: str,
):
    return action_prompt_template.render(
        role_name=role_name,
        source_bus=source_bus,
        destination_bus=destination_bus,
        reasoning_completion=reasoning_completion,
        bus_rules=bus_rules,
    )


reasoning_prompt_format = Template("""
# You Received a MESSAGE From the SOURCE BUS
## MESSAGE
{{input}}

## SOURCE BUS
{{source_bus}}
""")

def get_reasoning_input(
    input: str,
    source_bus: str,
):
    return reasoning_prompt_format.render(
        input=input,
        source_bus=source_bus,
    )