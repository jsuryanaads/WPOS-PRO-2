# WPOS PRO 2 Changelog

## 2.7.16 — Stabilization Release

- Strengthened SQLite backup restore validation.
- Added integrity and core-schema validation before restoring a database.
- Added a safety backup of the active database before restore replacement.
- Added automated backup/restore regression coverage.
- Enforced SemVer validation in the Windows build pipeline.
- Aligned installer metadata with application version `2.7.16`.
- Versioned EXE and installer artifacts by release version.
- Added SHA-256 checksum generation for the installer artifact.
- Updated the local Windows build script to run compile checks and tests before packaging.

### Release rule

WPOS PRO 2 uses Semantic Versioning (`MAJOR.MINOR.PATCH`):

- **PATCH**: bug fixes, hardening, and backward-compatible stabilization.
- **MINOR**: new backward-compatible functionality.
- **MAJOR**: breaking changes or incompatible architecture/API changes.

A version is a release milestone, not a commit counter. A release is considered complete only when the source version, installer version, build artifacts, tests, and release metadata are consistent.
