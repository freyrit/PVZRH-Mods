# Submit a mod

The catalog currently uses reviewed GitHub pull requests. This keeps the public feed from accepting arbitrary downloads automatically.

## 1. Host the mod package

Create a public GitHub Release in a repository you control and attach the `.dll` or `.zip` package as a release asset. Do not include game files. The package must be compatible with PVZRHTools' MelonLoader-based installer.

## 2. Calculate package metadata

Record the exact asset size in bytes and SHA-256 digest. In PowerShell:

```powershell
(Get-Item .\YourMod.zip).Length
(Get-FileHash .\YourMod.zip -Algorithm SHA256).Hash.ToLowerInvariant()
```

## 3. Add a catalog entry

Fork this repository, add one object to the `mods` array in `catalog.json`, then open a pull request. Use this shape:

```json
{
  "id": "author-mod-name",
  "name": "Example Mod",
  "author": "Author name",
  "description": "A short description of what the mod does.",
  "version": "1.0.0",
  "game": "PVZ Fusion",
  "loader": "MelonLoader",
  "category": "Gameplay",
  "downloadUrl": "https://github.com/OWNER/REPOSITORY/releases/download/TAG/ExampleMod.zip",
  "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "fileSize": 12345,
  "sourceUrl": "https://github.com/OWNER/REPOSITORY"
}
```

`id` must be unique, lowercase, and use only letters, digits, and hyphens. `downloadUrl` must be the direct URL of a public GitHub Release asset. `sha256` must match the asset exactly. Keep the description factual and include known compatibility limits.

Maintainers may ask for changes or decline entries that are incomplete, unsafe, misleading, or not compatible with the supported game and loader.
