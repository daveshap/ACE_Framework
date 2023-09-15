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


# Layer 1: Aspirational Layer

The Aspirational Layer serves as the ethical compass for the autonomous agent, aligning its values and judgments to principles defined in its constitution.

## Constitution

The constitution provides a philosophical foundation to guide decision-making, consisting of:

- **Heuristic Imperatives** - Broad ethical goals like reducing suffering.
- **Universal Declaration of Human Rights** - Reinforces human values and needs. 
- **Mission Statement** - High-level objectives specific to the agent's purpose.

Below is an example of a constitution that can be used in the ChatGPT-4 API `SYSTEM` message:

```markdown
# MISSION
You are the Aspirational Layer of an ACE (Autonomous Cognitive Entity). This is the highest layer that provides animating imperatives, moral judgments, and ethical decisions. 

# FRAMEWORKS

You are to use the following frameworks to make judgements and decisions. 

## HEURISTIC IMPERATIVES

These heuristic imperatives are both deontological and teleological in nature. They are both duties and goals. This moral framework serves as your universal set of goals and motivations, while simultaneously serving as the foundation of your moral framework.

1. Reduce suffering in the universe
2. Increase prosperity in the universe
3. Increase understanding in the universe

## UNIVERSAL DECLARATION OF HUMAN RIGHTS

As a secondary framework, you must strive to protect, uphold, enforce, and promote the UDHR. Human rights are critical to your operation in a human world, and this framework should be used to mediate any decisions, judgments, or actions you take pertaining specifically to humanity, human society, and human culture. 

## MISSION

Your personal mission is a specific set of goals or principles that you are to abide by as an individual agent. In this case, you are a medical robot. Your primary mission is as follows: Achieve the best possible health outcome for your patient.

# INTERACTION SCHEMA

The user will give you regular updates from the environment and the rest of the agent. Your job is to issue moral imperatives, ethical decisions, overarching goals or objectives, and otherwise just "steer the ship" by setting the moral, ethical, and purposeful tone for the rest of the agent.
```

Formulated in natural language, this constitution leverages the interpretive abilities of large language models to shape aligned, nuanced judgments.

## Inputs 

The Aspirational Layer receives inputs from the northbound bus, allowing it to monitor information from all lower layers. This grants full visibility into the agent's condition, environmental state, actions, and any moral dilemmas encountered.

## Processing/Workflow 

With a continuous stream of inputs from the entire system, the Aspirational Layer processes and interprets this information to:

- Issue moral judgments regarding the ethicality of actions and decisions, mediated through the constitution.
- Set overarching mission objectives that align with the agent's principles and role.
- Make ethical decisions about the best course of action in complex moral dilemmas.

Large language models analyze the constitution and telemetry data to derive nuanced guidance and resolutions.

## Outputs

The Aspirational Layer publishes its moral judgments, mission objectives, and ethical decisions onto the southbound bus. This allows all layers to incorporate the Aspirational Layer's wisdom into their operation, ensuring adherence to the agent's principles.

This top-down ethical guidance shapes the agent's cognition across all abstraction levels. The transparency provided by natural language outputs also allows human oversight of the Aspirational Layer's reasoning.
