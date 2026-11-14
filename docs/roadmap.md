# Roadmap

The roadmap describes dependency order, not delivery-date guarantees. Phase 0 is active in November 2026. No gameplay implementation or full gameplay begins before 2027. The only current scaffold is one standard-library-only Rust `nexus-world` crate for coordinate and chunk math; it has no renderer or gameplay.

## Phases and bounded backlog

### Phase 0 — foundation and validation (now; November 2026)

- **P0-01 — World coordinates and chunks.** Keep the sole `nexus-world` crate std-only; define integer voxel coordinates, chunk addressing, and checked coordinate/chunk conversions. **Depends on:** none. **Done when:** documented invariants and focused tests cover origin, positive/negative boundaries, and overflow behavior; no renderer or gameplay dependency exists.
- **P0-02 — Content identity and minimal format.** Specify stable namespaced IDs and a small versioned example definition format. **Depends on:** P0-01. **Done when:** examples parse/validate or a format-validation tool reports clear errors for malformed IDs/schema; no large content catalogue is authored.
- **P0-03 — Tick and command/event boundary.** Document fixed-tick ownership, validation, ordering, and renderer-independent command/event shapes. **Depends on:** P0-01, P0-02. **Done when:** a minimal example demonstrates inputs, deterministic ordering within the defined contract, and emitted events without linking renderer code.
- **P0-04 — Phase gate and acceptance checklist.** Record headless checks separately from manual runtime acceptance. **Depends on:** P0-01–03. **Done when:** the repository can state what is structurally validated and what still requires a human to launch and inspect a runtime; Phase 0 claims no gameplay acceptance.

### Phase 1 — 2027 world interaction slice

- **P1-00 — Engine selection spike.** Evaluate candidate rendering/runtime engines against project constraints; record the decision and tradeoffs in `docs/engine-evaluation.md`. **Depends on:** P0-01. **Done when:** a documented comparison supports one chosen engine and a minimal technical spike confirms it can host the crate boundary; no gameplay implementation.
- **P1-01 — Voxel world and placeholder 3D view.** Render a simple voxel test world, camera, and placeholder 3D creature. **Depends on:** P0-01, P0-03, P1-00. **Done when:** a human can launch the app and confirm the test world, creature, and camera respond as designed.
- **P1-02 — Selection and world commands.** Select cells/entities; issue dig and claim commands. **Depends on:** P1-01, P0-03. **Done when:** manual runtime acceptance confirms selection feedback and valid/invalid dig/claim changes in world state.
- **P1-03 — Basic pathfinding.** Route a test agent through traversable voxels and update routes after edits. **Depends on:** P1-02. **Done when:** headless route cases and manual blocked/open route checks pass; no job simulation implied.

### Phase 2 — playable core management

- **P2-01 — Heart, workers, and rooms.** Implement a minimal Dungeon Heart, worker units, room claiming/building, and simple jobs. **Depends on:** P1-01–03, P0-02–03. **Done when:** a fresh scenario supports a manually verified loop from claim/build through worker assignment and visible outcome.
- **P2-02 — Economy and combat.** Add a small resource loop, hostile units, and basic combat. **Depends on:** P2-01. **Done when:** costs/production and combat outcomes are reproducible in headless scenarios and accepted in a manual runtime session.

### Phase 3 — extended systems

- **P3-01 — Extended creature, room, and equipment systems.** Add needs, job breadth, room efficiency/upgrades, equipment, and evolution. **Depends on:** P2-01–02.
- **P3-02 — Magic, traps, doors, and consumables.** Add spells/mana, traps, access/doors, potions, and alchemy. **Depends on:** P2-02 and P3-01.
- **P3-03 — Progression and campaign systems.** Add research, manufacturing, prisoners, corpses/necromancy, attraction/spawning, factions/diplomacy, campaigns/objectives, and AI opponents. **Depends on:** P3-01–02; systems may be split into separately accepted slices.

Each Phase 3 slice is complete only when its data definitions, runtime state transitions, command/event interactions, headless cases, and manual runtime acceptance are recorded. Faction diversity must be demonstrated through distinct eligible rosters and progression/rule data, not merely different labels.

### Phase 4 — authoring and diagnostics tools

- **P4-01 — Content validation and inspection tools.** Expand format validation, ID/reference checking, simulation diagnostics, and content inspection. **Depends on:** P0-02–03 and the content used by Phases 2–3. **Done when:** intentionally malformed references are reported clearly and valid scenario data can be inspected without renderer coupling.
- **P4-02 — Mod loading and package dependencies.** Define mod manifests, dependency resolution, load ordering, and handling of missing/conflicting dependencies for custom asset and definition mods. **Depends on:** P0-02 and P4-01. **Done when:** fixture packages load in a documented order, unresolved dependencies and conflicts produce actionable diagnostics, and content IDs remain stable.
- **P4-03 — Native campaign format and editor.** Define a native campaign format and build an editor for authoring/validating campaigns and objectives. **Depends on:** P0-02, P3-03, P4-01. **Done when:** an authored campaign round-trips through the format, validates references, and runs its objective sequence in a scenario.
- **P4-04 — DK1/KeeperFX campaign converter.** Build an optional converter from supported DK1/KeeperFX campaign inputs into the native format. **Depends on:** P4-03 and explicit input-format analysis. **Done when:** documented fixtures convert with a report of preserved, transformed, and unsupported fields, and the converted campaign validates and runs. Conversion is not runtime compatibility or bundled content/assets.

### Phase 5 — presentation and scale

- **P5-01 — Presentation, content breadth, and optimization.** Expand beyond placeholder visuals with advanced animation, environmental effects, expanded rosters and additional factions, plus performance optimization against representative worlds and rosters. **Depends on:** stable world interaction and accepted playable systems from Phases 1–4. **Done when:** feature-specific manual runtime acceptance is recorded and representative workload profiles meet project-defined performance budgets; no fixed dates or budgets are implied here.

## Verification language

Headless tests and schema checks establish only the behaviors they exercise. Build success establishes compilation. Neither establishes that the application launches, renders correctly, or feels usable. Runtime acceptance means a human launches the target build and checks the specified scenario; record it separately with build identity and scenario. No phase is considered accepted solely because implementation or tests exist.

## Explicit initial non-goals

Multiple levels, elevators, advanced fluids, and networking are outside the initial scope. No dates beyond the Phase 0/2027 sequencing are promises. The roadmap grants no license, relicense, or asset provenance decisions; all content and assets require their own independent review.
