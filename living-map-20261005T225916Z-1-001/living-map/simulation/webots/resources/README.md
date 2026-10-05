# Meshes, Textures, and Maps

Place 3D meshes, textures, and reference maps for the Webots tunnel world here.

## Expected Files

| File | Format | Purpose |
|------|--------|---------|
| `tunnel_geometry.obj` or `.dae` | OBJ / COLLADA | Main tunnel shell mesh (~60 m long, 3 m wide, 2.5 m high; trapezoidal cross-section) |
| `rock_texture.png` | PNG | Procedural rock/concrete surface texture (tileable, 1024×1024) |
| `beam_mesh.obj` | OBJ | Fallen concrete beam obstacle (~1.5 m × 0.3 m × 0.3 m) |
| `debris_mesh.obj` | OBJ | Debris field (irregular rock/rubble cluster) |

## Coordinate Convention

All meshes are authored in **local frame** coordinates:
- **+x**: tunnel axis (depth into mine)
- **+y**: left (facing into mine)
- **+z**: up

Origin = ONA gateway anchor point at tunnel entrance.

## Scale

All meshes exported in **metres** (1 Webots unit = 1 m).

## Notes

- The tunnel geometry mesh is imported into Webots via a `Shape` node with a `Mesh` geometry.
- Rock texture applied as a `PBRAppearance` node with `baseColorMap`.
- Beam and debris meshes are separate `Solid` nodes with physics bodies for Writer/Executor collision.
