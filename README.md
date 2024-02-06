# Project Principles

## Exclusively Open Source

We will be committed to using 100% open source software (OSS) for this project. This is to ensure maximum accessibility and democratic access.

## Exclusively Local Hardware

No cloud or SaaS providers. This constrains the project to run locally on servers, desktops, laptops, smart home, and portable devices. 

## Principles

### 1. Be Scrappy
Don't wait for permission or controls. This is a purely volunteer group so if something resonates, go for it. Experiment. Try stuff. Break stuff. Share your results. Use your own sandboxes, report results, and together we'll decide what get's pulled into MAIN via pull request. But as one member said: we need more data! So the principle here is to engage in activities that generate more data, more telemetry, so we can see and feel what's working and what isn't. 

### 2. Avoid Vendor Lockin
While we generally agree we want to be model agnostic, but acknowledge there are problems with this, the overarching principle is that we don't want to get locked into working with any single vendor. OpenAI in particular. This means we tinker with multiple providers, vendors, models, etc. This also means a preference for Open Source wherever possible. This general principle covers several areas.

### 3. Task-Constrained Approach
The team acknowledges that the tasks the framework can accomplish are constrained by the capabilities provided to it. Identifying the potential task space is critical, and the framework should be designed with the types of tasks it should be able to accomplish in mind. This means that milestones and capabilities should be measured by tests and tasks so that we can remain empirical and objective oriented.

### 4. Avoiding Overcomplication
The team agrees on the importance of not overcomplicating the project from the start. Modest milestones and a focus on what is feasible are recommended. As we're doing nothing short of aiming for fully autonomous software, we need to not "boil the ocean" or "eat the whole elephant." Small, incremental steps while keeping the grand vision in mind. 

### 5. Establish New Principles
We're exploring an entirely new domain of software architecture and design. Some old paradigms will obviously still apply, but some won't. Thus, we are discovering and deriving new principles of autonomous software design as we go. This adds a layer of complexity to our task. 


# Intro to this Repo

This is the main public repo for the ACE (Autonomous Cognitive Entity) repository.

> If you're looking for the main ACE Framework documentation, it is available here: https://github.com/daveshap/ACE_Framework/blob/main/ACE_Framework.md

## Participation

Please check out the following files and locations for more details about participation:

1. Contributing: https://github.com/daveshap/ACE_Framework/blob/main/contributing.md
   - This page will be updated with the best ways to contribute
2. Agile: https://github.com/daveshap/ACE_Framework/blob/main/agile.md
   - This is the overall roadmap and organizational document
3. Discussions: https://github.com/daveshap/ACE_Framework/discussions
   - Jump into the discussions! 

We also have a Public Discord. Keep in mind that this repo is the Single Source of Truth! Discord is just for convenience. If it's not on the repo, it doesn't exist! Join the Autonomous AI Lab here: https://discord.gg/mJKUYNm8qY

<div alt style="text-align: center; transform: scale(.5);">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Overall%20Architecture.png" />
<img alt="tldraw" src="https://raw.githubusercontent.com/daveshap/ACE_Framework/main/images/ACE%20Framework%20Overall%20Architecture.png" />
</picture>
</div>

## Projects

There are many possible implementations of the ACE Framework. Rather than detail every possible permutation, here is a list of categories that we perceive as likely and viable.

1. **Personal Assistant and/or Companion**
   - This is a self-contained version of ACE that is intended to interact with one user. 
   - Think of Cortana from HALO, Samantha from HER, or Joi from Blade Runner 2049. (yes, we recognize these are all sexualized female avatars)
   - The idea would be to create something that is effectively a personal Executive Assistant that is able to coordinate, plan, research, and solve problems for you.
   - This could be deployed on mobile, smart home devices, laptops, or web sites.
2. **Game World NPC's**
   - This is a kind of game character that has their own personality, motivations, agenda, and objectives. Furthermore, they would have their own unique memories.
   - This can give NPCs a much more realistic ability to pursue their own objectives, which should make game experiences much more dynamic and unpredictable, thus raising novelty.
   - These can be adapted to 2D or 3D game engines such as PyGame, Unity, or Unreal.
3. **Autonomous Employee**
   - This is a version of the ACE that is meant to carry out meaningful and productive work inside a corporation.
   - Whether this is a digital CSR or backoffice worker depends on the deployment.
   - It could also be a "digital team member" that primarily interacts via Discord, Slack, or Microsoft Teams.
4. **Embodied Robot**
   - The ACE Framework is ideal to create self-contained, autonomous machines.
   - Whether they are domestic aid robots or something like WALL-E
