# Rendering and engine evaluation

Status: researched 2026-11-14; recommendation only. **No engine dependency has
been added.** Re-evaluate supported releases and licences at the 2027 spike.

| Approach | Useful starting point | Cost / uncertainty for Nexus |
| --- | --- | --- |
| Bevy | Rust ECS/plugins; PBR, glTF skinning and animation blend graph examples | Custom chunk meshing/invalidation, picking, pathfinding and tools still needed; migration work must be budgeted |
| Fyrox | Rust engine with integrated editor, animation tooling and scene workflow | Verify procedural chunk update throughput and data-first mod workflow; avoid coupling authoritative state to editor scenes |
| wgpu + selected libraries | Portable GPU API, maximum control over chunk rendering | Team must assemble asset loading, animation, PBR/shadows, tools, UI and resource lifetimes; largest maintenance scope |

Bevy is the preferred **first experiment**, because its data-oriented/plugin
model fits a simulation with generated terrain and separate content. This is a
design inference, not benchmark evidence. Its official guide warns about missing
features and breaking API releases; pin an evaluated release and schedule
upgrades, rather than depending on moving main.
[Bevy introduction](https://bevy.org/learn/quick-start/introduction/).

Official examples demonstrate glTF skinned animation, blend graphs, PBR and
custom meshes. These are promising building blocks, not proof that Nexus-scale
voxel worlds or production animation will meet budget.
[Bevy examples](https://github.com/bevyengine/bevy/blob/main/examples/README.md).

Fyrox merits a comparison if its editor substantially reduces content iteration
cost. Its project provides an editor and animation/scene facilities, and added
glTF loading in its documented 0.34 release; current loader coverage must be
tested with Nexus exports.
[Fyrox repository](https://github.com/FyroxEngine/Fyrox),
[glTF introduction in Fyrox 0.34](https://fyrox.rs/blog/post/fyrox-game-engine-0-34/).

wgpu exposes portable graphics/compute APIs with native Vulkan, Metal, DX12 and
OpenGL ES backends. It is a graphics foundation, so selecting it directly also
means owning the higher-level engine systems. Choose only if a measured blocker
in an existing engine justifies that burden.
[wgpu project](https://wgpu.rs/).

## Selection gate: Phase 1, before production implementation

Use independent cubes and a permission-cleared rig. Compare identical scenes
and recorded settings, not marketing feature counts:

1. Chunk face culling, boundary edits, asynchronous rebuild and stale-job rejection.
   Compare naive face meshing with greedy merging; avoid an entity per cube.
2. Elevated orbit/pan/zoom camera, orthographic vs perspective readability,
   occlusion/cutaway options, CPU voxel ray traversal and selection latency.
3. GLB skin, named clips, blending, material sharing, 3 LOD meshes, collision
   proxies; record extension support and import failures.
4. PBR, moving lights/shadows, masked/transparent surfaces, particles, emissive
   lava and a water plane; graphics tiers with fallbacks and adjustable distance,
   shadow budget, LOD and effects. Fluid physics is a separate question.
5. Fixed-tick headless simulation while frames vary; save/restore domain state
   without serializing engine entities.
6. Measure cold build, incremental build, frame-time distribution, RAM/VRAM,
   chunk update latency and scaling at several world/entity sizes. Set target
   budgets before interpreting results. Test Linux, Windows and macOS on actual
   hardware/backends; record driver and adapter details.

Exit: a written decision with pinned versions, licences, selected quality tiers,
measured limits, import receipts and manual camera/readability acceptance.
No performance numbers or cross-platform graphics acceptance are claimed today.
