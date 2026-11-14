# Keeper Nexus: independent Phase 0 foundation

## Canonical repository and publishing

The canonical public repository is
https://github.com/TamsynnImogen/KeeperNexus. Keep authorized Keeper Nexus
changes committed and pushed to GitHub `main` as part of completing the work.
Before publishing, fetch and check remote divergence, preserve all user work,
and never force-push. Publish only the intended branch using an explicit
branch refspec (for example, `git push nexus HEAD:main` after verifying the
checked-out commit); never use `--all`, `--mirror`, `--tags`, or publish local
archival refs or legacy ancestry. This shared local worktree may use the
`nexus/main` tracking branch; an ordinary clone may use `origin/main`.
Publishing guidance does not imply unattended continuous syncing or authorize
gameplay work.

Read README.md and docs/decisions.md before changing scope. The KeeperFX Rust
port is discontinued; recovery information is in docs/reset-report.md. Do not
resume porting or copy archived code/assets without a specific suitability and
provenance review. Keep legacy parsers out of the future runtime.

Full game development and production assets start in 2027. Phase 0 consists of
design, examples, and minimal headless Rust scaffolding. Engine selection,
scripts, gameplay rules, and draft formats are not frozen contracts.

Never automate input devices, focus windows, or run GUI-input automation.
Preserve user changes. Use headless checks and document manual acceptance gaps.

When adding independent new code, maintain licensing/provenance notes; do not
infer asset distribution rights from repository history or genre inspiration.
