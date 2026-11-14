# Voxel world design

Status: preliminary. Only spatial addressing is implemented. Storage, meshing,
digging, claiming, reinforcement, fluids and pathfinding are future work.

## Coordinates and initial playable surface

Use signed `(x, y, z)` integers for cubic cells; Y is up. A voxel at `(x,y,z)`
occupies `[x,x+1) × [y,y+1) × [z,z+1)` in logical block units. Rendering may scale
one block into a chosen number of metres; no legacy slab/subtile scale applies.

Phase 1 uses one designated `playable_surface_y = 0`. A worker stands in empty
space beginning at Y=0, supported by the floor voxel at Y=-1. Rooms use square
X/Z footprints, each tile referencing its supporting floor coordinate. Digging
affects specified wall voxels within an authored wall-height band; a later
prototype must settle whether one tile order removes a whole column. Do not
assume this rule in generic voxel storage.

The map can store voxels above and below that surface; navigation and build
commands initially allow only its designated surface. Do not flatten positions
into `x,z` IDs or reserve a single height in file layouts. Multiple levels,
tunnels, vertical construction, bridges, elevators, stairs/ramps and physical
terrain deformation are future compatibility goals, **not implemented features**.

## Chunk model

Propose sparse chunks containing dense local arrays, initially 16³ cells. A
missing chunk is empty air, not bedrock. Maps specify finite chunk-aligned bounds
and explicit boundary policy; outside bounds is blocked/unknown, never diggable.
Chunk edge is serialized in the draft, but today's coordinate library supports
only 16; changes require explicit version/loader negotiation.

Use Euclidean division on every axis: world -1 becomes chunk -1/local 15.
Local index is `x + edge * (z + edge * y)`. Chunk cell palettes refer to stable
content IDs; runtime handles may differ after each load. Keep dirty generation
counters and separate mesh/navigation dirty regions, including adjacent chunks
when an exposed boundary face changes. Use bounded allocation before decoding.
Benchmark palette compression and chunk size before freezing a binary format.

Solid voxel occupancy is separate from sparse gameplay state: surface owner,
reinforcement owner/tier, remaining durability, environmental state and room ID.
Claimed Floor is an owned surface state, Reinforced Walls are reinforcement on
an eligible material; model them compositionally to avoid a material × owner ×
faction enum explosion. A material may still provide a special reinforced skin.

## Preliminary terrain catalogue

Values and rules below are design hypotheses, not balance numbers. Finite
durability is a positive number defined in content; an explicit indestructible
property replaces sentinel HP values. Movement depends on clearance, support,
hazard resistance and locomotion capabilities, not material name alone.

| Candidate | Proposed nature and durability | Movement / reinforcement / interactions to refine |
| --- | --- | --- |
| Dirt | Diggable solid, low finite durability | Blocks walking; reinforcement eligible |
| Rocky Dirt | Diggable solid, higher than dirt | Tool/job cost increase; reinforcement eligible |
| Gold | Finite extractable resource solid | Yield defined externally; decide post-mining material |
| Gems | Resource-bearing solid | Decide finite vs renewable extraction; not a hardcoded infinite source |
| Reinforced Walls | Ownership/tier overlay on eligible solid | Resistance and access depend on ruleset; owner-specific appearance |
| Earth | Solid candidate | Resolve distinction from dirt before shipping duplicate definitions |
| Claimed Floor | Owner overlay on supporting floor | Access/buildability/efficiency policy; not a solid filling the standing cell |
| Bedrock | Indestructible solid by initial proposal | Blocks movement and digging; no reinforcement |
| Brimstone | Hazardous solid candidate | Heat/fire interaction, finite durability TBD |
| Permafrost | Cold solid candidate | Freeze/thaw and slipping are future rules, not fluid simulation today |
| Water | Liquid occupancy/material | Swimming/flight/bridge permissions; flow deferred |
| Lava | Hot liquid | Fire damage/resistance; emissive presentation independent of damage |
| Acid | Corrosive liquid | Corrosion/durability interaction and resistance policy |
| Abyss | Unsupported void region | Falling/access policy distinct from ordinary empty air |

Empty air (`nexus:air`) is also needed for storage; it is not a walkable floor.
Material definitions should describe geometry class, destructibility, durability,
dig requirements/yields, movement tags, hazards, reinforcement eligibility and
visual references. Environmental interactions are separately registered rules
over tags; avoid a hardcoded full material-pair matrix. Do not implement fluids,
thermal simulation, structural collapse or reactions in Phase 0.

## Mutation and presentation (future contract)

A validated dig order creates a job; a completed job changes authoritative
voxels and yields resources. A claim changes ownership only after adjacency,
support and faction-rule checks. Reinforcement checks base material, owner,
resources and tier. Each successful mutation invalidates occupancy/navigation,
room connectivity/efficiency and affected mesh borders via events. Store no GPU
handles in the world.

Mesh only exposed cubic faces; compare greedy meshing with per-face materials
and ambient detail before choosing. Separate opaque, masked and transparent
surfaces. Use instancing for repeated equipment/decoration where appropriate.
Creatures use independent skeletal meshes and collision proxies. Physics shape
generation and terrain render meshes have different update/precision budgets.

## Future validation gates

Round-trip negative coordinates and world limits (covered now); storage seam
edits; palette overflow/missing references; bounded malformed RLE rejection;
save/edit/load equivalence; ownership and reinforcement preservation; pathfinding
invalidation and blocked boundaries; manual selection and digging readability.
