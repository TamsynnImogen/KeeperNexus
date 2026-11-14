# Legacy campaign and map converter specification

Status: design specification. This document defines a future converter; it does not claim that a converter or any native writer already exists.

## Purpose and compatibility boundary

Convert user-supplied, lawfully obtained DK1/KeeperFX campaign and map data into a staged Keeper Nexus project. The converter may read legacy maps and associated metadata, placements, terrain, rooms, ownership, objectives, and scripts. It must not run the game, execute scripts, or modify source inputs. It must not copy proprietary game assets into its output. Full gameplay or campaign compatibility is explicitly not promised.

The converter must not infer undocumented binary layouts, coordinate scales, slab mappings, enum values, script semantics, or version differences. Each supported input format and mapping requires documented format research and fixtures before implementation. Unknown or unverified semantics are reported; they are never silently assigned a plausible default.

## Inputs and output

Inputs may include maps and campaign metadata plus placements, terrain and room definitions, ownership, objectives, and script text or references. Parsing is data-only: scripts are treated as opaque source or structured text and are never evaluated. Do not depend on the game runtime, FFI, or native engine execution to parse inputs. A shared native-format DTO/validator crate is appropriate; legacy parsers stay in the converter and are never linked by the game.

Write only into a new output directory. If the requested output directory already exists, fail by default and preserve it. Stage native-format project manifests and content in the output; never write back to input files. Every conversion records the source identity and the conversion choices so an output can be audited or reproduced.

The proposed CLI is limited to:

```text
keeper-nexus-convert --input PATH --output PATH --profile NAME [--strict] [--report PATH] [--dry-run]
```

`--profile` selects an explicit, versioned mapping profile. No implicit “best guess” profile is allowed. `--dry-run` performs parsing, mapping, and validation without creating staged output. `--strict` fails conversion when any required source feature is unsupported, approximated, or needs manual work. Without strict mode, incomplete staging is permitted only when the report clearly records every limitation. A successful process exit must never imply that unsupported required objectives or scripts were preserved.

Proposed exit status: `0` means complete under the selected profile, `2` means
incomplete conversion (staged only when non-strict), and `1` means fatal input,
profile, validation or I/O failure. Dry-run emits its report to stdout and writes
no files; reject `--report PATH` combined with dry-run. Strict failure may write
an explicitly requested diagnostic report, but must not promote a native project
as complete. Final output promotion follows validation; never replace an existing
destination.

## Native target conventions

Use the native format definitions in `docs/native-formats.md` as they become documented. The currently proposed conventions are draft-only: TOML manifests and content; JSON maps with version `0.1-draft`; y-up signed XYZ voxel coordinates; floor construction in XZ at `playable_surface_y = 0` with supporting floor voxels at `y = -1`; and chunk edge 16. The chunk edge is provisional. Treat these as target-format constraints, not evidence about any legacy source layout or scale.

Map profiles must state their conversion from source coordinates and units to target coordinates, including origin, axis direction, scale, rounding, bounds, and any slab-to-voxel construction. Such values require documented evidence and fixtures for that source version. If a profile cannot justify a mapping, affected data is blocked or requires manual conversion; do not guess.

## Profiles, provenance, and reproducibility

Each profile must have a stable identifier and version, supported source game/format versions, references to the format research and fixtures that justify its mappings, and explicit mappings for all handled feature categories. Profile changes that alter output semantics require a version change.

The staged project must include a machine-readable conversion record containing at least:

- converter and profile identifiers/versions;
- detected or user-declared source format/version, and any uncertainty;
- hashes of every source file read (SHA-256), relative source names, and byte sizes;
- per-category mapping decisions and output paths;
- unsupported, approximated, manual, and blocked items with source locations;
- warnings/errors and whether conversion was strict or dry-run.

Do not embed proprietary assets. Where the source references an asset absent from the project, preserve only a reference/identifier when its meaning is understood and report the missing external dependency. Hashes identify inputs; they do not grant redistribution rights.

## Feature handling and report contract

Every discovered item must end in one explicit state: `supported`, `approximated`, `manual`, or `blocked`. Each report entry includes severity, category, stable item identifier where available, source file and location (byte offset, record/index, or text line/column as appropriate), target path or affected object if known, state, and a concise reason. Include relevant profile mapping identifier and evidence/fixture reference when applicable.

- **Supported:** mapping is documented and preserves the defined semantics within the stated profile.
- **Approximated:** output intentionally differs; state the exact loss or substitution. Never describe this as full compatibility.
- **Manual:** conversion is withheld pending a human-supplied correction or mapping.
- **Blocked:** conversion cannot safely proceed for that item, including malformed or unknown required data.

Severity communicates impact (at least `info`, `warning`, `error`, `fatal`). A required objective or script that is unsupported, approximated, manual, or blocked must produce an error or fatal report entry and make `--strict` fail. Unknown required data cannot be discarded while returning success. The summary must count items by state and severity and distinguish “staged” from “complete under profile.”

Illustrative report shape (not an implemented report writer):

```json
{
  "format_version": "0.1-draft",
  "profile": {"id": "example-profile", "version": "0.1.0"},
  "outcome": "incomplete",
  "entries": [{
    "severity": "error", "state": "manual", "category": "objective",
    "source": {"file": "synthetic-script.txt", "line": 3},
    "item_id": "objective-1", "target": null,
    "reason": "No verified native mapping for this required condition"
  }]
}
```

The complete implementation must also include the input hashes, converter
version and summary counts specified above. This synthetic shape makes no
claim about an actual DK1/KeeperFX command or file layout.

## Corrections and repeat conversion

Manual corrections belong in a separate, explicit patch overlay, never in generated files or the source campaign. The overlay must identify its base conversion/source hashes and profile version, and use stable source/item identifiers where available. On reconversion, apply only corrections whose base identity and targets still match. Report stale, ambiguous, or conflicting patches and require review rather than silently applying them. Preserve the overlay across conversion runs; do not overwrite or delete it.

## Validation and tests

Before implementation, assemble documented fixtures for each supported source version and each claimed mapping. Keep synthetic golden fixtures separate from local lawful game fixtures:

1. **Synthetic golden tests:** small hand-authored byte/text inputs with documented expected parse results, coordinate transforms, native manifests/maps, hashes, and report entries. Include malformed, truncated, unknown-version, out-of-range, unsupported-required-objective, and unsupported-script cases. Assert that strict mode fails on every required unsupported/approximated/manual/blocked item, output collisions fail without modifying existing contents, dry-run writes nothing, and patch overlays survive reconversion with stale patches rejected.
2. **Local lawful fixtures:** user-provided files the tester is authorized to inspect. Keep them outside source control unless redistribution rights are established. Record source hashes, provenance, declared/detected version, profile version, expected report, and manual review outcome. Do not include proprietary asset bytes in test output or documentation.

Golden tests validate the converter’s declared mappings, not general compatibility with all DK1/KeeperFX content. Any unsupported versions or features remain explicit in the profile and report.

## Licensing and provenance

The KeeperFX Enhanced source audit found a repository GPL-2.0-or-later declaration and KeeperFX-specific Rust ports; the top-level `LICENSE` is GPL version 2. That audit did not establish the provenance or license of every copied subset. Preserve applicable source notices, document the provenance of any implementation derived from legacy code, and review dependency and asset licenses before redistribution. Do not treat the license of the converter or project as permission to distribute proprietary game assets or imported campaign content. This specification does not change any license.
