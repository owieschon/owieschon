# Owen Schoeniger

I build customer-facing AI systems for messy enterprise workflows—systems that turn uncertain model output into evidence-backed, human-authorized action.

I came to software from heavy-duty manufacturing and industrial distribution: parts catalogs, ERP data, sales workflows, and customers who rarely resemble clean benchmark rows. That experience taught me to design for the cost of a confident wrong answer.

## Start here

| Project | What it demonstrates | Fast reading path |
| --- | --- | --- |
| [Customer Action Control Plane](https://github.com/owieschon/ultra-csm) | AI-assisted customer action with a human-approved, hash-bound action boundary. The [live demo](https://ultra-csm.vercel.app/) is synthetic, read-only, and requires no login. | Demo → architecture → gate tests |
| [SKU Resolver](https://github.com/owieschon/sku-resolver) | Tenant-scoped, catalog-bound identity resolution. Models may rank retrieved candidates, but only active catalog rows can become binding identifiers; ambiguity becomes `pending` or `unresolvable`. | Contract → resolver service → catalog-boundary tests |
| [3xit enforcement engine](https://github.com/owieschon/3xit2_demo) | An independent release layer for unattended coding agents that catches oracle tampering, stale evidence, partial execution, and live-path mismatches across a 50-case adversarial suite. | First catch → enforcement path → adversarial suite |
| [Contact Verifier](https://github.com/owieschon/contact-verifier) | A compact tenant-aware integration that converts incomplete DNS and identity evidence into bounded risk instead of false certainty. | Contract → evidence adapters → integration tests |

Across them, models may extract, rank, or draft; deterministic code owns binding state changes; humans retain judgment; receipts make the result auditable.

## A decision I am proud of

[Why I killed a 0.99 AUC model](./case-studies/why-i-killed-a-099-auc-model.md) pairs a qualitative decision record with a seeded public experiment and an independent multi-seed verifier: a full-period feature appears nearly perfect until a point-in-time reconstruction removes the future information it was using.

## What I bring to an AI-native team

- Move between the customer workflow, model behavior, and the controls needed to operate safely.
- Translate technical constraints for operators, engineers, customers, and executives.
- Optimize for decision quality with independent oracles, adversarial cases, and bounded claims.

These are sanitized public artifacts with synthetic fixtures or explicitly bounded claims—not customer records or private implementation details. For customer engineering, field engineering, technical account management, or related work, reach me through GitHub.
