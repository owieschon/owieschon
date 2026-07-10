# Synthetic feature-time leakage demo

This generated-data experiment shows how an apparently excellent model signal can come entirely from information that did not exist at prediction time.

Run it with the Python standard library:

```bash
python3 case-studies/leakage_demo/run_demo.py --seed 20260710 --json
```

Then verify it without importing the runner:

```bash
python3 case-studies/leakage_demo/verify_demo.py
```

The runner creates a panel of synthetic entities and peer groups. The leaky feature summarizes peer outcomes across the full observation window, including periods after the evaluation cutoff. The honest feature uses only peer outcomes available before the cutoff. Flipping every post-cutoff label changes the leaky feature but leaves the honest feature unchanged.

[`expected_output.json`](./expected_output.json) is the checked-in receipt for the documented seed. [`verify_demo.py`](./verify_demo.py) runs the producer as a black box across three fixed seeds, validates the synthetic panel shape, independently rebuilds both features, recomputes AUC with a rank-based implementation, and performs the future-perturbation test. Public CI runs the same verifier on every change.

This demo proves a failure mechanism on generated data. It does not reproduce or estimate the performance of a private model or dataset.
