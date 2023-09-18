# ACE Agile Chart

## Roles

- **Product Owner:** Dave
  - Sets overall requirements and acceptance criteria
  - Writes user stories, roadmap, etc
- **Scrum Master:** ???
  - Primary stakeholder responsible for process
  - Communicates with product owner (creates boundary)
- **Lead Developer:** ???
  - Senior-most developer (or one with most relevant experience
  - Responsible for major architectural decisions, etc

## MVP/POC

The purpose of the ACE Framework MVP is to create a small "toy" example of the ACE Framework primarily as demonstration purposes. In other words, this is a super simple implementation to show "Hey look, it actually works."

The idea here is that we will probably also learn valuable lessons before we scale up to multi-agent deployments or more involved environments. For instance, we will probably want to solve a bunch of API and architectural problems before we try to build ACE agents that control robots or interact in complex social environments. 

### Acceptance Criteria

1. **Python:** Must be Python-native or at least mostly Python. This is to maximize for accessibility and learning. Thus we should avoid too many exotic requirements, such as other servers or interpreters. 
2. **Hackable:** Must be optimized for easy copy/pasta and/or tinkering. Hackability will increase immediate utility and adoption. It will also make it easier for people to poke and modify. Furthermore, by starting with a "hackability" mindset, this will set the stage for polymorphic implementations later. 
3. **Simple & Easy:** Must be relatively easy to setup and deploy. Ideally, little more than `pip install -r requirements.txt` followed by `python ace.py` or something like that. Again, this is to maximize uptake for people such as novices and college students. Future versions can be more involved, such as with containers and such.
4. **Visual:** Must have some kind of visual (PyGame, Web UI, Tkinter, whatever) that can give users at least a little "peek under the hood" plus some intuitive usability. Ideally it would ultimately have some kind of audiovisual avatar, but this is more of a long-term idea. 
5. **Full ACE:** Must implement all six layers and both buses with clear dilineations and demarcations. In other words, it must be a true and full implementation of the ACE Framework. 

## Roadmap

- MVP
  - Toy, demo example, easy to learn on
  - Learn lessons, overcome problems, refine architecture, document as we go
  - Get something mostly as a simple proof of concept
- Release 1 - Robustness
  - Refactor with lessons learned
  - Increase robustness and resilience
  - **Refine architecture, establish best practices**
- Release 2 - Configurability
  - Focus on flexibility and configurability e.g. **ACE just needs a few config changes and the entire purpose changes**
  - Remember, hackability means easier to become polymorphic!
  - Everything defined as some JSON or YAML files? Dunno
- Release 3 - Extensibility
  - Focus on spontaneous extension of hardware and/or software capabilities
  - Plug and play architecture? (Find and use new tools, APIs, etc)
- Release 4 - Deployability
  - Focus on **"anywhere, anytime"** mentality
  - Create kernels that can run in any container, any environment, thus can be used for games, robots, enterprise agents, etc
- Release 5 - Polymorphic
  - Focus on self-modification (e.g. self-configuration, self-extension, etc)
  - Self-transforming in order to better pursue aspirations
