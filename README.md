# Owen Schoeniger

I build agent systems and full-stack products that turn ambiguous work into
verified outcomes. My work spans product interfaces, TypeScript and Python
services, data systems, model evaluation, tool-use runtimes, and the checks that
decide whether an agent actually finished the job.

I work best on small teams close to customers and production: find the real
failure, reduce it to a testable contract, ship the narrow fix, and keep the
result inspectable.

## Shipped product: Reter

[Reter](https://reter.io/) is a revenue-intelligence product for manufacturers
and distributors. I built it from the customer problem through the operating
system: a React application, TypeScript APIs, PostgreSQL data model, ML
pipelines, scheduled recomputation, and an agent that turns account evidence
into proposed actions.

The agent runtime owns its tool loop, context composition, capability loading,
retry budget, cancellation, and approval boundary. Actions that affect money or
leave the system wait for a distinct human decision; read-only intelligence is
also exposed through MCP for other tools to consume.

The most important model result was one I did not ship. A broad churn model
reported roughly 0.99 cross-validation AUC until I traced the result to temporal
leakage. Point-in-time reconstruction reduced it toward chance, so I replaced
the broad claim with narrower prediction lanes that generalized. The public
case study is [Why I killed a 0.99 AUC model](./case-studies/why-i-killed-a-099-auc-model.md).

## Building now: Rackful

[Rackful](https://rackful.ai/) is an execution layer for expensive AI workloads.
The current work focuses on turning workload intent into a bounded execution
contract, selecting compute with evidence, preserving artifacts and receipts,
and refusing to label a run successful when the requested deliverable is
missing.

## Agent systems and engineering tools

| Project | What it demonstrates | Start here |
| --- | --- | --- |
| [Agent Governance Lab](https://github.com/owieschon/agent-governance-lab) | A reproducible evaluation of whether execution gates catch coding-agent failures that instructions and green tests miss | [Evidence contract](https://github.com/owieschon/agent-governance-lab/blob/main/docs/EVIDENCE_CONTRACT.md) |
| [Customer Action Control Plane](https://github.com/owieschon/ultra-csm) | A full-stack agent workflow that assembles evidence, proposes an action, and binds approval to the exact payload | [Live demo](https://ultra-csm.vercel.app/) |
| [sourcebound](https://github.com/owieschon/sourcebound) | A developer tool that binds documentation claims to source evidence and fails CI when they drift | [Documentation standard](https://github.com/owieschon/sourcebound/blob/main/STANDARD.md) |
| [bank-mcp](https://github.com/owieschon/bank-mcp) | A local finance system with deterministic forecasts, integer-cents accounting, MCP access, and bounded model narration | [Architecture](https://github.com/owieschon/bank-mcp/blob/main/docs/ARCHITECTURE.md) |
| [Contact Verifier](https://github.com/owieschon/contact-verifier) | A small service that exposes the same bounded verification contract through REST, MCP, and Parquet | [Architecture](https://github.com/owieschon/contact-verifier/blob/main/ARCHITECTURE.md) |

I also contributed the core of a project-detection evaluator to
[PostHog Wizard Workbench](https://github.com/PostHog/wizard-workbench/pull/2754).
The maintainers carried its fixtures and evaluation ideas into a broader agent-
and skill-driven design.

## How I engineer agent systems

- Start with the user's deliverable, then define the evidence that would prove
  it exists.
- Turn production failures and ambiguous outcomes into repeatable evaluations.
- Let models interpret and propose; keep authorization, state transitions, and
  completion checks in code.
- Treat context, skills, tools, retries, and model choice as runtime policy, not
  prompt folklore.
- Build the product surface, backend, data path, deployment, and observability
  as one system.
- State what is simulated, what is measured, and what remains unproven.

## Background

I was a teacher before I was an engineer. I later worked across 3D printing,
manufacturing, and industrial technology. That background still shapes how I
build: expose the system's state, make failure recoverable, and give both users
and engineers evidence they can inspect.

Coding agents assist with research, implementation, testing, and adversarial
review. I own architecture, acceptance criteria, claim boundaries, and release
decisions. Public repositories use synthetic fixtures or bounded public
evidence, never customer records.
