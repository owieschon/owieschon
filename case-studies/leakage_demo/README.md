# Synthetic feature-time leakage demo

This generated-data experiment shows how an apparently excellent model signal can come entirely from information that did not exist at prediction time.

Run it with the Python standard library:

```bash
python3 case-studies/leakage_demo/run_demo.py --seed 20260710 --json
```

The runner creates a panel of synthetic entities and peer groups. The leaky feature summarizes peer outcomes across the full observation window, including periods after the evaluation cutoff. The honest feature uses only peer outcomes available before the cutoff. Flipping every post-cutoff label changes the leaky feature but leaves the honest feature unchanged.

[`expected_output.json`](./expected_output.json) is the checked-in receipt for the documented seed. The portfolio verification oracle generates additional seeds, independently rebuilds both features from raw rows, recomputes AUC, and performs the future-perturbation test.

This demo proves a failure mechanism on generated data. It does not reproduce or estimate the performance of a private model or dataset.
