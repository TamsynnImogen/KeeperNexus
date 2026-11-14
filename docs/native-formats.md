# Preliminary native formats

Status: **0.1-draft**, disposable design fixtures, not a stable mod/save API.
No Rust loader, serialization dependency, full schema validator, or converter is
implemented. `tools/check_examples.py` checks only the bundled examples' selected
invariants. Implement versioned DTOs/validation before calling formats supported.

## Encoding choices

Propose TOML 1.0 for package manifests and content definitions: comments and
tables are useful for authors and parsers exist beyond Rust. JSON is proposed
for generated/edited map interchange and diagnostic reports. JSON is verbose
and lacks comments; preserve hand corrections in separate overlays. RON offers
Rust-friendly enums but risks exposing Rust type changes as a public content API.
Choose explicit tagged data independent of implementation types. YAML is not
needed as a third authoring language. No parser is selected yet.
[TOML 1.0](https://toml.io/en/v1.0.0),
[JSON](https://www.json.org/json-en.html),
[RON](https://github.com/ron-rs/ron).

All text is UTF-8. IDs match `namespace:name`, each side lowercase ASCII
`[a-z][a-z0-9_.-]*`; comparisons are case-sensitive. Paths are forward-slash
package-relative paths, no absolute paths, parent traversal or external URLs.
Readers must reject duplicate keys, non-finite numbers, unsupported required
features/versions, unresolved required references and unreasonable resource
requests. Unknown fields should error in authoring validation, with an explicit
namespaced extension table for optional extras. Draft examples are not a final
error-handling implementation.

## Package manifest: `manifest.toml`

| Field | Draft meaning |
| --- | --- |
| format_version | Exact `0.1-draft` for these fixtures |
| id, version | Package namespace and independent semantic package version |
| engine_api | Required engine content API version/range; draft only |
| kind | base, mod or campaign |
| license, authors | Content ownership/distribution metadata, not implied by engine licence |
| content | Relative paths to definition tables |
| dependencies | Required package ID/version ranges; optional deps explicitly separate |
| load_after, conflicts | Optional ordering hints and incompatible package IDs |
| required_features | Features that must exist, never silently ignored |

Base content is loaded by the same future package interface as mods; it has no
privileged hardcoded roster. The fixture `nexus` is synthetic and has no
external dependencies. Dependency resolution rules are in [modding](modding.md).

## Definition tables

Each definition has `id`, `kind`, schema version inherited from the document,
display/localization reference and category-specific data. References are stable
IDs, not offsets/numeric KeeperFX models. A document carries `format_version`
and `[[definitions]]`. Initial categories include terrain, rooms, creatures,
abilities/spells, traps, doors, potions, resources, factions, rulesets,
equipment, recipes, effects and campaign objectives. Do not invent every schema
now; define and validate a category alongside its first use.

The terrain example deliberately includes only `geometry = air|solid`, `diggable`,
`indestructible`, optional positive finite `max_durability`, `movement_tags`,
and `reinforcement_allowed`. It establishes shape, not production balance.
Future tags/yields/hazards and asset references need category schemas. Runtime
cell instances reference definitions plus mutable state; HP/ownership are not
copied into each authored material definition.

## Map interchange: `map.json`

| Field | Draft meaning / validation |
| --- | --- |
| format_version, id | Version and namespaced stable map ID |
| required_packages | Exact package/version locks; release locks also record content hashes |
| coordinate_system | `y-up`; arrays are always `[x,y,z]` |
| chunk_edge | 16 in the current draft; reject other sizes in first loader |
| bounds | `min` inclusive, `max` exclusive, signed i32, chunk-aligned, positive volume |
| boundary | `blocked`; out-of-map space is never ordinary diggable air |
| playable_surface_y | Single permitted initial standing surface, 0 in fixture |
| palette | Unique material IDs, index 0 must be `nexus:air` |
| chunks | Unique `coord` chunk positions and `runs` `[count,palette_index]` |
| surfaces | Unique supporting voxel `pos`, optional owner, reinforcement, room reference |
| players | Stable map-local string ID and faction ID |
| entities | Stable map-local ID, definition ID, world transform and owner if applicable |
| rooms | Stable map-local ID, definition ID, owner and square floor voxel footprint |
| objectives | Native objective IDs/parameters; only validated handlers are executable |

Each RLE chunk expands to exactly `edge³` cells in
`x + edge * (z + edge * y)` order. Counts are positive integers and indices must
exist in the palette. Reject duplicate chunks and out-of-bounds chunks; missing
in-bounds chunks mean palette index 0. Check products/sums before allocation.
Do not infer missing floor/support or default ownership. An absent surface is
unclaimed; `owner` references a player. A `room` references a room record.
Reinforcement requires an eligible solid cell and valid owner/tier. Cross-check
room footprints, surfaces and owners; reject contradictory duplicate state.

Draft transforms use logical block units, Y-up, and positions relative to the
same origin; rotation convention and scales must be finalized with the first
entity schema. Empty entity/room/objective lists in the fixture do not specify
those future record layouts. No saved ECS entity indices or raw struct bytes.

Example: chunk `[0,-1,0]`, local cell `[0,15,0]`, index 3840 is world `[0,-1,0]`.
It supports the standing cell `[0,0,0]`. The bundled fixture has just this one
dirt voxel and an unclaimed surface: it is a format illustration, not a level.

## Campaign, save and binary formats

Campaign proposal: TOML `format_version`, `id`, `title`, `required_packages`,
ordered `[[missions]]` with unique mission ID, map path, prerequisites, native
entry conditions and result/unlock IDs. Detect dependency cycles and missing
maps. Objective semantics are explicit native data, not arbitrary legacy script
text. No campaign runner or complete campaign schema is provided yet.

Map authored state and game saves are distinct. Saves will add schema/API
version, content hashes/load order, world deltas, entity state, progression,
tick and RNG state. Decide migrations/backward support before first persistent
playable milestone. Keep unknown optional authoring metadata round-trippable
in editors; unknown required semantics block loading.

A chunked binary distribution/save container may eventually contain a versioned
header, chunk directory, palettes, compressed payloads and hashes. Byte layouts,
compression, endianness and streaming are intentionally unspecified until
measured. JSON example structure is not a promised binary ABI. Migrations must
write a new file and retain the original, with an explicit report.
