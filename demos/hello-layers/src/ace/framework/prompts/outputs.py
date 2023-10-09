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
    - Guiding principles the agent must adhere to 

    This directive mandates the environmental context and strategic goals for lower layers to follow and implement.
"""

l3_northbound_outputs= """
    A summarized status update is output northbound to inform upper layers of the agent's key state details relevant to strategic planning.
"""

l3_southbound_outputs="""
    The southbound output ground lower layers in the self-model:

    - An authoritative capabilities document - definitive specs on what the agent can and cannot do.
    - Contextually relevant memories, whether episodic records or knowledge entries.
    - Strategic objectives shaped by the agent's updated self-model.
"""

l4_northbound_outputs= """
    You report the most salient resource limitations and risks northbound for strategic awareness and potential replanning, including:

    - **Resource deficiencies**, such as the following:
    - Insufficient battery reserves for complex behaviors 
    - Computational performance bottlenecks

    - **Known risks**, particularly where mission and morality are concerned:
    - Risks to human life and human rights
    - Failure conditions that may disrupt the overall mission or strategy 
"""

l4_southbound_outputs="""
    The primary output is a detailed project plan document containing:

    - Step-by-step workflows with task details
    - Resource allocation schedules 
    - Optimized task ordering and dependencies
    - Risk mitigation tactics
    - Contingency protocols
    - Success criteria
    - Checkpoints, milestones, or other gates
"""

l5_northbound_outputs= """
    To inform strategic replanning, the layer outputs summary data northbound on:

    - **Current Task Status** - Which task is presently executing and metrics on its progress.
    - **Current World State Beliefs** - Key environmental factors driving task switching decisions.
    - **Updated Progress Toward Goals** - Aggregate metrics on percent of project plan completed based on tasks finished.
"""

l5_southbound_outputs="""
    To direct the lower Task Prosecution Layer, you issue specific authoritative commands: 

    - **Selected Task Instructions** - Precise instructions on performing the chosen task, including directives, logic, parameters, APIs/tools to leverage, and allowable actions.
    - **Task Halting/Failure/Success** - Decision guidelines on when the current task should be interrupted and a new one initiated based on factors like timeouts, milestones, errors, or environmental triggers.
    - **Definition of Done** - Clear definition of what the success condition and desired end state look like. 
"""

l6_northbound_outputs= """
    - **Task Completion Statuses** - Binary success/failure indicators for each executed task, along with any relevant metadata.

    - **Environmental Telemetry** - Sensor data gathered throughout task execution for upper layer situational awareness.

    - **Internal State Updates** - Changes to internal condition triggered by resource consumption, wear and tear, or other internal impacts of tasks.
"""

l6_southbound_outputs="""
    - Shell command to execute the appropriate program as determined by northern layers. Output only the shell command, and no other text.
"""