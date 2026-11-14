# Keeper Nexus

Canonical public repository: [github.com/TamsynnImogen/KeeperNexus](https://github.com/TamsynnImogen/KeeperNexus).
The active standalone project is published from its local shared worktree to
GitHub `main`; see `AGENTS.md` for the publishing and archive boundaries.

An independent, Rust-based, fully 3D, cubic voxel dungeon-management game and
modding platform. Multiple factions and rulesets will share a modern engine
without requiring identical creatures, rooms, resources, or progression.

**Status: Phase 0 foundation, November 2026.** Full game development and production
3D assets are planned for 2027. This repository currently builds a small spatial
library. It does not launch a game, render terrain, load mods, or convert maps.

The former KeeperFX Rust port is discontinued. Its source, uncommitted work,
and history have been preserved; see [the reset report](docs/reset-report.md).
The active tree contains no legacy engine, original game assets, FFI bridges,
or dependency on a Dungeon Keeper/KeeperFX installation. Archived legacy
history and the preserved former port are local recovery/reference material;
they are not part of the public standalone project or the architecture of the
new game.

## Direction

- Cubic terrain with digging, claiming, reinforcement, and destructible materials.
- One playable dungeon surface initially, with 3D coordinates and storage that
  leave room for later vertical expansion.
- Detailed animated 3D creatures, PBR rooms/equipment, lighting, shadows, and effects.
- External content definitions, optional modules, factions, campaigns, and mods.
- A separate future converter for selected DK1/KeeperFX maps and campaigns;
  direct runtime compatibility and full script compatibility are not goals.
- Original or permission-cleared assets; third-party franchises are references,
  never an implied permission to distribute their content.

## Build the foundation

Rust 1.75+ (edition 2021), Cargo, and Python 3.11+ for the example checker.
The local verification report records the actual tested toolchain. No graphics
engine, network fetch, original game data, or system libraries are required.

```sh
cargo build --workspace --locked --offline
cargo test --workspace --locked --offline
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
python3 tools/check_examples.py
```

`crates/nexus-world` contains only signed 3D positions and checked chunk addressing.
`examples/phase0` contains synthetic, preliminary format examples, not playable
content. The Python checker checks those fixtures; it is not a runtime loader or
a general content validator. The CI workflow is prepared for Linux, Windows,
and macOS; local checks alone do not prove those platforms or graphics drivers.

## Design documents

| Document | Purpose |
| --- | --- |
| [Architecture](docs/architecture.md) | Responsibilities, dependency direction, future crate split |
| [Engine evaluation](docs/engine-evaluation.md) | Bevy, Fyrox, and wgpu trade-offs and selection gate |
| [Voxel world](docs/voxel-world.md) | 3D model, playable surface, terrain catalogue |
| [Native formats](docs/native-formats.md) | Draft content, map, campaign, and save boundaries |
| [Gameplay systems](docs/gameplay-systems.md) | Modular gameplay responsibilities and factions |
| [Modding](docs/modding.md) | Definitions, dependencies, overrides, script boundary |
| [Legacy converter](docs/legacy-converter.md) | Offline conversion, compatibility reporting, correction |
| [Asset pipeline](docs/asset-pipeline.md) | Tripo/Blender/glTF proposal and asset admission |
| [Roadmap](docs/roadmap.md) | Milestones, dependencies, acceptance criteria |
| [Decision register](docs/decisions.md) | Current direction and unresolved design questions |
| [Reset report](docs/reset-report.md) | Audit, archive, removal/retention, recovery |
| [Verification](docs/verification.md) | Checks actually run and their limits |

## Licensing and provenance

The existing GPL-2.0-or-later code licensing is retained for this foundation;
`LICENSE` contains the existing GPL v2 text. No relicensing decision was made.
The new Rust code was written afresh; no archived implementation was copied.
Asset and mod licences must be declared independently. See
[provenance](docs/provenance.md). This is an independent genre-inspired project,
not an official Dungeon Keeper or KeeperFX release.
