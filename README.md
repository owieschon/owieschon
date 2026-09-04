# Owen Schoeniger

Most of my work starts with a workflow nobody has specified cleanly.

I figure out how the work actually happens, identify the decisions and failure
modes that matter, and build whatever the result requires. That work has
included industrial catalog resolution, revenue intelligence, customer
operations, developer tools, and agent infrastructure.

## External contributions

Two fixes for [Superset](https://github.com/superset-sh/superset) are merged
upstream: correct pull-request merge attribution
([#7110](https://github.com/superset-sh/superset/pull/7110)) and preserve agent
session recovery after terminal cleanup
([#7127](https://github.com/superset-sh/superset/pull/7127)).

## Selected systems

- [Sourcebound](https://github.com/owieschon/sourcebound) — a released CLI that
  binds documentation claims to source evidence and fails CI when they drift.
  [Recorded demo](https://owieschon.github.io/sourcebound/),
  [tutorial](https://github.com/owieschon/sourcebound/blob/main/docs/learn/tutorial-catch-a-lying-doc.md).
- [Ultra CSM](https://github.com/owieschon/ultra-csm) — a synthetic
  customer-action system with a browser-only approve/deny/edit simulation;
  its local backend ties authorization to the proposed action's payload, not
  just the action type. [Synthetic demo](https://ultra-csm.vercel.app/).
- [GoNoGo](https://github.com/owieschon/gonogo) — a coding-agent task
  evaluator that compares the specification with the diff, tests, and
  transcript, checks claimed changes against the evidence, and pressure-tests
  its verdict against adversarial fixtures with deterministic replay. Human
  calibration is unverified. [Run the recorded demo](https://github.com/owieschon/gonogo#readme).

## How I build

I work at whatever layer is constraining the result. Sometimes that is the
interface or data model; sometimes it is a service, model boundary, integration,
deployment, or recovery path. The layer matters less than whether the whole
system works.

I use models where evidence is ambiguous. Identity, permissions, budgets, state
changes, and external effects stay in explicit code. I put acceptance criteria
beside the work that must satisfy them, preserve the evidence behind
consequential results, and turn failures into regression tests.

I distrust flattering results. When a
[0.99 AUC model](case-studies/why-i-killed-a-099-auc-model.md) failed
point-in-time validation, I discarded the headline result, narrowed the product
decision, and rebuilt the evaluation around historically available evidence.

## Field work

Inside a traditional manufacturer, I built a customer CRM integrated with an
ERP and a catalog-resolution engine. It maps messy rep and voice input to valid
system-of-record identifiers; ambiguous requests remain unresolved rather than
inventing a part.

## Other projects

- [bank.mcp](https://github.com/owieschon/bank-mcp) — a local personal-finance
  system with exact integer-cents storage, deterministic forecasts, and a model
  boundary that cannot overwrite computed figures.
