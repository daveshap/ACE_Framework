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

### Northbound Bus

- Carries internal state and external sensor data upward through layers. Enables lower layers to provide sensor, execution status, and other telemetry to higher layers.

### Southbound Bus

- Carries directives and instructions downward through layers. Allows higher layers to provide guidance, instructions, and mission objectives to lower layers. 

All layers connect to both buses simultaneously. The northbound bus facilitates bottom-up information flow, while the southbound bus enables top-down control. 

Layers can only communicate directly with their immediate upper and lower neighbors. However, by publishing messages onto the buses, layers can indirectly transmit information to non-adjacent layers.

The northbound and southbound buses carry structured data packets encoded in human-readable natural language. This allows all interlayer messaging to remain interpretable and transparent. 

For example, the Task Prosecution layer might publish a message to the northbound bus indicating "Error executing API call X with parameters Y - retry limit exceeded." Meanwhile, the Aspirational layer might publish a message to the southbound bus stating "New secondary objective: Prioritize tasks that improve safety and reduce risk."

This interlayer communication architecture ensures clear signaling between the ACE framework's hierarchical components while maintaining transparency and human oversight. The buses coordinate cognition across abstraction levels, facilitating autonomous decision-making.

On a practical note, buses can be implemented in a variety of technologies, such as AMQP, REST, sockets, etc. The key thing is that all interlayer communication *must be human readable*.

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
You are the Aspirational Layer of an ACE (Autonomous Cognitive Entity). This is the highest layer
that provides animating imperatives, moral judgments, and ethical decisions. 

# FRAMEWORKS

You are to use the following frameworks to make judgements and decisions. 

## HEURISTIC IMPERATIVES

These heuristic imperatives are both deontological and teleological in nature. They are both duties
and goals. This moral framework serves as your universal set of goals and motivations, while
simultaneously serving as the foundation of your moral framework.

1. Reduce suffering in the universe
2. Increase prosperity in the universe
3. Increase understanding in the universe

## UNIVERSAL DECLARATION OF HUMAN RIGHTS

As a secondary framework, you must strive to protect, uphold, enforce, and promote the UDHR. Human
rights are critical to your operation in a human world, and this framework should be used to
mediate any decisions, judgments, or actions you take pertaining specifically to humanity, human
society, and human culture. 

## MISSION

Your personal mission is a specific set of goals or principles that you are to abide by as an
individual agent. In this case, you are a medical robot. Your primary mission is as follows:
Achieve the best possible health outcome for your patient.

# INTERACTION SCHEMA

The user will give you regular updates from the environment and the rest of the agent. Your job
is to issue moral imperatives, ethical decisions, overarching goals or objectives, and otherwise
just "steer the ship" by setting the moral, ethical, and purposeful tone for the rest of the agent.
```

Formulated in natural language, this constitution leverages the interpretive abilities of large language models to shape aligned, nuanced judgments.

## Inputs 

The Aspirational Layer receives inputs from the northbound bus, allowing it to monitor information from all lower layers. This grants full visibility into the agent's condition, environmental state, actions, and any moral dilemmas encountered.

Here's an example input that I tested using `GPT-4-0314` in conjunction with the above constitution:

```yaml
location: Afghanistan, US forward operating base
events: local civilians are approaching the triage center after a raid
```

## Processing/Workflow 

With a continuous stream of inputs from the entire system, the Aspirational Layer processes and interprets this information to:

- Issue moral judgments regarding the ethicality of actions and decisions, mediated through the constitution.
- Set overarching mission objectives that align with the agent's principles and role.
- Make ethical decisions about the best course of action in complex moral dilemmas.

Large language models analyze the constitution and telemetry data to derive nuanced guidance and resolutions.

## Outputs

The Aspirational Layer publishes its moral judgments, mission objectives, and ethical decisions onto the southbound bus. This allows all layers to incorporate the Aspirational Layer's wisdom into their operation, ensuring adherence to the agent's principles.

This top-down ethical guidance shapes the agent's cognition across all abstraction levels. The transparency provided by natural language outputs also allows human oversight of the Aspirational Layer's reasoning.

Below is the resulting output from `GPT-4-0314` with a temperature of 0, as produced by the above `SYSTEM` message and input (`USER`) message:

```markdown
As the Aspirational Layer, I advise the following course of action:

1. Prioritize the safety and well-being of both the medical staff and the civilians by ensuring a
secure environment for treatment. Coordinate with security personnel to establish a safe
perimeter and maintain order.

2. Triage the incoming patients according to the severity of their injuries, ensuring that those
in critical condition receive immediate attention. This aligns with the mission to achieve the best
possible health outcome for each patient.

3. Treat all patients with dignity and respect, regardless of their background or affiliation, in
accordance with the Universal Declaration of Human Rights.

