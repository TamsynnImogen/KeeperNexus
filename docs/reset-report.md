# Phase 0 reset report — 2026-11-14

## Active project and preserved prototype

The canonical new development worktree is
`/home/tamsynn/Projects/KeeperNexus`. The initial reset was committed on local
branch `nexus/standalone-phase0`; publication uses local branch `nexus/main`,
tracking GitHub `main` at https://github.com/TamsynnImogen/KeeperNexus.
The worktree shares the existing local Git object store, but the public project
starts with a fresh root commit containing only the standalone tree. The
KeeperFX archive and pre-publication history remain local. No legacy engine
source or game asset is built or loaded from history. Other worktrees and their
branches remain unchanged.

The former Keeper Nexus workspace was found at
`/home/tamsynn/Documents/Games/KeeperFX-Enhanced-ui-modern/rust/Cargo.toml`;
its original branch is `enhanced/ui-modern`, original HEAD
`ee3b2c1d066a58a07fd5aae1a1bfc8d41606f274`. It contained extensive uncommitted
native and Rust work. This working copy remains intact for recovery/reference;
its continued physical presence does not make it the new project's foundation.
Do not resume the port when asked to work on Keeper Nexus. The following recovery
refs and filesystem paths describe the local archive; a public GitHub clone does
not contain these archive refs or their legacy objects.

## Safe archival checkpoint

- Archive branch: `archive/keeper-nexus-port-20261114T095115Z`.
- Archive commit: `ff88fac834ee63d5f5990512f42973491bd265c9`.
- Tree: `d1f7d170ac5f03f5da084f30e6a9706d5c0893cd`.
- Recovery directory: `/home/tamsynn/Documents/KeeperNexus-archives/reset-20261114T095115Z`.
- Git bundle: `keeper-nexus-port.bundle` in that directory, plus SHA-256 receipt,
  bundle verification, source SHA-256 inventory, original status, original index,
  staged/unstaged binary patches, and independent recovery verification.
- [Machine-readable summary](archive-checkpoint.json) records the bundle hash.

A temporary Git index captured all tracked and nonignored untracked files,
without committing, staging, stashing, or resetting the source worktree.
The snapshot contains 2,198 paths: 2,197 file/symlink blobs and one empty
`external/vcpkg` gitlink directory. That gitlink records its pinned upstream
commit; the source has no corresponding `.gitmodules` mapping. It is not a
vendored copy of upstream vcpkg and upstream objects are not in the bundle.
Ignored build outputs, dependencies, local installs and other worktrees remain
at their original locations, untouched; they are not claimed as Git-archived.

Every archived file was compared to its Git blob before proceeding. The bundle
has complete repository history. See [verification](verification.md) for recovery
checks and the final source-preservation check.

## Audit and retirement decisions

Paths below refer to the archive/source checkout, not the new active tree.

| Area | Evidence / assumptions | Treatment |
| --- | --- | --- |
| Rust port workspace | `rust/Cargo.toml`: nexus-config, nexus-formats, nexus-engine, nexus-ffi | Retired wholesale from active tree |
| Native integration | `nexus-ffi/Cargo.toml` links into keeperfx; CMake Rust integration, `src/nexus_*.h`, engine build scripts reference native headers | No FFI, native callbacks or C/C++ build system carried over |
| World model | `src/map_data.h` slab/subtile conversion macros and default map size; `slab_world.rs` ports ownership/WLB/safe-land policy | Replace with signed XYZ voxel design, no inherited slab scale |
| Rendering | `src/engine_render.c` uses column stacks/slabsets; `src/kfx/renderer` and Rust rendering/texture/sprite modules preserve existing presentation behavior | Retire palette/sprite/column assumptions; evaluate a modern 3D engine independently |
| Simulation | Rust core_simulation, economy, combat, mood, navigation, keeper_ai and script_runtime behind native ownership; native creature/room/thing code remains | No automatic transplantation; document independent systems |
| Persistence/network | save_schema/replay_codec/network_frames, native packed/save layouts and protocol checks | No legacy save/replay/protocol ABI in new runtime |
| Data and assets | KeeperFX configs/campaigns/levels/lang/res; sprite/audio/texture format readers and original installation assumptions | Removed from new tree; no legacy data required |
| Port validation | `docs/rust-migration` and `tests/*` differential/parity gates | Archived as evidence of discontinued prototype, not new acceptance criteria |
| Tooling/dependencies | CMake/Make/VS launchers, vendored native helpers, external gitlink | Removed from active tree; no updater/launcher can build/deploy the old game here |

## Reuse evaluation

Pure Rust and `forbid(unsafe_code)` are useful qualities but do not establish
architectural suitability. No existing algorithm or utility was copied.

| Candidate | Assessment |
| --- | --- |
| `nexus-formats/src/rnc.rs`, mapfiles, replay codecs | Potential offline converter material only after source-specific provenance and independent format research; replay is outside initial converter scope |
| `json.rs`, config/TOML readers | Often preserve centijson/centitoml/C quirks; prefer a maintained native schema/parser for new formats after evaluation |
| Pure math/policy/navigation modules | Fixed-point tables, native callbacks and legacy semantics need per-module review; do not assume generic utility status |
| Dump-comparison/parity scripts | Useful testing ideas; existing tools target native game dumps and layouts, so not copied |
| Existing licence text | Retained byte-for-byte; code metadata remains GPL-2.0-or-later; no rights inferred for assets |

See [provenance](provenance.md). This audit is not a certification of every
historical asset/dependency's redistribution rights. Recovery artifacts stay local.

## Created foundation

- Root Cargo workspace and a newly written, std-only `nexus-world` crate.
- Four focused spatial tests; no terrain store or gameplay implementation.
- New README, local agent guidance, licence/provenance ledger and ignore rules.
- Architecture, world/terrain, gameplay, modding, converter, asset, format,
  engine-evaluation, roadmap and decision documents.
- Two synthetic material definitions, one illustrative map and a limited
  Python fixture checker; no proprietary or production assets.
- Prepared desktop CI checks; local evidence is recorded separately.

## Recovery without disturbing current work

Use a new destination; never restore over either live worktree:

```sh
git -C /home/tamsynn/Projects/KeeperNexus worktree add -b recovery/keeper-nexus-port /home/tamsynn/Projects/KeeperNexus-port-recovery archive/keeper-nexus-port-20261114T095115Z
```

If the shared repository is lost, recover the standalone source archive:

```sh
git clone --branch archive/keeper-nexus-port-20261114T095115Z /home/tamsynn/Documents/KeeperNexus-archives/reset-20261114T095115Z/keeper-nexus-port.bundle /home/tamsynn/Projects/KeeperNexus-port-recovered
```

The snapshot represents working contents. The separate original-index and patch
receipts preserve staging distinctions; do not copy that index into a different
repository. Ignored artifacts are recovered from the unchanged original checkout,
not from this bundle. Keep archive refs/bundle until their retention is explicitly
reconsidered. No cleanup of the original worktree is part of this reset.
