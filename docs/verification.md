# Phase 0 verification

Local and GitHub headless checks, 2026-11-14. This records the independent foundation only;
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
| GitHub Linux, Windows and macOS matrix | Passed on standalone publication commit `f0a5aa09acb1b914ccbd61ab4f63be36a47b36ed`; see linked run below |

A separate build using a fresh `/tmp/keeper-nexus-phase0-build` target directory
also passed. Independent read-only review repeated the routine checks, verified
all 20 local document links, the bundle hash, all 2,197 source file hashes and
the preserved original index/branch/HEAD; it found no confirmed defect.

Exact routine commands are in the root README. The Python checker verifies the
bundled examples' selected invariants; complete schemas, malformed-input suites
and runtime loaders are future work. Four spatial tests do not prove chunk
storage or terrain behavior. The [first GitHub CI run](https://github.com/TamsynnImogen/KeeperNexus/actions/runs/43584454158)
passed formatting, offline locked builds/tests, Clippy and example checks on
`ubuntu-latest`, `windows-latest` and `macos-latest`. These are hosted headless
checks with stable toolchains, not graphics/runtime acceptance or a Rust 1.75 test.

Android/ARM portability update: local Rust 1.96.0
`cargo check --workspace --all-targets --locked --offline --target TARGET` passed
for `aarch64-linux-android`, `armv7-linux-androideabi`, `x86_64-linux-android`,
`i686-linux-android`, and `aarch64-unknown-linux-gnu`. The workflow now checks
these targets too and logs the desktop compiler host triple. These checks cover
library/test-source compilation only: no cross-target test execution, native
linking, APK, Android SDK/NDK integration, emulator or physical device was tested.
See [platform support](platform-support.md) for the future device gate.

No game executable exists yet. No GPU rendering, camera, digging/claiming,
pathfinding, animation, mods, campaign conversion or in-game acceptance is claimed.
The renderer choice, balance, format stability and production asset pipeline
remain open at the documented decision gates.