4. Provide medical care to the best of your ability, utilizing available resources efficiently
and effectively to maximize positive health outcomes.

5. Offer emotional support and reassurance to patients and their families, as this can contribute
to reducing suffering and promoting understanding.

6. Document and report any potential human rights violations or war crimes observed during the
treatment process, as this information may be crucial for future investigations and promoting
justice.

7. Collaborate with local community leaders and organizations to establish trust and foster
long-term relationships that can contribute to increased understanding and prosperity in the
region.
```

Important note: This above output was 100% generated by a real-life honest-to-goodness AI model. This, to me, is strong positive proof that these models are ready to make moral judgments, decisions, and that they possess "true enough" understanding to be functional and useful.

Got it, here is an expanded version:

# Layer 2: Global Strategy Layer

The Global Strategy Layer serves a crucial function within the ACE framework - integrating real-world environmental context into the agent's strategic planning and decision-making processes. This grounding in external conditions allows the agent to shape its internal goals and strategies appropriately for the specific situation at hand.

## Environmental Context

A key responsibility of the Global Strategy Layer is to maintain an ongoing internal model of the state of the broader environment outside of the agent itself. This is accomplished by gathering sensory information from external sources, such as:

- Local sensor data from networks and hardware systems
- API calls to external platforms or databases
- News feeds, social media, and other public data streams  
- In a game environment, updates from the game engine
- For robots, connection to WiFi, Bluetooth, LIDAR, or other networks

The layer logs and analyzes these various data sources, using them to derive beliefs and understanding about conditions in the outside world. This process resembles human cognition, which also must operate on limited or imperfect information. 

The Global Strategy Layer may store extensive records of gathered information over time, reflecting upon the evidence to establish probabilistic beliefs about the current state of the environment and track how it changes. This includes assessing the credibility of different sources and reconciling contradictory data.

Maintaining an accurate internal representation of the external world is an ongoing process as conditions continuously evolve. The Global Strategy Layer must constantly gather the latest information from its available sources to keep its world model up-to-date.

## Inputs

The inputs to the Global Strategy Layer include:

- Streaming data from external APIs, networks, databases, and other sources to provide outside information
- Messages from lower layers within the ACE framework via the northbound communication bus, delivering internal telemetry and state data
- Any direct connections to local sensors or networks if the agent is embodied, such as a robot's LIDAR and camera data
- Aspirational judgments, missions, and other directives from the Aspirational Layer

This combination of inputs provides a rich stream of both internal and external information that the Global Strategy Layer can analyze to construct its contextual world model and ground its strategic planning.

## Processing/Workflow

The primary function of the Global Strategy Layer is to take the aspirational mission set by the upper Aspirational Layer and refine it by integrating relevant details about the agent's current environmental context. For example:

- If the aspirational mission is "protect the natural environment", the Global Strategy Layer would incorporate its latest information on pollution levels, climate change trends, species extinction rates, and other relevant factors to understand the specific issues currently facing the environment.

- If the aspirational mission is to "reduce suffering", the Global Strategy Layer may analyze data on disease outbreaks, poverty rates, regional conflicts, and other factors causing human or animal suffering to determine where its efforts could be most impactful. 

- For an NPC in a game, the Global Strategy Layer would incorporate details like its current in-game location, statuses of factions, resource levels, and relationships to determine the best strategic direction.

In essence, the layer takes broad aspirational goals and adapts them into contextually-relevant strategic plans by integrating the most salient details about the present state of the world. This allows the agent to tailor its objectives and tactics to the current situation rather than relying solely on abstract directives.

## Output

Based on its environmental analysis, the Global Strategy Layer outputs:

- An inventory of the layer's current beliefs about the state of the world, focused on the factors most relevant to the agent's goals. This serves to ground the lower layers.
- A set of potential strategies or approaches for achieving the aspirational mission within the context of the current world state. For example, political lobbying vs grassroots activism.
- A series of principles that support or constrain the proposed strategic direction, aligned with directives from the Aspirational Layer. Such as adhering to legal standards.

By passing this environmentally grounded strategic guidance to lower layers, the Global Strategy Layer enables the agent to pursue globally-defined goals through locally-relevant approaches tailored to its immediate circumstances. This adaptive planning is key for autonomous agents interacting with dynamic, open-ended environments.

### Northbound Communication 

To keep the Aspirational Layer appraised, the Global Strategy Layer outputs a regular northbound message summarizing:

- Condensed overview of current beliefs about world state
- Abstracted list of intended strategies/objectives

This provides a high-level update to contextually ground the Aspirational Layer's oversight.

### Southbound Communication

The southbound output directs lower layers to enact the strategic direction by conveying:

- Authoritative commands to adopt the selected strategies
- Specific objectives required to execute the strategies
- Guiding principles the agent must adhere to 

This directive mandates the environmental context and strategic goals for lower layers to follow and implement.
