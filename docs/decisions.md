# Decision register and design questions

Status: 2026-11-14. Revisit proposals with measured evidence in 2027.

| ID | Status | Decision / question | Next evidence or discussion |
| --- | --- | --- | --- |
| D01 | Directed by project owner | Independent Rust 3D voxel game; KeeperFX port discontinued | Reset report and archived implementation |
| D02 | Directed | One initial playable surface, full XYZ world | Prototype selection/dig/claim and floor support |
| D03 | Directed | External content, multiple factions/rulesets; no legacy assets needed | Data-only custom faction acceptance |
| D04 | Directed | Offline converter only, no direct runtime legacy compatibility | Synthetic conversion/report fixtures |
| D05 | Phase 0 choice, reversible | One std-only coordinate crate; no game/editor stubs or empty systems | Split when actual consumers/boundaries exist |
| D06 | Recommendation | First rendering spike in Bevy; Fyrox alternative, direct wgpu only for measured need | Engine evaluation gate; no dependency adopted |
| D07 | Proposal | TOML 1.0 authoring, JSON map interchange, explicit schemas | Author feedback and bounded parser validation |
| D08 | Proposal | 16³ chunks, Y-up, X/Z room tiles; claimed/reinforced overlays | Meshing/storage profiling, tile scale and wall-height choice |
| D09 | Retained, no relicensing | GPL-2.0-or-later code metadata and existing licence text | Owner review before any future licence change; asset licences separate |
| D10 | Open | Engine version, ECS integration, desktop minimum hardware and quality budgets | Cross-platform spike measurements |
| D11 | Open | Tick rate, numeric model, RNG, save versioning/migrations | First simulation/persistence design; networking deferred |
| D12 | Open | Dirt vs Earth, gem exhaustion, hazard/temperature/fluid semantics | Terrain design review before implementation |
| D13 | Open | Dig column vs individual voxels; room tile scale, cutaway camera | Readability and gameplay prototype |
| D14 | Open | Faction capabilities, resources, progression, Dungeon Heart alternatives | Two meaningfully different synthetic faction designs |
| D15 | Open | Script VM, capability policy, debugging and saveable state | Actual bounded gameplay hook use cases |
| D16 | Open | Native binary map/save layout, compression and content hashing | Benchmarks and first persistent milestone |
| D17 | Open | Legacy mapping scale, script subset, objective equivalence | Independently researched formats and lawful fixtures |
| D18 | Open | Tripo rights/export workflow, rig standards, LOD conventions and budgets | Export/import and deformation tests; terms review at use |

Draft files intentionally make these questions visible. No production rendering,
scripting, binary layout, multiplayer protocol, balance, or full compatibility
commitment has been made by the reset. Do not interpret a format illustration
as approval to implement all of its eventual systems before 2027.
