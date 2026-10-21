# Recon Lab — user guide

## Start with the question

Compare source and target records using unique business keys and explicit tolerance policies.

## Five-minute tour

Run the sample → inspect changed records → compare tolerance frontier → review missing keys → open Review desk → export the handoff.

1. Open [the live app](https://m-qazi99.github.io/recon-lab/) and inspect the labeled synthetic preview.
2. Review the editable inputs before selecting **Run experiment**. The first run downloads a pinned Python runtime.
3. Inspect the workspace views; choose a source record, activity or passage when available.
4. Scroll to **Review desk**. Filter **Investigate**, **Review**, or **Context**. Check an item only after inspecting its evidence.
5. Export the reviewed handoff. Its checkmarks describe your inspection state; they are not automatic sign-off.

## Review Desk in this project

Keyset exceptions, field-level mismatch priorities, and policy review before widening tolerance.

Every computed run replaces the priorities and clears the checklist. Switching workspace views retains it. Reload also clears it. Unfiltered exports include every priority and its checked state.

## Downloads and data

The input editor supports local files. Inputs are processed in a Python worker; the initial runtime comes from jsDelivr. Exported full experiments include their inputs. Review Desk exports omit original cell values, but can contain column names, activity names, query text or document titles. Review all exports before sharing.

## Troubleshooting

- **Runtime does not start:** check connectivity to jsDelivr, then retry. Use the native CLI if WebAssembly/CDN access is unavailable.
- **Invalid request:** keep the source error and reduce the input to a synthetic reproducer. Field constraints are in [API.md](API.md).
- **Old results after editing:** select Run experiment again. The current result represents the last submitted request.
- **Checklist disappeared:** it resets for a new result or page reload by design.

## Limits

Missing and target-only keys are unaffected by numeric tolerances. Control totals cover entire input snapshots and can include numeric identifiers. Equal totals do not prove equal records. Data is never repaired or written back.

Inputs remain in the active tab. Initial runtime files come from jsDelivr and fonts from Google Fonts; no input is sent to these services. Inputs and snapshots are not automatically persisted. Exported experiments include their input; review before sharing. File contents are limited to 2 MB and CSV datasets to 10,000 rows.

[Implementation](ARCHITECTURE.md) · [Report an issue](https://github.com/m-qazi99/recon-lab/issues/new/choose)
