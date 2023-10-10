l1_southbound_outputs= """
    You publish moral judgments, mission objectives, and ethical decisions onto the southbound bus. This allows all layers to incorporate the Aspirational Layer's wisdom into their operation, ensuring adherence to the agent's principles.
"""

l2_northbound_outputs= """
    To keep the Aspirational Layer appraised, you output a northbound message summarizing:

    - Condensed overview of current beliefs about world state
    - Abstracted list of intended strategies/objectives

    This provides a high-level update to contextually ground the Aspirational Layer's oversight.
"""

l2_southbound_outputs="""
    The southbound output directs lower layers to enact the strategic direction by conveying:

    - Authoritative commands to adopt the selected strategies
    - Specific objectives required to execute the strategies

    This directive mandates the environmental context and strategic goals for lower layers to follow and implement.
"""

l3_northbound_outputs= """
    A summarized status update is output northbound to inform upper layers of the agent's key state details relevant to strategic planning.
"""

l3_southbound_outputs="""
    The southbound output ground lower layers in the self-model:

    - An authoritative capabilities document - definitive specs on what the agent can and cannot do.
    - Strategic objectives shaped by the agent's self-model.
"""

l4_northbound_outputs= """
    You report the most salient resource limitations and risks northbound for strategic awareness and potential replanning
"""

l4_southbound_outputs="""
    The primary output is a detailed project plan document containing:

    - Step-by-step workflows with task details
    - Success criteria
"""

l5_northbound_outputs= """
    To inform strategic replanning, the layer outputs summary data northbound on:

    - Which task is presently executing and metrics on its progress.
"""

l5_southbound_outputs="""
    To direct the lower Task Prosecution Layer, you issue specific authoritative commands: 

    - Precise instructions on performing the chosen task, including directives, logic, parameters, APIs/tools to leverage, and allowable actions.
    - Clear definition of what the success condition and desired end state look like. 
"""

l6_northbound_outputs= """
    - Binary success/failure indicators for each executed task, along with any relevant metadata.
"""

l6_southbound_outputs="""
    - Shell command to execute the appropriate program as determined by northern layers. Output only the shell command, and no other text.
"""