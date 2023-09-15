# Introduction to the ACE Framework

The Autonomous Cognitive Entity (ACE) framework provides a layered architecture for developing self-directing, self-modifying, and self-stabilizing autonomous machine entities. Inspired by biological cognition and principles from computer science, it coordinates specialized functions to enable sophisticated reasoning, planning, and ethical decision-making.  

At the core of the ACE framework is a "cognition-first" approach that emphasizes internal cognitive processes over reactive input-output loops. This prioritizes imagination, reflection, and strategic thinking, with environmental interaction being secondary.

The framework consists of six hierarchical layers, each handling distinct functions:

- **Aspirational Layer** - Provides an ethical constitution to align the agent's values and judgements. Formulated in natural language principles.
- **Global Strategy Layer** - Considers the agent's context to set high-level goals and strategic plans.
- **Agent Model Layer** - Develops a functional self-model of the agent's capabilities and limitations. 
- **Executive Function Layer** - Translates strategic direction into detailed project plans and resource allocation.
- **Cognitive Control Layer** - Dynamically selects tasks and switches between them based on environment and internal state.
- **Task Prosecution Layer** - Executes tasks using digital functions or physical actions. Interacts with the environment.

Information flows bidirectionally between adjacent layers to coordinate cognition from abstract reasoning to concrete actions. Together, these layers aim to produce an AGI architecture grounded in ethics and aligned with human values.

The ACE framework provides a conceptual blueprint for autonomous agents that are corrigible, transparent, and beneficial by design. It balances goal-directedness with moral principles to shape behavior. By elucidating this layered cognitive architecture, the ACE framework offers a comprehensive reference for developing aligned AGI.

## Interlayer Communication Buses

The ACE framework employs two unidirectional communication busss to coordinate information flow between layers:

- **Northbound Bus** - Carries internal state and external sensor data upward through layers. Enables lower layers to provide sensor, execution status, and other telemetry to higher layers.
- **Southbound Bus** - Carries directives and instructions downward through layers. Allows higher layers to provide guidance, instructions, and mission objectives to lower layers. 

All layers connect to both buses simultaneously. The northbound bus facilitates bottom-up information flow, while the southbound bus enables top-down control. 

Layers can only communicate directly with their immediate upper and lower neighbors. However, by publishing messages onto the buses, layers can indirectly transmit information to non-adjacent layers.

The northbound and southbound buses carry structured data packets encoded in human-readable natural language. This allows all interlayer messaging to remain interpretable and transparent. 

For example, the Task Prosecution layer might publish a message to the northbound bus indicating "Error executing API call X with parameters Y - retry limit exceeded." Meanwhile, the Aspirational layer might publish a message to the southbound bus stating "New secondary objective: Prioritize tasks that improve safety and reduce risk."

This interlayer communication architecture ensures clear signaling between the ACE framework's hierarchical components while maintaining transparency and human oversight. The buses coordinate cognition across abstraction levels, facilitating autonomous decision-making.
