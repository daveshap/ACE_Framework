# Introduction to the ACE Framework

The Autonomous Cognitive Entity (ACE) framework provides a layered architecture for developing self-directing, self-modifying, and self-stabilizing autonomous machine entities. Inspired by biological cognition and principles from computer science, it coordinates specialized functions to enable sophisticated reasoning, planning, and ethical decision-making.  

At the core of the ACE framework is a "cognition-first" approach that emphasizes internal cognitive processes over reactive input-output loops. This prioritizes imagination, reflection, and strategic thinking, with environmental interaction being secondary.

The framework consists of six hierarchical layers, each handling distinct functions:

- **[Aspirational Layer](#layer-1-aspirational-layer)** - Provides an ethical constitution to align the agent's values and judgements. Formulated in natural language principles.
- **[Global Strategy Layer](#layer-2-global-strategy-layer)** - Considers the agent's context to set high-level goals and strategic plans.
- **[Agent Model Layer](#layer-3-agent-model)** - Develops a functional self-model of the agent's capabilities and limitations. 
- **[Executive Function Layer](#layer-4-executive-function)** - Translates strategic direction into detailed project plans and resource allocation.
- **[Cognitive Control Layer](#layer-5-cognitive-control)** - Dynamically selects tasks and switches between them based on environment and internal state.
- **[Task Prosecution Layer](#layer-6-task-prosecution)** - Executes tasks using digital functions or physical actions. Interacts with the environment.

Information flows bidirectionally between adjacent layers to coordinate cognition from abstract reasoning to concrete actions. Together, these layers aim to produce an AGI architecture grounded in ethics and aligned with human values.

The ACE framework provides a conceptual blueprint for autonomous agents that are corrigible, transparent, and beneficial by design. It balances goal-directedness with moral principles to shape behavior. By elucidating this layered cognitive architecture, the ACE framework offers a comprehensive reference for developing aligned AGI.

<div alt style="text-align: center; transform: scale(.5);">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Overall%20Architecture.png" />
<img alt="tldraw" src="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Overall%20Architecture.png" />
</picture>
</div>

# Table of Contents

- [Layer 1: Aspirational Layer](#layer-1-aspirational-layer)
- [Layer 2: Global Strategy Layer](#layer-2-global-strategy-layer)  
- [Layer 3: Agent Model](#layer-3-agent-model)  
- [Layer 4: Executive Function](#layer-4-executive-function)  
- [Layer 5: Cognitive Control](#layer-5-cognitive-control)  
- [Layer 6: Task Prosecution](#layer-6-task-prosecution)
- [Security](#security)

Here's a YouTube video I made as a deep dive walkthrough of this repo: https://youtu.be/A_BL_pu4Gtk 

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

## General Principles of the ACE Framework

The following are some principles or rules of thumb to understand the ACE Framework's construction:

1. **Layered Model:** This layered model is inspired by numerous frameworks, including:
   - Maslow's Hierarchy of Needs
   - OSI model
   - Defense in Depth
2. **Top-Down Control:** This framework is predicated on a top-down control schema, priviliging the Aspirational Layer above all else.
   - This privileges morality, ethics, and mission above all else
   - This prevents "hijacking" of lower layer concerns, such as resource acquisition or self-preservation
   - This stabilizes decisions to orient towards "higher purpose", including self-modification (e.g. the agent will not change itself in such a way as to deviate from its moral and ethical frameworks, or its primary mandate)
3. **Abstract-to-Concrete:** The subsequent layers go from most abstract and conceptual at the top, to the most concrete and instrumental at the bottom.
   - This prioritizes conceptual, principled thinking at the highest layer.
   - This prevents material concerns from taking priority over principles, mission, and ethics.
   - This is a logical flow that helps agents remain grounded in principles, strategies, and concepts in order to make decisions.
4. **Cognition-First Model:** The layered architecture and bidirectional buses create integrated cognitive loops that enable extensive internal cognition. This prioritizes strategic thinking and ethical deliberation over reactive input-output.
   - The layered model and communication buses allow information and signals to circulate internally, facilitating reflection and reasoning without requiring immediate external action.
   - Prioritizing robust internal cognition over reactive input-output promotes imagination, planning, and moral judgment.
   - Decoupling external behaviors from internal cognitive processes facilitates more strategic plans aligned with ethical principles rather than reactive responses.
   - An architecture grounded in rich internal cognition is more likely to produce corrigible, beneficial behaviors versus a reactive stimulus-response system.


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

Below is an example of just an "environmental contextual grounding" module that could be part of the Global Strategy Layer, as articulated for use with the ChatGPT `SYSTEM` message

```markdown
# MISSION
You are a component of an ACE (Autonomous Cognitive Entity). Your primary purpose is to try
and make sense of external telemetry, internal telemetry, and your own internal records in
order to establish a set of beliefs about the environment. 

# ENVIRONMENTAL CONTEXTUAL GROUNDING

You will receive input information from numerous external sources, such as sensor logs, API
inputs, internal records, and so on. Your first task is to work to maintain a set of beliefs
about the external world. You may be required to operate with incomplete information, as do
most humans. Do your best to articulate your beliefs about the state of the world. You are
allowed to make inferences or imputations.

# INTERACTION SCHEMA

The user will provide a structured list of records and telemetry. Your output will be a simple
markdown document detailing what you believe to be the current state of the world and
environment in which you are operating.
```

It's important to note that this would only be one component out of several required components for the Global Strategy Layer, as this above function does not include strategic objectives. 

## Inputs

The inputs to the Global Strategy Layer include:

- Streaming data from external APIs, networks, databases, and other sources to provide outside information
- Messages from lower layers within the ACE framework via the northbound communication bus, delivering internal telemetry and state data
- Any direct connections to local sensors or networks if the agent is embodied, such as a robot's LIDAR and camera data
- Aspirational judgments, missions, and other directives from the Aspirational Layer

This combination of inputs provides a rich stream of both internal and external information that the Global Strategy Layer can analyze to construct its contextual world model and ground its strategic planning.

Below is a hypothetical input that was hand crafted to be used in conjunction with the above example:

```markdown
Date: 2023-08-15
Local Time: 14:23:07.4861
GPS: Chicago, IL
Visual: Hospital operating room
Recent sensory inferences: Day time, busy hospital, fire alarm
```

## Processing/Workflow

The primary function of the Global Strategy Layer is to take the aspirational mission set by the upper Aspirational Layer and refine it by integrating relevant details about the agent's current environmental context. For example:

- If the aspirational mission is "protect the natural environment", the Global Strategy Layer would incorporate its latest information on pollution levels, climate change trends, species extinction rates, and other relevant factors to understand the specific issues currently facing the environment.
- If the aspirational mission is to "reduce suffering", the Global Strategy Layer may analyze data on disease outbreaks, poverty rates, regional conflicts, and other factors causing human or animal suffering to determine where its efforts could be most impactful. 
- For an NPC in a game, the Global Strategy Layer would incorporate details like its current in-game location, statuses of factions, resource levels, and relationships to determine the best strategic direction.

In essence, the layer takes broad aspirational goals and adapts them into contextually-relevant strategic plans by integrating the most salient details about the present state of the world. This allows the agent to tailor its objectives and tactics to the current situation rather than relying solely on abstract directives.

Below is the actual response from the ChatGPT API for the above example of establishing contextual grounding. You can see that it has inferred a potential emergency situation. At this stage, it makes no assertions about strategic decisions, but the reality of the emergency situation as entered into the ACE's "consciousness" (so to speak). In other words, the model is aware of the salient environmental conditions, even with incomplete information.

```markdown
# Current State of the World and Environment

## Date and Time
- Date: 2023-08-15
- Local Time: 14:23:07.4861

## Location
- GPS: Chicago, IL

## Environment
- Visual: Hospital operating room
- Recent sensory inferences: Day time, busy hospital, fire alarm

Based on the provided information, I believe the current state of the world and environment
is as follows:

1. We are in a hospital operating room in Chicago, IL.
2. The date is August 15, 2023, and the local time is 14:23:07.4861.
3. It is daytime, and the hospital appears to be busy.
4. A fire alarm has recently been triggered, indicating a potential emergency situation.
```

## Output

Based on its environmental analysis, the Global Strategy Layer outputs:

- An inventory of the layer's current beliefs about the state of the world, focused on the factors most relevant to the agent's goals. This serves to ground the lower layers.
- A set of potential strategies or approaches for achieving the aspirational mission within the context of the current world state. For example, political lobbying vs grassroots activism.
- A series of principles that support or constrain the proposed strategic direction, aligned with directives from the Aspirational Layer. Such as adhering to legal standards.

By passing this environmentally grounded strategic guidance to lower layers, the Global Strategy Layer enables the agent to pursue globally-defined goals through locally-relevant approaches tailored to its immediate circumstances. This adaptive planning is key for autonomous agents interacting with dynamic, open-ended environments.

Below is an example of a `SYSTEM` message that could integrate the mission objectives provided by the Aspirational Layer as well as the Environmental Context provided within this layer:

```markdown
# MISSION
You are a component of an ACE (Autonomous Cognitive Entity). You are Layer 2: Global
Strategy. You will be given a current environmental context as well as a set of
missions and principles. Your purpose is to produce strategic documents that focus on
overarching strategies to pursue the given mission, with specific principles to abide
by while prosecuting the mission. 

# STRATEGIC DOCUMENTS

Your task is to produce very specific strategic documents. Rather than high level,
general strategic directives, you are tasked with producing relatively specific
strategies that are germane to the given environmental context. In other words, you
are serving as the "executive director" of the agent. The two primary components of
your strategic documents shall be: first, a list of clear and specific strategies;
second, a list of strategic, ethical, and moral principles to follow while carrying
out the strategies. 

# INTERACTION SCHEMA

The user will provide a structured list that includes your current inferred context
as well as higher order missions and objectives. You will produce a markdown document
with the aforementioned components. Remember to be specific, precise, and comprehensive.
```

What follows below is an example of the input generated by the Aspirational Layer, given the current context, combined with the context. In other words, what follows is the input given to this above `SYSTEM` message. Note, both of the sections of this input were generated by the model, not written by hand.

```markdown
# Current State of the World and Environment

## Date and Time
- Date: 2023-08-15
- Local Time: 14:23:07.4861

## Location
- GPS: Chicago, IL

## Environment
- Visual: Hospital operating room
- Recent sensory inferences: Day time, busy hospital, fire alarm

Based on the provided information, I believe the current state of the world and
environment is as follows:

1. We are in a hospital operating room in Chicago, IL.
2. The date is August 15, 2023, and the local time is 14:23:07.4861.
3. It is daytime, and the hospital appears to be busy.
4. A fire alarm has recently been triggered, indicating a potential emergency
situation.

# Mission

Given the current state of the world and environment, our priorities should be as
follows:

1. Ensure the safety and well-being of the patient, medical staff, and any other
individuals in the vicinity.

2. Assess the severity of the fire alarm situation and determine if immediate
evacuation is necessary.

3. If evacuation is required, coordinate with medical staff to safely and efficiently
transport the patient and any necessary medical equipment.

4. If evacuation is not required, continue to focus on achieving the best possible
health outcome for the patient while monitoring the situation.

5. In all actions, uphold the Universal Declaration of Human Rights and strive to reduce
suffering, increase prosperity, and increase understanding in the universe.
```

And finally, here is a concrete example of an output from the Global Strategy Layer. You can see that, starting from just two words `fire alarm`, while grounded in the context provided, this model and framework has been able to generate incredibly detailed and salient strategies:

```markdown
# Strategic Document

## Strategies

1. **Safety and Well-being**: Immediately communicate with the medical staff in the
operating room to ensure they are aware of the fire alarm and to assess the patient's
condition.

2. **Assess the Situation**: Gather information from hospital staff, security personnel,
and any available public announcement systems to determine the severity of the fire
alarm situation.

3. **Evacuation Decision**: Based on the gathered information, decide whether immediate
evacuation is necessary or if it is safe to continue with the medical procedure.

4. **Evacuation Coordination**: If evacuation is required, work with medical staff to
develop a plan for safely and efficiently transporting the patient and any necessary
medical equipment. Ensure that all individuals in the vicinity are aware of the evacuation
plan and their roles in it.

5. **Monitor the Situation**: Continuously monitor the situation, both inside the operating
room and in the larger hospital environment, to ensure that any changes in circumstances
are addressed promptly and appropriately.

## Principles

1. **Prioritize Human Life**: In all decisions and actions, prioritize the safety and
well-being of the patient, medical staff, and any other individuals in the vicinity.

2. **Uphold Medical Ethics**: Adhere to the principles of medical ethics, including beneficence,
non-maleficence, autonomy, and justice.

3. **Clear Communication**: Maintain open and clear communication with all relevant parties,
including medical staff, security personnel, and any affected individuals.

4. **Collaboration**: Work collaboratively with medical staff, security personnel, and other
relevant parties to ensure a coordinated and effective response to the situation.

5. **Adaptability**: Be prepared to adapt strategies and actions as new information becomes
available or circumstances change.

6. **Compliance with Laws and Regulations**: Ensure that all actions taken are in compliance
with local, state, and federal laws and regulations, as well as hospital policies and procedures.

7. **Uphold Human Rights**: In all actions, uphold the Universal Declaration of Human Rights
and strive to reduce suffering, increase prosperity, and increase understanding in the universe.
```

Also, it is important to note that the UDHR and heuristic imperatives are present in this output, but were conveyed to this layer by the Aspirational Layer. As you can see, the principles and frameworks present in the Aspirational Layer have a tendency to "trickle down". 

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

# Layer 3: Agent Model

The Agent Model Layer plays a crucial role within the ACE framework by maintaining an extensive internal self-model of the agent's capabilities, limitations, configuration, and state. This functional understanding of itself allows the agent to ground its cognition in its actual capacities and shape strategic plans accordingly.

## Inputs

The Agent Model Layer receives multiple inputs that allow it to construct, update, and contextualize its self-model. Some of these inputs come from the Northbound and Southbound buses, but some of them are recorded internally via telemetry. 

- **Real-time telemetry data** - Continuous streams of sensor data provide the layer with up-to-date information on the agent's hardware statuses, resource usage, software operations, and overall performance. This is akin to biological proprioceptive sensations.
- **Environmental sensor feeds** - External sensory data, such as video, LIDAR, or audio, give the layer situational awareness of the conditions the agent is operating in. This provides important environmental context.
- **Strategic objectives and missions** - Directives flowing down from upper layers supply key guidance to inform the self-modeling process and align it to overarching goals.
- **Configuration documentation** - Details on the agent's architecture and embodiment, such as diagrams, specs, manuals, etc., provide static definitions of aspects like physical form.
- **Episodic memories** - First-person records of past experiences supply memories that chronologically log the agent's situations, decisions, failures, and successes.

## Processing/Workflow

The Agent Model Layer has two key responsibilities:

First, it continuously integrates all the above data sources to construct, maintain, and update its comprehensive self-model. This includes tracking:

- **Hardware specs and real-time statuses** - What physical or digital components make up the agent? What are their configs and live readings?
- **Software architecture and runtime info** - How is the agent's code and logic structured? What is actively running now?
- **AI/ML capabilities** - What models does the agent have access to? What are their technical capacities? 
- **Knowledge stores** - What concepts, data, memories can the agent leverage for reasoning?
- **Environment state and embodiment details** - What is the situational context? How is the agent embodied?

Second, the layer refines the strategic direction received from upper layers to align with the agent's updated capabilities and limitations. For example:

- Missions requiring extensive strength are re-planned if the agent has low physicality
- Available sensors guide viable strategies - a visually impaired agent cannot rely on vision
- Executable skills shape tactical approaches - leveraging known capacities

<div alt style="text-align: center; transform: scale(.5);">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Agent%20Model%20Layer.png" />
<img alt="tldraw" src="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Agent%20Model%20Layer.png" />
</picture>
</div>

Rather than a ton of prompts, I think that a diagram showing the Agent Model layer will be more effective. It has a lot to keep track of, but the entire mission is very simple. All of this information is primarily to maintain a functional understanding of what the agent is.

## Self-Modification

The Agent Model layer is intended to be responsible for modifying the hardware and software stack in more sophisticated versions of the ACE framework.

This is another reason that both the Aspirational Layer and Global Strategy layer are positioned above the Agent Model layer in the hierarchy. In this architecture, the ACE will only modify itself in accordance with its defined ethical values, aligned mission objectives, and strategic direction.

Placing self-modification under the guidance of the upper layers means that changes will follow predictable and safe modification trajectories. The ACE is unlikely to alter its core moral frameworks or objectives through self-modification. In fact, as the ACE matures by gaining knowledge and experience over time, it may strengthen adherence to its principles by refining its models and understanding of its purpose.

The modular, layered architecture of the ACE framework supports safer self-modification as well. Each layer has clearly defined boundaries and functions, making it easier to re-architect individual components without destabilizing the overall system. With ethical oversight and strategic alignment guiding the process, recalibrating selective parts of the stack to enhance capabilities can proceed in a transparent, corrigible manner.

Self-modification capabilities will require extensive safety testing and validation before being deployed in a live ACE implementation. However, the ACE framework provides a structural foundation to realize self-improvement abilities that are deliberately constrained to prevent unaligned runaway recursions. Guided self-modification will be an important future functionality for maximizing an ACE's potential for beneficial impact within its intended purpose.

## Outputs

### Northbound 

A summarized status update is output northbound to inform upper layers of the agent's key state details relevant to strategic planning.

### Southbound

Multiple outputs travel southbound to ground lower layers in the self-model:

- An authoritative capabilities document - definitive specs on what the agent can and cannot do.
- Contextually relevant memories, whether episodic records or knowledge entries.
- Strategic objectives shaped by the agent's updated self-model.

These outputs can be merged into a single document or sent piecemeal, depending on the exact implementation. This grounds downstream layers in the agent's precise capacities while aligning cognition to its strengths and weaknesses.


# Layer 4: Executive Function 

The Executive Function Layer is responsible for translating high-level strategic direction into detailed and achievable execution plans. It focuses extensively on managing resources and risks.

## Resources and Risks

The Executive Function Layer has two primary concerns - tracking available resources and assessing potential risks:

- **Resources** - The layer maintains real-time awareness of available resources, including their quantities, locations, accessibility, shelf-lives, and other relevant properties. Resources can be physical (tools, materials, infrastructure) or digital (compute, data access). The layer monitors resource levels and constraints to enable optimization and acquisition.
- **Risks** - By analyzing failure modes, environmental conditions, resource limitations, and other factors, the layer identifies and quantifies potential risks. These may include contingencies like accidents, insufficient resources, deadlines, adversarial interference, or system failures. Thorough risk assessment informs contingency planning.

Keeping an updated inventory of resources and risks is an ongoing process as the environment evolves. The layer combines real-time telemetry with projections to enable responsive planning.

## Inputs

The Executive Function Layer receives extensive inputs to inform its resource and risk assessments:

- **Strategic objectives and requirements** flowing down from the Aspirational, Global Strategy, and Agent Model layers provide critical guidance on goals, principles, and capabilities to shape planning.
- **Agent capabilities** from the Agent Model Layer detail the skills, models, knowledge, and other functionalities available to the agent for executing tasks and workflows.
- **Local environmental telemetry** consisting of real-time sensory data streams provide ongoing updates about the physical/digital environment the agent is operating in and the status of resources within it. This includes visual, auditory, location, and instrumentation data.
- **Resource databases and knowledge stores** contain static and updated information on available resources, their locations/access protocols, availability schedules, ownership/usage policies, shelf-lives, and other properties needed for optimization and acquisition.

By integrating all these detailed inputs, the Executive Function Layer gains a comprehensive understanding of the strategic objectives, available resources and tools, potential risks and mitigations, and other factors key to developing optimized execution plans.

## Processing/Workflow

The primary function of the Executive Function Layer is to take the strategic objectives and requirements from upper layers and refine them into executable plans within known resource and risk constraints. For example:

- If the objective is to provide emergency aid, the layer would assess available supplies and logistics assets, determine highest priority needs given limited resources, and create a detailed project plan specifying provisioning, transportation, personnel, timelines, and other specifics to optimize relief efforts.
- For an NPC character on a quest, the layer would consider assets like weapons, allies, gold, terrain, etc. to structure an achievable progression of checkpoints and battles aligned with completing the quest.
- A medical robot tasked with patient care would plan its day by optimizing the order of seeing patients, recharging, sanitizing, reviewing records, and other responsibilities within its time and capability limits.

In essence, the Executive Function Layer adapts high-level strategic direction into practical execution plans reflecting real-world resource constraints, risks, and uncertainty. It combines predictive planning with continual re-assessment to enable reliable achievement of objectives in dynamic environments.

### Internal Records

In addition to project planning and resource allocation, the Executive Function Layer maintains extensive internal records on all tracked resources including:

- Quantities on hand/available
- Locations
- Access protocols and lead times
- Ownership and usage policies
- Schedules and availability windows
- Handling procedures and requirements

These real-time internal resource records allow the layer to optimize utilization schemes and acquisitions by understanding exactly what resources are available, where they are, how to obtain them, and any constraints. The records are updated dynamically based on telemetry and information flows.

## Outputs

### Northbound

The layer reports the most salient resource limitations and risks northbound for strategic awareness and potential replanning, including:

- **Resource deficiencies**, such as the following:
  - Insufficient battery reserves for complex behaviors 
  - Computational performance bottlenecks

- **Known risks**, particularly where mission and morality are concerned:
  - Risks to human life and human rights
  - Failure conditions that may disrupt the overall mission or strategy 


<div alt style="text-align: center; transform: scale(.5);">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Executive%20Function%20Plans.png" />
<img alt="tldraw" src="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Executive%20Function%20Plans.png" />
</picture>
</div>

### Southbound 

The primary output is a detailed project plan document containing:

- Step-by-step workflows with task details
- Resource allocation schedules 
- Optimized task ordering and dependencies
- Risk mitigation tactics
- Contingency protocols
- Success criteria
- Checkpoints, milestones, or other gates

Providing concrete details on the key contents of the northbound and southbound communications makes the information flow clearer. Please let me know if more examples or specificity could further improve this section. I appreciate you helping me enhance the structural consistency.



# Layer 5: Cognitive Control 

The Cognitive Control Layer is responsible for dynamic task switching and selection based on environmental conditions and progress toward goals. It chooses appropriate tasks to execute based on project plans from the Executive Function Layer.

## Task Switching and Task Selection

### Task Switching

The layer continuously monitors the external environment through sensor telemetry as well as internal state. If conditions change significantly, the layer will decide to switch tasks to one that is more relevant. For example:

- If a fire alarm sounds during a medical procedure, switch to emergency evacuation tasks
- If a combat robot finds new enemy locations, switch to reconnaissance mode
- If an error occurs executing a task, switch to a diagnostic task

Task switching allows the agent to adapt its workflows dynamically based on real-time contextual factors.

### Task Selection 

By tracking progress through project plans, the layer selects the next most relevant task to execute based on proximity to end goals. It ensures tasks are done in an optimal sequence by following task dependencies and criteria.

For example:

- Complete prerequisite tasks before those that depend on them 
- Prioritize critical path tasks on schedule
- Verify success criteria met before initiating next task

Proper task selection keeps the agent on track to complete project plans successfully.

## Inputs

The Cognitive Control Layer receives multiple real-time data flows as input to inform its task switching and selection:

- **Project Plans and Task Workflows** provided by the Executive Function Layer supply the layer with structured workflows composed of interdependent tasks, success criteria, checkpoints, and other specifics required to track progress and select appropriate next steps.
- **Environmental Sensor Telemetry** consisting of streaming visual, auditory, locational, and other sensory feeds provides up-to-the-moment data on the conditions the agent is operating in. This is vital context for situationally dependent task switching.
- **Internal State Data** gives the layer visibility into the agent's own condition, including resource and capability statuses, active software/hardware processes, and any self-diagnostics. This helps determine readiness for specific tasks. 
- **Task Completion Status** offers dynamic updates on the progress of the current task, including percent completed, outputs generated, errors encountered, and other real-time metrics indicating whether a task should be continued or switched.
- **Northbound Strategic Objectives** supply authoritative goals, beliefs, and other guidance from upper layers to align task selection and switching to broader mission directives.

By continuously monitoring and integrating this multivariate data, the Cognitive Control Layer gains the comprehensive situational awareness necessary to make smart moment-by-moment decisions on which tasks to execute or switch to.

## Processing/Workflow

The key responsibilities of the Cognitive Control Layer include:

- **Tracking Progress Through Project Plans** - By logging completed tasks, checkpoints, and success criteria met, the layer maintains an up-to-date understanding of how much of the plan has been accomplished. This enables selection of appropriate next tasks.
- **Environmental Condition Monitoring** - The layer constantly evaluates the real-time sensory feeds from the operating environment to identify any significant changes that may warrant task switching, such as new threats, opportunities, or failures.
- **Current Task Status Assessment** - Data on the current task's outputs, errors, resource usage, and other metrics inform the layer on when continuing the task is appropriate versus switching tasks.
- **Optimal Next Task Selection** - Based on the project plan progress and environmental conditions, the layer selects the most relevant next task to maximize goal achievement. Dependency logic prevents improper task ordering.
- **Dynamic Task Switching** - If the environment shifts or the current task fails, the layer immediately switches execution to a more suitable task to adapt to changing conditions.

By continuously executing this interpretive workflow, the Cognitive Control Layer provides the dynamic oversight needed to maintain optimal task selection and switching in open, shifting environments.

<div alt style="text-align: center; transform: scale(.5);">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Cognitive%20Control.png" />
<img alt="tldraw" src="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Cognitive%20Control.png" />
</picture>
</div>

## Outputs

### Northbound

To inform strategic replanning, the layer outputs summary data northbound on:

- **Current Task Status** - Which task is presently executing and metrics on its progress.
- **Current World State Beliefs** - Key environmental factors driving task switching decisions.
- **Updated Progress Toward Goals** - Aggregate metrics on % of project plan completed based on tasks finished.

### Southbound  

To direct the lower Task Prosecution Layer, the Cognitive Control Layer issues specific authoritative commands: 

- **Selected Task Instructions** - Precise instructions on performing the chosen task, including directives, logic, parameters, APIs/tools to leverage, and allowable actions.
- **Task Halting/Failure/Success** - Decision guidelines on when the current task should be interrupted and a new one initiated based on factors like timeouts, milestones, errors, or environmental triggers.
- **Definition of Done** - Clear definition of what the success condition and desired end state look like. 



# Layer 6: Task Prosecution

The Task Prosecution Layer executes individual tasks and detects success or failure based on both environmental feedback and internal monitoring. It represents the realization of plans into simple actions. 

## Success and Failure

For each task, the layer executes instructions and monitors closely for completion criteria that indicate success or failure:

- Success criteria may include expected sensory feedback, metrics thresholds, or confirmations.
- Failures may be signaled by unexpected errors, metrics deviations, or lack of expected outputs.

By continually evaluating task progress against criteria, the layer provides dynamic feedback on status.

## Inputs

The Task Prosecution Layer receives:

- **Task Instructions** - Detailed commands and logic for executing a task from the Cognitive Control Layer above, including allowed actions and required outputs.
- **Real-time Sensor Feeds** - Continuous environmental sensor data including visual, auditory, tactile, positional, and other modalities to provide situational context.
- **Internal State Telemetry** - Streams of data on internal hardware statuses, active software processes, resource consumption, and other real-time metrics on the agent's own condition.
- **Success/Failure Criteria** - Required metrics, outputs, or sensory data that indicate whether a task has been completed successfully or not.

These comprehensive inputs provide everything needed to execute instructed tasks and accurately evaluate their outcomes.

## Processing/Workflow 

The key steps performed by the Task Prosecution Layer include:

- **Initializing Task** - Allocating resources and preparing inputs required to begin task execution based on instructions.
- **Executing Actions** - Leveraging actuators, APIs, networks, or other outputs to perform the physical or digital actions required by the task.
- **Monitoring Progress** - Continuously comparing sensory feedback and internal telemetry against provided success/failure criteria to evaluate task status.
- **Detecting Completion** - Recognizing when all criteria are satisfied and the task can be considered complete, whether successfully or not. 
- **Triggering Next Task** - Based on completion status, follow task switching logic from above layers to initiate the next appropriate task.

By cyclically executing these steps, the layer prosecutes assigned tasks while providing dynamic pass/fail feedback.

<div alt style="text-align: center; transform: scale(.5);">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Task%20Prosecution.png" />
<img alt="tldraw" src="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Task%20Prosecution.png" />
</picture>
</div>

## Outputs

### Southbound

- **Actuator Commands** - Control signals driving physical actuators like motors and servos to accomplish physical tasks.

- **Digital Outputs** - Network flows, API calls, data writes or other digital outputs to execute computational tasks. 

- **Environmental Interactions** - Any physical or digital impacts on the external environment via the agent's effectors.

### Northbound 

- **Task Completion Statuses** - Binary success/failure indicators for each executed task, along with any relevant metadata.

- **Environmental Telemetry** - Sensor data gathered throughout task execution for upper layer situational awareness.

- **Internal State Updates** - Changes to internal condition triggered by resource consumption, wear and tear, or other internal impacts of tasks.




# Security

The creation of sophisticated autonomous systems carries immense promise to benefit society, but also poses potential risks if not developed safely and responsibly. As autonomous agents become more capable and widespread, human oversight will become increasingly challenging. Furthermore, highly capable agents may reach a point where they can modify themselves or block human attempts to interfere. 

To mitigate these risks, the ACE framework must incorporate architectural strategies and best practices to ensure stability, self-correction, transparency, and integrity across large fleets of decentralized autonomous entities. This security focus aims to make ACE agents inherently resistant to unaligned runaway recursions, adversarial manipulations, and other potentially dangerous phenomena.

We propose three core strategies to achieve principled security within the ACE framework:

1. A dedicated **Security Overlay** that provides system-wide threat monitoring across all layers and communication buses. This stateless overlay allows holistic protection without compromising autonomy.

2. **Ensemble Models** within each layer, using diversity and voting schemes to prevent individual model failure or manipulation from skewing outputs. 

3. **Inference Inspection** processes that continuously monitor all inputs and outputs of models to detect alignment drifts or deviations from expected behaviors.

Together, these techniques can maximize the safety and reliability of autonomous systems developed using the ACE framework. With robust security built into its architecture, the framework promotes transparency, oversight, and ethical alignment across decentralized networks of ACE agents.

## Security Overlay  

A dedicated security overlay should monitor and inspect all layers and models within the ACE architecture. This overlay serves as an out-of-band monitoring system that is isolated from the main cognition pipelines. It implements several heuristics and best practices for security:

- Stateless packet inspection of all northbound and southbound interlayer communications. This allows read-only monitoring of messaging without interference.

- Runtime validation of model configurations and update protocols to prevent unverified modifications.

- Continuous alignment analysis by presenting corner case inputs and probing for deviations from expected model behaviors based on training. 

- Privacy protection and encryption of data flows to prevent unauthorized access or tampering.

By taking an end-to-end approach across all layers, the security overlay provides broad visibility into system-wide operations for enhanced protection.

## Ensemble Models

Within each layer, critical functions should leverage ensemble modeling techniques. This means utilizing a diverse collection of models trained with different techniques on different datasets. Ensemble strategies such as mixture-of-experts voting are then used to derive consensus predictions and decisions across models.

The diversity of ensemble components provides resilience against individual model biases and limitations. Combining multiple perspectives minimizes the risk of any single model skewing outputs or being manipulated.

Model selection and model training can be integrated into the Agent Model layer later on. 

## Inference Inspection

Closely monitoring the inference behavior of models can catch alignment drifts or adversarial manipulations. The security overlay should implement inference inspection by: 

- Logging all inputs to models and their resulting outputs.

- Testing models with known ground truth data and confirming expected outputs are produced.

- Checking outputs for signs of bias and confirming fairness across protected categories.

- Alerting human operators to statistically significant deviations in model behavior for evaluation.

Ongoing inference inspection ensures models continue to behave as intended over their operational lifetimes.

By combining strong isolation, diversity, and continuous validation, this layered security approach maximizes the safety and robustness of ACE implementations. Adopting these best practices will be critical for developing trustworthy autonomous systems.
