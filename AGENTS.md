# Repository agent instructions

<!-- wellmanifest:local-ci-publication:start -->
## Local CI and independent publication

Adopt the publication policy from [Wellmanifest/new-project 0.20.10](https://github.com/wellmanifest/new-project/blob/d5f77d83b3752477cfb95a535d0e1ce77f148576/docs/information/local-ci-publication.md).
Immutable source revision: `d5f77d83b3752477cfb95a535d0e1ce77f148576`.
Document SHA-256: `44803480f1d51f64eec81a62335b6725747f01b5f2de78105ebfc4017a7922c6`.
This is publication-policy adoption; it does not establish full governance,
adoption of every Wellmanifest pack, deployed CI or successful verification.

For `semcod/*` and `subactor/*`, prefer the protected local OneDev executor
and independent local Validator App. Preserve the repository's own tests,
required platform matrix, protected checks and actor boundaries. Read the
actual protected Validator profile and OneDev configuration; missing profiles
are coverage gaps. GitHub may host code and PRs without hosting test execution.
A GitHub Actions billing/capacity failure does not prove local CI is unavailable.

Before publication, observe existing local reconciliation and reuse its receipt.
Require verification of the exact PR head with the current base and merge result.
Invoke the trusted local Validator adapter or its existing timer under the
user's publication authorization; never self-approve or merge directly.
Use hosted `dispatch-direct-pr.sh` only when the protected deployment explicitly
selects that transport. This rule supersedes older unconditional hosted-dispatch
examples, while retaining all additional repository requirements.

Retire a hosted check only after equivalent local tests and the required OS
matrix have a successful deployed canary and an independently reviewed policy
migration. Never empty required checks or create synthetic success statuses.
Report declared, configured, deployed, verified and published evidence separately.
The complete fleet audit belongs in `subactor/docs/architecture/analysis/local-ci-adoption.md`.
<!-- wellmanifest:local-ci-publication:end -->

<!-- wellmanifest:pack-adoption:start -->
## Wellmanifest pack adoption and governance

Source standard: [Wellmanifest/new-project 0.20.10](https://github.com/wellmanifest/new-project/tree/d5f77d83b3752477cfb95a535d0e1ce77f148576).
Immutable source revision: `d5f77d83b3752477cfb95a535d0e1ce77f148576`.
Source manifest digest SHA-256: `44803480f1d51f64eec81a62335b6725747f01b5f2de78105ebfc4017a7922c6`.

### Pack applicability and classification

1. **wellmanifest/docs** (Applicable):
   - Canonical path: `docs/`.
   - Metadata and index: `.governance/docs.json`.
   - Verification: Native doc verification and required independent governance checker before merge.

2. **wellmanifest/logs** (Applicable):
   - Typed event schema: `.planfile/events/operations.jsonl` and `.planfile/events/logs.dsl.txt` (v1 event stream).
   - Identity: Structured actor, task ID, and timestamp identity on every emitted event.
   - Integrity: Hash-chain and chronological ledger integrity preserved in `.planfile/events/.logs.dsl.v1`.
   - Conformance: Planfile parser and DSL consumers strictly adhere to the typed schema.

3. **wellmanifest/worktrees** (Applicable):
   - Canonical layout: Standard v5 worktree hierarchy under `worktrees/` using relative paths.
   - Leases & boundaries: Mandatory owner check and fenced active lease in `.subactor/leases/`.
   - Recovery inventory: Preserved recovery inventory in `.subactor/recovery/` maintained across cycles.

4. **wellmanifest/license** (Evidence-backed N/A / Reconciled Profile):
   - Profile inspection: Root `LICENSE` inspected and preserved under existing explicit profile.
   - SPDX reconciliation: Reconcile SPDX identifier and matrix metadata without automatic relicensing.

5. **wellmanifest/report** (Evidence-backed N/A / Docs Placement):
   - Profile inspection: Standalone report pack N/A as `.planfile/sync/github.receipts.jsonl` and sprint audits supply native receipts.
   - Manifest requirement: Any formal reporting artifacts require canonical `docs/` placement, scoped manifests, acceptance/evidence bindings, and independent validation.

### Execution gates, lifecycle and publication

- **Gate states**: Run repository required tests, local governance, and protected native CI. Preserve `failed`, `skipped`, `not-run`, and `blocked` states distinctly; never synthesize success statuses.
- **Canary & enforce**: Enable enforce mode only after the exact required canary passes end-to-end.
- **Backlog lifecycle**: Keep this task in backlog; do NOT start source edits before current-base native owner, accepted intent, canonical worktree, and bounded fenced lease are established.
- **Merge protocol**: Use independent Validator App and protected publisher for any authorized merge; never self-approve or merge directly.
- **Diagit Planfile adapter follow-up**: Diagit can inventory and prepare a repair plan for an existing task ID, but its current DSL does not create Planfile tickets. A bounded Diagit Planfile adapter follow-up is documented where this project owns that integration.
<!-- wellmanifest:pack-adoption:end -->
