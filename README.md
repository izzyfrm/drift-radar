# Drift Radar

A numerical dataset drift monitor using reference quantile bins and population stability index.

[![tests](https://github.com/izzyfrm/drift-radar/actions/workflows/tests.yml/badge.svg)](https://github.com/izzyfrm/drift-radar/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Built as a focused AI engineering lab: inspectable algorithms, deterministic examples, and explicit failure behavior. Runs offline with the Python standard library. No API keys, model downloads, or paid services.

## Run it

```bash
git clone https://github.com/izzyfrm/drift-radar.git
cd drift-radar
python -m drift_radar examples/reference.csv examples/current.csv
```

Requires Python 3.11 or newer. Commands run from the repository root and work in PowerShell, bash, and zsh. An editable install with `python -m pip install -e .` also exposes the `drift-radar` command; direct module execution needs no installation.

## How it works

Reference CSV → quantile cut points → reference/current histograms → additive 0.5 smoothing → population stability index per column → configurable alerts. Duplicate cut points are collapsed. The report exposes bins and distributions so you can inspect an alert. Exit code 1 signals at least one feature exceeded the threshold.

## Where it fits

Monitor request length, retrieval scores, inference latency, or numerical model features. Run the shifted fixture to see an alert: `python -m drift_radar examples/reference.csv examples/shifted.csv` intentionally exits with status 1.

## Example output

See [the checked demo output](examples/output.json). It comes from the quickstart command and is a small fixture demonstration, not a performance benchmark.

## Verify

```bash
python -m unittest discover -s tests -v
```

Tests cover core behavior and edge cases. GitHub Actions runs the suite on Python 3.11, 3.12, and 3.13. Local verification is recorded in [VALIDATION.md](VALIDATION.md).

## Limitations and tradeoffs

PSI is a descriptive distance, not a statistical significance test, a diagnosis of model failure, or proof of concept drift. The default 0.2 threshold is a demo setting to calibrate on your data. Numerical columns only; missing, empty, and nonfinite values fail validation. Small samples and constant reference columns need careful interpretation.

## Project layout

| Path | Purpose |
| --- | --- |
| `drift_radar.py` | Importable implementation and CLI |
| `tests/` | Behavioral and failure case tests |
| `examples/` | Reproducible demonstration artifacts |
| `pyproject.toml` | Package metadata and console entry point |

## Related labs

[Evidence Search](https://github.com/izzyfrm/evidence-search) · [Eval Forge](https://github.com/izzyfrm/eval-forge) · [Prompt Vault](https://github.com/izzyfrm/prompt-vault) · [Drift Radar](https://github.com/izzyfrm/drift-radar) · [Route Lab](https://github.com/izzyfrm/route-lab)

## License

MIT. See [LICENSE](LICENSE).
