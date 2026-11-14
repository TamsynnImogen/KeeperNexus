# Modding architecture proposal

Status: design only. No package loader, scripting VM, mod API or content compiler
exists today. Engine mechanics and authored game content are separate concerns.
See [native formats](native-formats.md) for preliminary authoring examples.

## Packages and registries

Use directory packages first; defer archive format/signing/distribution. A
manifest declares identity, version/API compatibility, authors, licences,
dependencies, ordering hints, conflicts, definitions, asset paths and requested
optional script capabilities. Package namespace ownership is validated; a
package cannot silently register another package's IDs.

Registries cover creatures, rooms, terrain, spells/abilities, traps, doors,
potions, resources, recipes, factions, rulesets, campaigns, models/materials,
textures and animation references. IDs stay textual on disk. Resolve to compact
handles only after the entire load plan validates. Registry size is bounded by
explicit budgets, not original engine model/room/player limits.

Proposed loading transaction:

1. Discover manifests in explicit configured roots; normalize safe paths.
2. Validate manifest schema and content API requirement before asset loading.
3. Select compatible package versions; reject missing required dependencies,
   conflicts and version contradictions with dependency-chain diagnostics.
4. Topologically sort dependency and applicable `load_after` edges; cycles are
   errors. Use stable lexical package-ID ordering to break otherwise equivalent
   ties. Ordering hints do not install or satisfy missing dependencies.
5. Parse definitions, validate categories and IDs, apply explicit patches, resolve
   all required references, faction rosters and rule capabilities.
6. Admit assets/scripts within budgets, then atomically publish a new immutable
   registry snapshot. Record package versions, hashes and final order in a lock.

Reject duplicate definitions. Overriding is an explicit patch naming the target,
expected target version/hash and fields changed. Multiple patches to the same
field require an explicit precedence/dependency or fail with both origins;
ordinary load order is not permission to overwrite silently. Patch syntax and
merge rules require a design review before implementation.

## Factions and rulesets

A faction selects rosters, resource/progression systems, attraction/spawn rules,
room variants and mechanic capabilities. A ruleset selects compatible policies
and victory conditions. Shared implementation does not require every faction to
have mana, workers, a workshop or identical room types. Validate required
capabilities up front; missing mechanics are errors, not hidden substitutions.
Keep optional lore/franchise-inspired concepts outside the standalone base.

Most additions should consist of definitions, meshes, animations and supported
effect/job compositions. New low-level mechanics may still require engine code;
data-driven does not mean an unlimited future API is already available.

## Optional scripting and tooling

Choose a script technology only after concrete gameplay hooks exist. Compare an
embedded language with a capability-constrained WASM host on debugging,
deterministic tick ordering, execution/memory limits, platform support, and
sandbox escape surface. No native shared-library mod ABI initially: it creates
unsafe compatibility and deployment responsibilities without an established need.

Scripts read bounded state views and submit validated commands at defined tick
boundaries. No raw pointers, unrestricted host filesystem/network/process APIs,
or engine renderer handles. Define budgets, errors, cancellation and saveable
state. A script failure must identify package/hook and pause or disable affected
content under an explicit policy; never silently alter objectives.

Provide validation CLI/editor diagnostics before the larger campaign editor:
file, field, content ID, dependency chain, severity and corrective suggestion.
Asset-only hot reload may come first; gameplay definition reload during a save
requires explicit migration/restart policy. Save/load uses the exact content
lock, with a clear incompatibility report when it cannot be reproduced.

## Future acceptance

Synthetic packages exercise missing deps, cycles, deterministic order, version
conflicts, duplicate IDs, traversal, bad references, colliding patches, absent
faction capabilities and bounded malformed content. Demonstrate one custom
creature/room/faction using data and independent assets without recompiling the
engine before describing the platform as modding-ready.
