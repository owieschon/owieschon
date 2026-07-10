#!/usr/bin/env python3
"""Generate and evaluate a synthetic feature-time leakage example.

The runner intentionally emits only raw panel rows.  The portfolio's frozen
verification oracle rebuilds both features independently from those rows.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Callable


CUTOFF_PERIOD = 2
GROUPS = 40
ENTITIES_PER_GROUP = 10
PERIODS = range(5)


def generate_panel(seed: int) -> dict:
    """Return a deterministic raw panel whose future outcomes leak by group."""
    randomizer = random.Random(seed)
    rows: list[dict] = []

    for group_index in range(GROUPS):
        peer_group = f"group-{group_index:02d}"
        group_outcome = group_index % 2

        for entity_index in range(ENTITIES_PER_GROUP):
            entity_id = f"entity-{seed}-{group_index:02d}-{entity_index:02d}"
            # Each entity has one positive and one negative pre-cutoff outcome.
            # Their order is seeded so panels differ while every honest peer
            # aggregate remains exactly uninformative at the cutoff.
            pre_cutoff = [0, 1]
            randomizer.shuffle(pre_cutoff)

            for period in PERIODS:
                if period < CUTOFF_PERIOD:
                    label = pre_cutoff[period]
                elif (
                    period == CUTOFF_PERIOD
                    and entity_index == 0
                    and group_index in (0, 1)
                ):
                    # Two deliberately discordant cutoff rows keep the public
                    # leaky receipt near, rather than exactly at, perfection.
                    label = 1 - group_outcome
                else:
                    label = group_outcome
                rows.append(
                    {
                        "entity_id": entity_id,
                        "peer_group": peer_group,
                        "period": period,
                        "label": label,
                    }
                )

    randomizer.shuffle(rows)
    return {
        "schema": "temporal-leakage-panel.v1",
        "seed": seed,
        "cutoff_period": CUTOFF_PERIOD,
        "rows": rows,
    }


def _auc(labels: list[int], scores: list[float]) -> float:
    positives = [index for index, label in enumerate(labels) if label == 1]
    negatives = [index for index, label in enumerate(labels) if label == 0]
    wins = 0.0
    for positive in positives:
        for negative in negatives:
            if scores[positive] > scores[negative]:
                wins += 1.0
            elif scores[positive] == scores[negative]:
                wins += 0.5
    return wins / (len(positives) * len(negatives))


def _group_values(rows: list[dict], include: Callable[[dict], bool]) -> dict:
    grouped: dict[str, dict[str, list[int]]] = {}
    for row in rows:
        if include(row):
            grouped.setdefault(row["peer_group"], {}).setdefault(
                row["entity_id"], []
            ).append(row["label"])
    return grouped


def _peer_score(grouped: dict, row: dict) -> float:
    peer_labels = [
        label
        for entity_id, labels in grouped[row["peer_group"]].items()
        if entity_id != row["entity_id"]
        for label in labels
    ]
    return sum(peer_labels) / len(peer_labels)


def summarize_panel(panel: dict) -> dict:
    """Measure the leaky and cutoff-safe peer features on a raw panel."""
    rows = panel["rows"]
    cutoff = panel["cutoff_period"]
    evaluation_rows = [row for row in rows if row["period"] == cutoff]
    labels = [row["label"] for row in evaluation_rows]

    all_time = _group_values(rows, lambda _row: True)
    pre_cutoff = _group_values(rows, lambda row: row["period"] < cutoff)
    leaky_scores = [_peer_score(all_time, row) for row in evaluation_rows]
    honest_scores = [_peer_score(pre_cutoff, row) for row in evaluation_rows]

    censored_rows = [dict(row) for row in rows]
    for row in censored_rows:
        if row["period"] > cutoff:
            row["label"] = 1 - row["label"]
    censored_all_time = _group_values(censored_rows, lambda _row: True)
    censored_pre_cutoff = _group_values(
        censored_rows, lambda row: row["period"] < cutoff
    )
    censored_leaky_scores = [
        _peer_score(censored_all_time, row) for row in evaluation_rows
    ]
    censored_honest_scores = [
        _peer_score(censored_pre_cutoff, row) for row in evaluation_rows
    ]

    return {
        "seed": panel["seed"],
        "rows": len(rows),
        "cutoff_period": cutoff,
        "leaky_auc": round(_auc(labels, leaky_scores), 6),
        "honest_cutoff_auc": round(_auc(labels, honest_scores), 6),
        "future_censor_leaky_auc": round(
            _auc(labels, censored_leaky_scores), 6
        ),
        "future_censor_leaky_rows_changed": sum(
            before != after
            for before, after in zip(leaky_scores, censored_leaky_scores)
        ),
        "future_censor_honest_rows_changed": sum(
            before != after
            for before, after in zip(honest_scores, censored_honest_scores)
        ),
    }


def run_experiment(seed: int = 20260710) -> dict:
    """Run the public experiment and return its reproducible receipt."""
    return summarize_panel(generate_panel(seed))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260710)
    parser.add_argument("--emit-panel", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    panel = generate_panel(args.seed)
    if args.emit_panel:
        args.emit_panel.write_text(json.dumps(panel, indent=2, sort_keys=True) + "\n")
    result = summarize_panel(panel)
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
