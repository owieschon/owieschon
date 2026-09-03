# Owen Schoeniger

Most of my work starts with a workflow nobody has specified cleanly.

I figure out how the work actually happens, identify the decisions and failure
modes that matter, and build whatever the result requires. That work has
included industrial catalog resolution, revenue intelligence, customer
operations, developer tools, and agent infrastructure.

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

## Selected systems

- [Sourcebound](https://github.com/owieschon/sourcebound) — a released CLI that
  binds documentation claims to source evidence and fails CI when they drift.
- [Ultra CSM](https://github.com/owieschon/ultra-csm) — a synthetic, full-stack
  customer-action system that assembles evidence, proposes a next step, and
  requires a separate approval record tied to the proposed action.
- [GoNoGo](https://github.com/owieschon/gonogo) — a coding-agent task evaluator
  that compares the specification with the diff, tests, and transcript, then
  pressure-tests its verdict against adversarial fixtures.
- [bank.mcp](https://github.com/owieschon/bank-mcp) — a local personal-finance
  system with exact integer-cents storage, deterministic forecasts, and a model
  boundary that cannot overwrite computed figures.

## External contributions

Two fixes for [Superset](https://github.com/superset-sh/superset) are currently
under review: correct pull-request merge attribution
([#7110](https://github.com/superset-sh/superset/pull/7110)) and preserve agent
session recovery after terminal cleanup
([#7127](https://github.com/superset-sh/superset/pull/7127)).
