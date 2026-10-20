# Recon Lab: engineering notes

## Product decision

The product is an investigation workspace rather than an input/report landing page. Each view answers a distinct question; controls change the actual Python model. Synthetic presets provide reproducible demonstrations without claiming enterprise telemetry.

## Computation

The engine indexes unique composite keys and compares shared fields using Decimal arithmetic. A numeric field matches when delta ≤ max(absolute tolerance, relative percentage × absolute source value). Text trimming/case-folding is opt-in. A sensitivity sweep recomputes match coverage over seven absolute tolerance settings.

## Runtime boundary

The public demo is static GitHub Pages with Pyodide 0.27.7. A worker loads `common.py`, `engine.py`, and `lab.py`; it receives a JSON request and returns a JSON-compatible result. All analysis is Python. DOM interaction and charts are JavaScript/SVG. Python startup has a 90-second timeout; each analysis has a 30-second timeout and a stop control. Terminating the worker releases the computation. Native CLI and API entry points use the same engine without WebAssembly.

## State and data

Inputs are editable and stay in the tab. Successful exports bind to the input submitted for that run, rather than a subsequently edited form. Experiment snapshots retain summary metrics in memory, with a maximum of four. Reload clears snapshots. There are no analytics, server uploads, external model calls, or automatic input persistence. Exporting an experiment includes its input and must be reviewed before sharing.

## Accessibility and display

Semantic buttons, form labels, visible focus, keyboard-accessible tabs, a skip link, reduced-motion support, and responsive layouts are included. Pipeline nodes can be selected with Enter/Space as well as pointer clicks. Narrow pipeline canvases scroll horizontally so activity labels remain readable. Charts are accompanied by evidence or textual summaries. Light themes preserve the portfolio's pearl/champagne direction.

## Tradeoffs and limitations

Missing and target-only keys are unaffected by numeric tolerances. Control totals cover entire input snapshots and can include numeric identifiers. Equal totals do not prove equal records. Data is never repaired or written back.

## Validation

The repository tests both the original and advanced engine, serialization, algorithm boundaries, and invalid requests. `scripts/check_site.py` checks browser/native Python parity and deployable assets. Tests are run through GitHub Actions on every push. Browser interaction validation is recorded in the delivery notes rather than represented as automated end-to-end CI.
