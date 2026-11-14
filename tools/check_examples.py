#!/usr/bin/env python3
"""Check selected invariants of the bundled draft fixtures, not arbitrary mods.

Uses only Python 3.11+ standard library. No legacy data or engine is involved.
Real loaders need complete schemas, bounded input sizes and richer diagnostics.
"""
from pathlib import Path
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1] / "examples" / "phase0"
VERSION = "0.1-draft"
ID = re.compile(r"[a-z][a-z0-9_.-]*:[a-z][a-z0-9_.-]*\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def integer(value):
    return type(value) is int


def xyz(value):
    return (isinstance(value, list) and len(value) == 3
            and all(integer(v) and -(2**31) <= v < 2**31 for v in value))


def check():
    manifest = tomllib.loads((ROOT / "manifest.toml").read_text(encoding="utf-8"))
    require(manifest["format_version"] == VERSION, "manifest version")
    require(manifest["kind"] == "base", "fixture is a base package")
    require(manifest["dependencies"] == [], "fixture must be independent")
    require(manifest["required_features"] == [], "fixture has no optional host features")
    definitions = {}
    for relative in manifest["content"]:
        path = ROOT / relative
        require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
                "content path must be relative")
        require(path.resolve().is_relative_to(ROOT.resolve()), "content path escapes fixture")
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        require(data["format_version"] == VERSION, "definition version")
        for item in data["definitions"]:
            name = item["id"]
            require(ID.fullmatch(name) is not None, f"invalid definition ID: {name}")
            require(name.startswith(manifest["id"] + ":"), "namespace ownership")
            require(name not in definitions, f"duplicate definition: {name}")
            require(item["kind"] == "terrain", "fixture supports terrain only")
            require(item["geometry"] in ("solid", "air"), "fixture geometry")
            if not item["indestructible"]:
                hp = item.get("max_durability")
                require(integer(hp) and hp > 0, "finite terrain needs positive durability")
            definitions[name] = item

    data = json.loads((ROOT / "map.json").read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object)
    require(data["format_version"] == VERSION, "map version")
    require(ID.fullmatch(data["id"]) is not None, "map ID")
    require(data["required_packages"] == [
        {"id": manifest["id"], "version": manifest["version"]}], "package lock")
    require(data["coordinate_system"] == "y-up", "coordinate system")
    edge = data["chunk_edge"]
    require(integer(edge) and edge == 16, "draft chunk size")
    low, high = data["bounds"]["min"], data["bounds"]["max"]
    require(xyz(low) and xyz(high), "bounds must be signed xyz")
    require(all(a < b and a % edge == b % edge == 0 for a, b in zip(low, high)),
            "bounds must be positive and chunk aligned")
    require(data["boundary"] == "blocked", "boundary policy")
    surface_y = data["playable_surface_y"]
    require(integer(surface_y) and low[1] < surface_y < high[1], "surface height")
    palette = data["palette"]
    require(palette and palette[0] == "nexus:air", "empty palette entry")
    require(len(set(palette)) == len(palette), "duplicate palette ID")
    require(all(p in definitions for p in palette), "missing material reference")
    chunks = {}
    for chunk in data["chunks"]:
        coord = chunk["coord"]
        require(xyz(coord), "chunk coordinate")
        key = tuple(coord)
        require(key not in chunks, "duplicate chunk")
        require(all(a <= c * edge and (c + 1) * edge <= b
                    for a, b, c in zip(low, high, coord)), "chunk outside bounds")
        cells = []
        for count, index in chunk["runs"]:
            require(integer(count) and 0 < count <= edge**3 - len(cells), "bad RLE count")
            require(integer(index) and 0 <= index < len(palette), "bad palette index")
            cells.extend([index] * count)
        require(len(cells) == edge**3, "incomplete chunk")
        chunks[key] = cells
    seen = set()
    for surface in data["surfaces"]:
        pos = surface["pos"]
        require(xyz(pos), "surface coordinate")
        require(pos[1] == surface_y - 1, "surface must reference supporting floor")
        require(all(a <= p < b for a, b, p in zip(low, high, pos)), "surface out of bounds")
        require(tuple(pos) not in seen, "duplicate surface")
        seen.add(tuple(pos))
        coord = tuple(p // edge for p in pos)
        x, y, z = (p % edge for p in pos)
        index = x + edge * (z + edge * y)
        material = chunks.get(coord, [0] * edge**3)[index]
        require(definitions[palette[material]]["geometry"] == "solid", "surface lacks support")
        require(set(surface) == {"pos"}, "fixture surface must remain unclaimed")
    require(all(data[key] == [] for key in ("players", "entities", "rooms", "objectives")),
            "fixture must not imply unimplemented gameplay schemas")
    print(f"Phase 0 examples OK: {len(definitions)} materials, {len(chunks)} chunk, "
          f"{len(seen)} supported surface; selected invariants only.")


if __name__ == "__main__":
    check()
