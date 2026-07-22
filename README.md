# Owen Schoeniger

I build developer tools and learning systems that help people and agents do difficult work without guessing.

I was a teacher before I was an engineer. Teaching led me through 3D printing, manufacturing, and industrial technology. The throughline is the same: make the system understandable, make the dangerous boundaries explicit, and give the learner evidence they can inspect.

## Start with TrashPal

[TrashPal](https://github.com/owieschon/trashpal) is the best single example of how I build and teach: a bounded agent investigates one service exception and drafts a cited recovery, while deterministic code owns approval, execution, recovery, and proof. It was distilled from [self-driving-trash-palace](https://github.com/owieschon/self-driving-trash-palace), the fuller build, which carries the deeper knowledge graph, evaluation harness, and architecture decisions if you want them.

The short version: the model can propose. Host code owns authority. Durable records and independent verification decide what happened. People and agents learn from the same hash-pinned knowledge graph.

## One upstream contribution

[PostHog Wizard Workbench PR #2754](https://github.com/PostHog/wizard-workbench/pull/2754) added the core of a project-detection evaluator inside another team's architecture. The maintainer chose to carry its fixtures and evaluation ideas into a broader agent-and-skill-driven direction. That interaction is useful evidence of how I prefer to contribute: do the work, make its boundaries inspectable, and leave maintainers room to steer.

## Teaching, before and after agents

My current documentation work treats teaching as an executable system:

- [Trustworthy docs for humans and agents](https://github.com/owieschon/self-driving-trash-palace/blob/main/knowledge/resources/trustworthy-docs-for-humans-and-agents.md) defines one canonical owner per fact, ordered learning paths, and evidence labels that prose cannot upgrade.
- [sourcebound](https://github.com/owieschon/sourcebound) binds documentation claims to source evidence and fails CI when they drift.
- [Catch a lying doc](https://github.com/owieschon/sourcebound/blob/main/docs/learn/tutorial-catch-a-lying-doc.md) teaches the system through a runnable failure rather than an abstract rule.

Before that, I taught people in whatever medium the problem required:

| Artifact | Teaching work |
| --- | --- |
| [MakerGear Help Center](https://makergear.zendesk.com/hc/en-us) ([archived copy](https://web.archive.org/web/20250717214042/https://makergear.zendesk.com/hc/en-us)) | Wrote most of the knowledge base for a 3D-printer manufacturer, covering setup, slicing, materials, maintenance, and troubleshooting for users in more than 80 countries. |
| [M3-SE](https://cdn.shopify.com/s/files/1/0030/7372/files/M3-SE_EN.pdf?6088892816647700696) and [M3-ID](https://cdn.shopify.com/s/files/1/0030/7372/files/M3-ID_EN_CE_Final_2.pdf?16795155840968660542) | Shipped two hardware user guides from safety and setup through the first successful print. |
| [MakerBot Educators Guidebook](https://bpb-us-e1.wpmucdn.com/blogs.gwu.edu/dist/7/2667/files/2019/09/MakerBot_Educators_Guidebook_vf2.pdf) | Contributed classroom material for teaching 3D printing; credited on page 194. |
| [Makerspace design walkthrough](https://www.youtube.com/watch?v=Kwo2gxM78Ds) | On-camera teaching from the college makerspace program I led and scaled into a six-day-a-week operation. |

## Selected systems

These six repositories show the systems I would start with and the question each one answers.

| Project | Question it answers | Best entry point |
| --- | --- | --- |
| [TrashPal](https://github.com/owieschon/trashpal) | How can an agent participate in consequential automation without becoming the authority? | [Core build contract](https://github.com/owieschon/trashpal/blob/main/docs/architecture/CORE_BUILD_CONTRACT.md) |
| [sourcebound](https://github.com/owieschon/sourcebound) | How can a repository detect when documentation outruns its evidence? | [Documentation standard](https://github.com/owieschon/sourcebound/blob/main/STANDARD.md) |
| [Agent Governance Lab](https://github.com/owieschon/agent-governance-lab) | How can a coding-agent governance claim fail when execution or evidence drifts? | [Evidence contract](https://github.com/owieschon/agent-governance-lab/blob/main/docs/EVIDENCE_CONTRACT.md) |
| [Customer Action Control Plane](https://github.com/owieschon/ultra-csm) | How can AI draft customer actions while a person releases one exact, evidence-bound payload? | [System tour](https://github.com/owieschon/ultra-csm/blob/main/docs/TOUR.md) |
| [bank-mcp](https://github.com/owieschon/bank-mcp) | How can an LLM narrate financial data it is never allowed to compute? | [Architecture](https://github.com/owieschon/bank-mcp/blob/main/docs/ARCHITECTURE.md) |
| [Contact Verifier](https://github.com/owieschon/contact-verifier) | How should identity risk stay bounded when DNS and tenant evidence cannot justify certainty? | [Architecture](https://github.com/owieschon/contact-verifier/blob/main/ARCHITECTURE.md) |

## A decision I am proud of

[Why I killed a 0.99 AUC model](./case-studies/why-i-killed-a-099-auc-model.md) pairs a qualitative decision record with a seeded public experiment and an independent multi-seed verifier. A full-period feature appears nearly perfect until a point-in-time reconstruction removes the future information it was using.

## How I work

- Start with the customer or operator's real decision, then map the technical contract around it.
- Give one fact one owner and derive secondary surfaces instead of maintaining parallel truths.
- Use deterministic checks for authority, safety, and product outcomes; use models where interpretation is genuinely required.
- Retain receipts for completion claims and label blocked evidence instead of replacing it with confidence.
- Translate the same system for engineers, customers, operators, executives, and agents without changing its underlying truth.

Coding agents assist with research, implementation, testing, and adversarial review. I own architecture, acceptance criteria, claim boundaries, and release decisions. Public repositories use synthetic fixtures or explicitly bounded evidence, never customer records or private implementation details.
