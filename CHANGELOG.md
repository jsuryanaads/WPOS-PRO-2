# WPOS PRO 2 Changelog

## 2.7.17 — Global UI Refinement

- Applied a global UI rule across all 14 business pages: decorative label backgrounds are transparent by default.
- Removed the visual "box inside box" treatment caused by unnecessary label backgrounds while preserving functional backgrounds for inputs, buttons, tables, cards, badges, and panels.
- Standardized label presentation so text sits directly on its parent surface unless a specific component requires its own background.
- Kept business logic, database schema, authentication flow, and transaction behavior unchanged.
- Recorded the version change in README and Changelog according to the release versioning policy.

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
