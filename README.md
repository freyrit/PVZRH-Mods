# PVZRH Mods

The community catalog for mods used with PVZRHTools. Mod files are distributed by their authors through public GitHub Releases; this repository contains the catalog and submission guidance.

## Browse catalog

The app reads [`catalog.json`](catalog.json) from this repository's `main` branch. The catalog is intentionally empty until a mod author submits a complete listing and it is reviewed.

## Publish a mod

1. Publish your mod archive as an asset on a public GitHub Release that you control.
2. Calculate the archive's SHA-256 checksum and exact byte size.
3. Follow [MOD_SUBMISSION.md](MOD_SUBMISSION.md) to propose a catalog entry.

Each listing must point to a public HTTPS GitHub Release asset, include a SHA-256 checksum, and describe the supported game and loader versions. The app can verify the downloaded file before installing it.

## Safety and scope

- Do not upload or redistribute game files.
- Only submit mods you have permission to distribute.
- A catalog entry is reviewed before it appears in the app. Creating a release does not automatically publish it in the catalog.
- The catalog does not provide mod hosting accounts or a server-side upload service. Authors host their own release assets; catalog contributions are reviewed through GitHub pull requests.
- Listing a mod does not guarantee that it is safe or compatible. Review its source and release notes before installing.
