# Owen Schoeniger

I build software for work that is expensive to get wrong. The common thread is
decision-making under incomplete information: models interpret messy inputs;
ordinary code controls permission, state, spend, and the definition of done.

I work across the whole product—interface, TypeScript and Python services,
PostgreSQL, model pipelines, deployment, and operations. I like small teams,
direct contact with users, and problems where the first explanation turns out
not to be the real one.

## Shipped product: Reter

[Reter](https://reter.io/) is a revenue-intelligence product for manufacturers
and distributors. I built it from the customer problem through the operating
system: a React application, TypeScript APIs, PostgreSQL data model, ML
pipelines, scheduled recomputation, and an agent that turns account evidence
into proposed actions.

Reter's account-research system gathers evidence and proposes next steps. It can
read broadly, but anything that spends money or changes an external system
waits for explicit approval. The same read-only intelligence is available over
MCP for other software to consume.

The most important model result was one I did not ship. A broad churn model
reported roughly 0.99 cross-validation AUC until I traced the result to temporal
leakage. Point-in-time reconstruction reduced it toward chance, so I replaced
the broad claim with narrower prediction lanes that generalized. The public
case study is [Why I killed a 0.99 AUC model](./case-studies/why-i-killed-a-099-auc-model.md).

## Building now: Rackful

[Rackful](https://rackful.ai/) is an execution layer for expensive AI workloads.
It has completed six workload families on live RunPod GPUs, including full
`lm-eval` + vLLM runs for 7B and 8B open models over 11,902 documents and 42,028
requests. Accepted receipts bind the workload, artifacts, runtime telemetry,
spend ceiling, and confirmed teardown; a green provider state is not enough.

A predeclared held-out pair used one accepted run to choose the batch size for a
distinct target. Other runs remain labeled calibration, simulated, blocked, or
failed when their evidence does not support a stronger conclusion. The public
[proof surface](https://rackful.ai/proof) shows the current claim boundary.

## Agent systems and engineering tools

| Project | What it demonstrates | Start here |
| --- | --- | --- |
| [Agent Governance Lab](https://github.com/owieschon/agent-governance-lab) | On a fixed corpus, written rules and ordinary tests stopped 0/6 violations; the enforced gate stopped 6/6, while both released the two clean controls | [Receipt-verifying explorer](https://owieschon.github.io/agent-governance-lab/) |
| [Customer Action Control Plane](https://github.com/owieschon/ultra-csm) | A full-stack agent workflow with a live read-only UI and 24/24 hard gates for evidence, consent, tenant separation, grounding, injection defense, reproducibility, and proposal-only behavior | [Live demo](https://ultra-csm.vercel.app/) |
| [Career Scout](https://github.com/owieschon/career-scout) | A cost-layered agent pipeline that runs deterministic gates before a task-pinned model judge, tracks model spend through one chokepoint, and exercises the boundary with 430 passing tests | [Latest public CI](https://github.com/owieschon/career-scout/actions/runs/29916107926) |
| [sourcebound](https://github.com/owieschon/sourcebound) | A released developer tool that binds documentation claims to source evidence and fails CI when they drift | [v2.0 release](https://github.com/owieschon/sourcebound/releases/tag/v2.0.0) |
| [bank-mcp](https://github.com/owieschon/bank-mcp) | A local finance system with deterministic forecasts, integer-cents accounting, MCP access, and bounded model narration | [Architecture](https://github.com/owieschon/bank-mcp/blob/main/docs/ARCHITECTURE.md) |
| [Contact Verifier](https://github.com/owieschon/contact-verifier) | A small service that exposes the same bounded verification contract through REST, MCP, and Parquet | [Architecture](https://github.com/owieschon/contact-verifier/blob/main/ARCHITECTURE.md) |

I also built a project-detection evaluator in
[PostHog Wizard Workbench PR #2754](https://github.com/PostHog/wizard-workbench/pull/2754).
The PR was not merged as written; maintainers incorporated parts of its fixture
and evaluation approach into a broader redesign.

## How I build

I use model judgment for fuzzy evidence and ordinary code for permissions,
budgets, and state transitions. I put the acceptance rule next to execution,
turn production surprises into fixtures, and preserve enough of each run to
reconstruct why it succeeded or stopped. When a flattering metric collapses
under a better test, I narrow or kill the claim.

## Background

I was a teacher before I was an engineer. I later worked across 3D printing,
manufacturing, and industrial technology. That background still shapes how I
build: expose the system's state, make failure recoverable, and give both users
and engineers evidence they can inspect.

Coding agents assist with research, implementation, testing, and adversarial
review. I own architecture, acceptance criteria, claim boundaries, and release
decisions. Public repositories use synthetic fixtures or bounded public
evidence, never customer records.
