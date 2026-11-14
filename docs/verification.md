# Phase 0 verification

Local headless checks, 2026-11-14. This records the independent foundation only;
the discontinued KeeperFX port was not rebuilt or launched.

Toolchain: Rust/Cargo 1.96.0 on Linux x86_64. Declared minimum Rust is 1.75;
that minimum toolchain is not installed and was not tested. The lockfile uses
version 3 and there are no third-party Cargo dependencies.

| Check | Outcome |
| --- | --- |
| Cargo build, workspace, locked/offline | Passed |
| Cargo test, workspace, locked/offline | Four tests passed: negative boundary, world-range round trips, local range/order, checked overflow |
| Cargo fmt --check | Passed |
| Cargo clippy, all targets, locked/offline, deny warnings | Passed |
| Python example checker | Passed: two material definitions, one RLE chunk, one supported unclaimed surface |
| Active-tree local Markdown links | Checked before completion |
| Archive bundle verify and independent clone/fsck/blob comparison | Recorded in archive recovery receipts |
| Original worktree source hashes, branch/HEAD, index and status | Compared with archive receipt before completion |

A separate build using a fresh `/tmp/keeper-nexus-phase0-build` target directory
also passed. Independent read-only review repeated the routine checks, verified
all 20 local document links, the bundle hash, all 2,197 source file hashes and
the preserved original index/branch/HEAD; it found no confirmed defect.

Exact routine commands are in the root README. The Python checker verifies the
bundled examples' selected invariants; complete schemas, malformed-input suites
and runtime loaders are future work. Four spatial tests do not prove chunk
storage or terrain behavior. Cross-platform CI is prepared but has not run on
a remote or established Windows/macOS acceptance.

No game executable exists yet. No GPU rendering, camera, digging/claiming,
pathfinding, animation, mods, campaign conversion or in-game acceptance is claimed.
The renderer choice, balance, format stability and production asset pipeline
remain open at the documented decision gates.
