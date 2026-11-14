# Platform and CPU portability

Status: Phase 0, 2026-11-14. Android on **ARM and x86** is a project goal, alongside
desktop Linux/Windows/macOS and ARM64 desktop portability. There is no game
executable or Android package yet. Full game work remains scheduled for 2027.

## Android architecture matrix

| Android ABI | Rust target | Current gate / future priority |
| --- | --- | --- |
| arm64-v8a (ARM64) | aarch64-linux-android | Core compile checks; first physical-device prototype priority |
| armeabi-v7a (32-bit ARM) | armv7-linux-androideabi | Core compile checks; device support gated on engine/dependencies, memory and GPU evidence |
| x86_64 | x86_64-linux-android | Core compile checks; first Android emulator prototype priority and eligible device testing |
| x86 (32-bit) | i686-linux-android | Core compile checks; device support gated on engine/dependencies, memory and GPU evidence |

These are distinct ABIs, not an architecture called “arm86”. Android documents
the ABI names and Rust supplies corresponding targets with `std` support.
[Android ABI reference](https://developer.android.com/ndk/guides/abis),
[Rust Android targets](https://doc.rust-lang.org/rustc/platform-support/android.html).
Listing a target here does not promise a game release for that ABI. In particular,
32-bit CPU compatibility does not imply the required GPU/driver or enough memory.
Do not drop ARMv7/x86 silently: record the tested blocker and revisit the target
matrix with the project owner before narrowing it.

## What Phase 0 verifies

CI keeps the hosted desktop build/test/format/lint/example matrix, records the
compiler host triple, and adds `cargo check --workspace --all-targets` for the
four Android targets and `aarch64-unknown-linux-gnu`. This type-checks library and
test sources, including 32-bit `usize` compilation. It does **not** link a native
app, execute cross-target tests, run an emulator, verify graphics, or build an APK.
No Android SDK/NDK or Gradle project is required for these std-only checks.

To reproduce after installing the desired Rust target:

```sh
rustup target add aarch64-linux-android
cargo check --workspace --all-targets --locked --offline --target aarch64-linux-android
```

Target installation downloads Rust's standard library. Future native Android
application linking/packaging will need the selected engine's Android build
integration and compatible SDK/NDK/toolchain; do not infer that the command above
produces an installable game. Rust's Android documentation describes NDK use for
building native binaries. [Rust Android build requirements](https://doc.rust-lang.org/rustc/platform-support/android.html).

Desktop ARM64: Linux receives the explicit cross-check; macOS/Windows hosted
checks apply to their logged host architecture, not every available CPU. Native
ARM64 Linux/macOS smoke tests belong to the prototype gate. Windows ARM64 remains
an evaluation target until selected dependencies, linking and real runtime tests
support it. Rust target availability alone does not settle engine support.
[Rust platform list](https://doc.rust-lang.org/rustc/platform-support.html).

## 2027 application/device acceptance gate

- Select the engine with Android/ARM/x86 in its requirements. Pin SDK/NDK, API
  level, ABIs, dependencies and renderer backends based on actual tests. Decide
  APK vs AAB/distribution and signing later; never put signing secrets in Git.
- Package and launch the independent voxel/camera prototype on a physical ARM64
  device and an x86_64 Android emulator; test an actual x86 device before claiming
  physical x86 support. Record individual 32-bit results and any excluded ABI.
- Human-test touch pan/orbit/zoom, selection, dig/claim orders, HUD scaling and
  gesture conflicts. Provide alternatives to hover, right click and keyboard
  modifiers; optional keyboard/controller input maps to the same commands.
- Verify pause/resume, surface loss/recreation, audio focus, suspend checkpointing
  and process-death recovery. Use an explicitly scoped disposable prototype
  checkpoint for this early spike; define its contents and discard/migrate policy
  rather than imply a stable production save format already exists. Fix lifecycle
  ownership in the app, not simulation.
- Verify private save storage and explicit user-selected content/mod imports;
  review script budgets and imported package validation on mobile. Desktop path
  assumptions must not leak into domain/content schemas.
- Measure sustained frame time, memory, battery/thermal effects, chunk edit
  latency, animation and texture/shadow quality on named devices. Set minimum
  Android version, GPU/API requirements and quality budgets from those results.

An Android game client does not require the full editor or legacy converter on
Android; these can remain desktop tools producing shared native packages. Do not
add an empty app wrapper, mobile engine dependency, or new gameplay in Phase 0.
Browser, iOS and consoles are separate future decisions.
