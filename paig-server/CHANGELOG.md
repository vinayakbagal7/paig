# paig-server Changelog
All changes to paig-server will be documented in this file.

## [v0.0.7] - 2025-03-27
### Added
- Sensitive Data Filter with REDACT Regex in Guardrails
- New encryption key type for guardrails

### Changed
- Optimized validation errors for guardrails
- Fixed guardrails UI to Allow updating offtopic, denied terms and regex
- Updated paig-authorizer-core version to 0.0.2

## [v0.0.6] - 2025-03-17
### Added
- Paig lens support added. PAIG UI navigation bar updated.
- Mysql compatibility improved.

### Changed
- UI Change - User Invited column updated to 'NA' in User Management

## [v0.0.5] - 2025-03-06
### Added
- Paig-eval Frontend and Backend implementation.
- Backend API for guardrails service.
- UI Cypress automation tests for User and Login operations.

## [v0.0.4] - 2025-02-24
### Added
- AWS Bedrock guardrails support.
- API Error Handling improved for invalid API endpoints.
- Fixed application count in Sensitive Data Access dashboard graph.

## [v0.0.3] - 2024-10-08
### Added
- Added documentation for Developers Guide.
- Added Tutorial and Integration Guide for PAIG with Milvus VectorDB.
- Separated Core Authorization logic into paig-authorizer-core python module.
- Integrated paig-authorizer-core python module within paig-server.
- Added cleanup logic in encryptor refresher service.

### Changed
- Updated task template to create issues.
- Updated default value in authz response ranger policy ids, audit id and paig policy ids.
- Updated PAIG logo and Title.
- Fixed notebooks link in documents.
- Fixed paig-server python package installation issue.
- Updated audits decryption to use the same encoding as used in encryption.
- Updated README.md with new animated gif with all the features of PAIG.

## [v0.0.2] - 2024-09-06
### Added
- For audit storage Opensearch support added

### Changed
- Improved server startup experience
- Fixed warnings
- Updated dependencies
- Scanner loading time improved


## [v0.0.1] - 2024-08-14
### Added
- Initial release of the `paig-server`.