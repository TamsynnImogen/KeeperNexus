# Licensing and provenance ledger

This is an engineering inventory, not a grant of rights to third-party content.
The reset retains existing code licence metadata and does not relicense history.

| Material | Active treatment | Provenance / further work |
| --- | --- | --- |
| Existing LICENSE text | Retained byte-for-byte | GPL v2 text from archived repository; Rust prototype metadata was GPL-2.0-or-later |
| Phase 0 Rust spatial library | Newly written under retained GPL-2.0-or-later metadata | No legacy implementation transplanted |
| Phase 0 docs, checker and synthetic examples | Newly authored foundation | Repository code licensing retained; no franchise content/assets copied |
| KeeperFX C/C++/Rust port | Archive history only | Keep upstream notices; file-specific and transitive provenance needed before reuse |
| RNC/JSON/legacy map or replay utilities | Candidates only, not retained in active code | Audit upstream algorithms, licences, native assumptions, and exact source lineage before converter reuse |
| Existing fonts, sprites, textures, maps, binaries, third-party dependency trees | Removed from active tree; recoverable in original/archive as applicable | Do not treat historical presence as permission to redistribute |
| Future Tripo/Blender assets and mods | None bundled | Per-item authorship, terms, licence, attribution, source/export hashes |

The archive bundle is a **local recovery artifact**, not a release distribution.
The GitHub publication starts from a fresh root with only the standalone tree;
legacy history remains in local archive refs and the verified bundle. Never push
those refs or use `--all`, `--mirror`, or `--tags` for publication. Release packages
must use the active tree and an explicit allowlist. Do not publish archival blobs
before their distribution rights are reviewed.
Independent source architecture does not itself settle trademark, copyright,
asset rights, or eventual licensing decisions.
