# Asset pipeline proposal

Status: future workflow; no production assets generated, imported or required
in Phase 0. Tool versions, budgets and engine import support are not frozen.

## Authoring and interchange

Proposed path: original concept / rights-reviewed Tripo AI output → Blender
cleanup, retopology, UV/material work, rigging and clip authoring → glTF 2.0/GLB
export → validation and engine-specific cook → runtime package. Keep editable
`.blend` sources and export settings separately from generated runtime exports.
Do not treat AI output as automatically rig-ready, optimized or cleared for
distribution; record source, generation service/version/date, applicable terms,
human edits and the chosen asset licence. Review actual Tripo export/rig support
and service terms when using it; no present capability or legal guarantee is made.

glTF provides meshes, skinning, animation and metallic/roughness PBR materials;
GLB packages glTF data into a binary container. Adopt a tested subset and record
required extensions rather than expecting every Blender node or exporter option
to survive interchange. [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html).

Use named objects/materials/clips; one logical unit scale with Y-up runtime
conversion at export/import, reviewed transforms and pivots at floor contact.
Recompute or preserve normals/tangents consistently. Keep equipment attachment
sockets, collision proxies and selection bounds distinct from the visual mesh.
Prototype clips: idle, walk, work, attack and death. Specify root-motion policy
and transitions/blend rules in animation definitions; do not derive movement
distance from visual animation unless explicitly designed.

## Textures, LOD and environmental visuals

Start interchange with PNG color/normal/occlusion/roughness/metallic textures.
Color/emissive data and linear material channels need correct color spaces.
Retain lossless authoring sources; generate mipmaps and platform-specific cooked
textures. Evaluate KTX2/Basis against actual importer/backend support before
making compressed textures mandatory. KTX2 supports supercompressed textures
and glTF integration through `KHR_texture_basisu`.
[Khronos KTX](https://www.khronos.org/ktx/).

Use reusable meshes/materials for equipment, doors, traps and decoration; author
manual LOD meshes and validate transition distances. Do not assume a portable
glTF LOD convention is universally implemented. Choose LOD references in native
asset metadata if needed. Set triangle/joint/texture/draw-call budgets using the
engine spike; no arbitrary production limits yet.

Water, lava, acid and environmental effects need engine materials and particle
systems beyond static asset interchange. Separate visual animation/emission
from hazards or fluid simulation. Graphics tiers should control shadow/light
counts, texture quality, effects, LOD and draw distance. Preserve top-down
readability, silhouette and ownership cues across all tiers.

## Admission checklist for future imports

1. Record author/source/licence and source/export SHA-256; no proprietary
   franchise assets in base packages, no inferred rights from archive history.
2. Validate GLB structure with [Khronos glTF Validator](https://github.com/KhronosGroup/glTF-Validator),
   plus referenced paths, bounds, transforms, normals, textures and extension list.
3. Inspect skin weights/joint counts, named clips and deformation in Blender;
   export round trip and compare floor contact, sockets and equipment grip.
4. Import into the selected engine, check PBR/color space, shadowing, animation
   blending, shared resources, LODs and quality settings on target GPUs.
5. Preserve validation output and a manual visual acceptance note. A valid GLB
   alone does not prove acceptable deformation, appearance or performance.

Phase 1 uses independently authored geometric placeholders or explicit licensed
test rigs. Production creature/room/equipment modelling belongs to later phases.
