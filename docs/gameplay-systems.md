# Gameplay systems (design, Phase 0)

KeeperNexus is an independent Rust 3D cubic-voxel dungeon management game. The old KeeperFX port is discontinued: there is no runtime compatibility target, and no third-party game assets are bundled. This document defines design boundaries, not a playable specification. Phase 0 establishes formats and interfaces only; gameplay implementation starts no earlier than 2027.

## Simulation contract

The simulation is authoritative and renderer-independent. External player/AI actions enter as validated commands at tick boundaries; the simulation advances in fixed ticks and emits ordered domain events plus a state snapshot/delta for presentation. Rendering, audio, UI, and input translate to and consume this contract; they do not mutate world state directly. Deterministic ordering, save/replay needs, and command/event schemas are Phase 0 validation work, not a promise of cross-platform bit-identical simulation.

Native world coordinates are signed integer X/Y/Z with Y up; the surface is at `y=0` and its floor voxel is `y=-1`. All persistent content references use stable IDs such as `nexus:lair`, never display strings or array positions. Definitions describe authored rules and parameters; runtime state holds mutable instances, timers, ownership, health, inventories, and relationships. Systems interact through commands, queries, and events rather than direct renderer or UI callbacks.

Illustrative sequence only (no implementation implied): for tick 42, accept the submitted `ClaimCell(cell)` command only if the cell exists and is claimable; reject invalid commands without changing state. Apply accepted commands in the documented stable order, then commit resulting events in that order, for example `CellClaimed(cell, faction)`. Consumers observe committed events after the tick transition, not tentative command validation. This example defines the boundary, not a complete wire format or ordering algorithm.

## Shared foundations and factions

Voxel terrain, spatial queries, pathfinding, room ownership, command validation, tick scheduling, event delivery, inventories, resources, and objective evaluation are shared mechanics. Factions use these mechanics through data-driven definitions and explicit rule hooks where a real rules difference is needed. Faction data defines rosters, room/equipment/spell availability, costs, affinities, starting conditions, and progression. Runtime owns faction resources, unlocks, relations, and active units. Factions may differ in creature rosters, recruitment, room/equipment access, research branches, economy, diplomacy, or objectives; they must not be reduced to cosmetic skins. No faction roster or special rule is finalized in Phase 0.

## System responsibilities and interactions

For each group, definitions are authored content; runtime is mutable simulation state. Listed interactions are event/command-level dependencies, not implementation commitments.

| Group | Data definitions | Runtime responsibilities and interactions |
|---|---|---|
| Rooms: efficiency, upgrades, equipment | Room types, placement rules, capacity, adjacency, efficiency curves, upgrade paths, supported equipment | Recompute usable capacity/efficiency on terrain, occupancy, damage, upgrade, and equipment changes; feed jobs, needs, research, and economy. Equipment is content with eligibility, upkeep, and effects, installed/removed as commands. |
| Spells and mana | Spell IDs, costs, targets, effects, prerequisites, faction access; mana sources/caps/regeneration rules | Validate casts and targets, spend/regenerate mana, resolve effects on ticks, emit results. Spells may affect terrain, creatures, rooms, combat, and diplomacy only through defined effects/events. |
| Traps | Trap definitions, footprint, targeting, trigger, detection, charges/recharge, upkeep, upgrades, damage/effects | Place, arm, target, detect, trigger, disarm, recharge, upgrade, and maintain instances; environmental conditions may modify defined effects. Interact with terrain, access, factions, creatures, and combat. |
| Doors and access | Door types/materials, access policy, durability, reinforcement/upgrades, lock/ownership rules, special effects | Resolve traversal and permissions for units, jobs, prisoners, and faction boundaries; handle open/closed/locked/damaged state, reinforcement, special rules, and path invalidation. |
| Potions and alchemy | Reagents, recipes, stations, outputs, storage rules, effects, research gates | Run queued production jobs, consume inputs, store and transfer potion items, and apply effects on consumption through inventory and creature events. |
| Creatures: jobs, needs, evolution | Creature IDs, stats, needs, job capabilities/preferences, experience/progression, combat abilities, evolution/transformation branches/conditions, faction membership | Track needs, assignment, work, movement, experience, combat, abilities, and evolution/transformation; arbitrate player orders versus autonomy. Jobs consume/produce shared resources and respond to room, terrain, access, and faction rules. |
| Terrain | Voxel material IDs, dig/claim permissions, hardness, support/solidity, yields, hazards | Store chunked voxel state; validate dig, claim, build, and terrain-change commands; emit changed cells and invalidate affected path/room queries. |
| Economy | Resource/item IDs, costs, yields, storage rules, upkeep, trade values | Account for reserves, transfers, production, spending, wages/upkeep, and shortages. Connect rooms, jobs, manufacturing, research, recruitment, spells, and diplomacy without UI-owned accounting. |
| Research and manufacturing | Research nodes/prerequisites/costs; recipes, stations, batches, outputs | Advance projects and production queues on ticks, reserve/consume inputs, unlock content, and emit completions. Faction progression chooses among available branches. |
| Prisoners and torture | Prisoner states, custody/escape rules, interrogation/treatment actions, facility and faction policies | Track capture, transfer, custody, escape, outcomes, and consequences. Interact with access, rooms, needs, morale/loyalty, intelligence, diplomacy, and recruitment rules. |
| Corpses and necromancy | Corpse decay/state, handling rules, rituals, recipes, resulting creature/effects | Track remains and decay, validate handling/ritual jobs, consume corpses where specified, and emit created units or effects. Interact with terrain, jobs, rooms, economy, and faction rules. |
| Attraction and spawning | Attraction conditions, caps, costs, offers, spawn rules, faction eligibility | Evaluate eligible arrivals and spawn requests, enforce capacity and costs, and create units only through validated simulation commands. Feed from room quality, economy, progression, and faction state. |
| Factions and diplomacy | Faction rosters/rules, relationship modifiers, treaties, hostility, trade and objective policies | Track relations and agreements; resolve shared mechanics with faction-specific data/hooks. Events from combat, prisoners, trade, territory, and objectives may change relations. |
| Campaigns and objectives | Campaign/mission IDs, starting setup, objective graphs, prerequisites, completion/failure conditions | Evaluate objectives from simulation events/state, sequence unlocks and mission transitions, and expose status to presentation. |
| AI opponents | Strategy profiles, priorities, constraints, difficulty parameters, faction choices | Observe the same public simulation state and issue the same validated commands as players, on defined decision intervals. No privileged direct state mutation. |
| Dungeon Heart | Heart definition, footprint, durability, resource/aura rules, defeat conditions | Own its runtime health and faction linkage; anchor dungeon start/economy rules, signal threat/defeat, and interact with rooms, workers, spells, enemies, and objectives. |

## Phase 0 boundaries

Phase 0 may define and validate content-ID conventions, minimal serialization/schema examples, command/event envelope shapes, coordinate and chunk math, and fixed-tick ownership boundaries. It does not implement gameplay behavior, faction content, full save compatibility, or complete balance data. Multiple levels, elevators, advanced fluids, and networking are explicit non-goals for the initial project scope.
