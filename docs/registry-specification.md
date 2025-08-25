# OGCR API Specification

**Version:** 0.1.0  
**Date:** July 2025   
**Authors:** OGCR Consortium  
**Status:** Draft  
**License:** CC-BY 4.0

## Abstract

The OGCR API Specification defines a registry framework for carbon removal certification based on open geospatial standards and verifiable ledger integration. It specifies canonical data formats, lifecycle states, API interfaces, and blockchain anchoring methods for managing project design, monitoring, verification, and issuance of removal attestations. The specification builds upon GeoJSON [[1](#ref-1)], JSON Schema [[2](#ref-2)], and ERC-721 [[3](#ref-3)] to support traceable, interoperable, and auditable carbon removal systems consistent with the Carbon Removal Certification Framework (CRCF) and Regulation (EU) 2024/3012 [[4](#ref-4)].

## 1. Introduction

### 1.1 Purpose and Scope

This specification defines the functional and structural requirements for carbon removal registry systems. It establishes data formats, interface protocols, and lifecycle rules for managing project registration, monitoring, verification, and credit issuance. The framework is designed for interoperability with third-party systems, integration with public blockchains, and alignment with regulatory instruments such as the EU Carbon Removal Certification Regulation.

The scope includes data structures for project design documents (PDD), monitoring and verification reports (MRV), and certified removal units (CRU); conformance rules for state transitions; and patterns for cryptographic anchoring. Support is provided for multiple removal types, including land-based and industrial processes.

### 1.2 Design Principles

The specification is governed by five principles:

* **Minimality**: All data requirements SHALL support traceability, validation, and regulatory reporting, with no redundant fields.
* **Extensibility**: The data model and API structure SHALL accommodate evolving methodologies and domain-specific extensions.
* **Transparency**: All state changes SHALL be traceable, verifiable, and publicly inspectable.
* **Interoperability**: The specification SHALL conform to open standards to ensure compatibility with geospatial, registry, and blockchain systems.
* **Security**: Registry operations SHALL implement role-based access control and ensure cryptographic integrity of attestations.

### 1.3 Regulatory Context

This specification is intended to support implementation of Article 9 and Annexes I–III of Regulation (EU) 2024/3012 [[4](#ref-4)]. It addresses certification requirements for permanent carbon removals, carbon farming, and carbon storage in products. It specifies data fields and workflows necessary for compliance with monitoring, verification, additionality, permanence, and liability provisions. The architecture supports registry interoperability, auditability, and integration with national and international carbon accounting mechanisms.


## 2. System Architecture

### 2.1 Architectural Overview

This specification defines a three-layer architecture required for all conforming implementations. The architecture constrains the separation of user-facing interfaces, application logic, and verifiable state anchoring. Each layer has distinct responsibilities and MUST interoperate with the others to support the lifecycle, validation, and traceability requirements defined in Sections [3](#3-core-data-models), [4](#4-api-design), and [5](#5-smart-contract-requirements).

![System Architecture](../diagrams/system-architecture-component.png)
*Figure 1: Reference system architecture defining Application, API, and Ledger layers.*

* The **Application Layer** provides interfaces for human and machine actors. This includes web portals, mobile applications, and automated clients. It SHALL support identity delegation, task execution, and interaction with the API layer.

* The **API Layer** exposes a RESTful interface for managing lifecycle operations on registry artifacts. It SHALL implement document validation, access control, schema enforcement, and canonical serialization of [PDDs](#31-project-design-document-pdd), [MRVs](#32-monitoring-reporting-and-verification-mrv), and [CRUs](#34-carbon-removal-units-crus). It MAY coordinate with external systems such as verification bodies or monitoring data providers.

* The **Ledger Layer** anchors critical registry state to an immutable, cryptographically verifiable record. It SHALL record document hashes, lifecycle events, and token-related operations. It MUST support auditability and MAY expose events for off-chain synchronization.

This architecture provides the operational boundaries necessary to support auditability, traceability, and certification workflows aligned with the EU Regulation 2024/3012 [[4](#ref-4)]. All implementations claiming conformance SHALL implement and integrate these layers in accordance with the specifications defined herein.

### 2.2 Data Flow

This specification defines the canonical data flows required to support lifecycle operations within a conforming registry system. These flows govern project registration, monitoring, verification, and issuance of removal attestations. Each transition SHALL be deterministic, auditable, and linked to a canonical document reference as defined in in this specification.

* **Project Registration** begins with the submission of a [Project Design Document (PDD)](#31-project-design-document-pdd) through the API layer. The system SHALL validate schema compliance, methodology references, and spatial boundaries. Upon acceptance, a unique project identifier SHALL be assigned, and a document hash SHALL be anchored in the [Ledger Layer](#21-architectural-overview).

* **Monitoring and Verification** involves the submission of [Monitoring, Reporting, and Verification (MRV)](#32-monitoring-reporting-and-verification-mrv) documents for approved projects. These documents SHALL include quantified removal estimates, methodology-specific inputs, and verification metadata. Verified MRVs SHALL be cryptographically linked to the corresponding PDDs and SHALL serve as the basis for issuance.

* **Credit Management** includes the creation, transfer, and retirement of [Carbon Removal Units (CRUs)](#34-carbon-removal-units-crus). Each CRU SHALL represent a verified quantity of net removal and SHALL be traceable to its source MRV. All issuance and lifecycle operations MUST be anchored on-chain and recorded for auditability.

These flows are mandatory for conformance and SHALL be implemented in accordance with the interface, validation, and ledger requirements defined in this specification.

### 2.3 Integration Patterns

This specification defines required integration patterns that ensure consistency, traceability, and interoperability across registry systems, blockchain networks, and external data sources. These patterns are normative and SHALL be implemented as specified to ensure conformance.

* **Registry Federation**
  Conforming implementations MAY participate in federated registry networks. Federated systems SHALL implement mechanisms to prevent credit double counting, preserve document provenance, and ensure unique identifiers across jurisdictions. Federation models MUST conform to the document structure and state management rules defined in this specification.

* **Ledger Integration**
  All conforming systems SHALL implement ledger anchoring of document hashes and state transitions as defined in [Section 5](#5-smart-contract-requirements). Implementations MAY abstract underlying blockchain infrastructure, provided that minimum data availability and auditability guarantees are preserved. Optimizations for gas efficiency and chain selection are permitted but MUST retain hash consistency and public verifiability.

* **External System Integration**
  Systems MAY interoperate with verifiers, monitoring data providers, or market platforms. All integrations SHALL use authenticated communication protocols and standardized data representations as defined in this specification. Off-chain processes involved in validation or verification MUST maintain traceable links to their associated on-chain references.


## 3. Core Data Models

![Core Data Models](../diagrams/core-data-models-class.png)
*Figure 4: UML class diagram of canonical document types and their relationships.*

This specification defines three canonical document types used to represent project declarations, monitoring results, and verified removal units. All core documents SHALL be serialized as GeoJSON Features [[1](#ref-1)] and SHALL follow schema constraints defined in the corresponding conformance classes.

### 3.1 Project Design Document (PDD)

The Project Design Document (PDD) defines the foundational parameters of a carbon removal project. It establishes the spatial scope, governance, and methodological basis against which monitoring, verification, and issuance processes are evaluated. Each PDD SHALL conform to the GeoJSON Feature model and SHALL declare `profile: "pdd"` to enable schema validation.

#### 3.1.1 PDD Fields

| Field Name         | Type                                                | Description                                                                                                                                                                                                 |
| ------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`             | string                                              | **REQUIRED.** MUST be `"Feature"` per GeoJSON. Identifies the object as a geographic feature with spatial footprint and metadata.                                                                          |
| `id`               | string                                              | **REQUIRED.** Globally unique, immutable identifier for the PDD. MUST be stable across versions. Recommended: UUIDv4 or hash-based ID.                                                                      |
| `crgf_version`     | string                                              | **REQUIRED.** Indicates the version of the CRGF spec this document conforms to. Follows [Semantic Versioning](https://semver.org).                                                                           |
| `profile`          | string                                              | **REQUIRED.** MUST be `"pdd"`. Identifies the document type for validation purposes.                                                                                                                        |
| `geometry`         | GeoJSON Geometry Object                             | **REQUIRED.** Geographic footprint of the project. MUST comply with [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946). Typically a `Polygon` or `MultiPolygon`. Used for spatial indexing and MRV validation. |
| `bbox`             | \[number]                                           | REQUIRED if `geometry` is not null. Bounding box array for fast spatial filtering. Format: `[west, south, east, north]`.                                                                                    |
| `properties`       | [PDD Properties Object](#312-pdd-properties-object) | **REQUIRED.** Domain-specific metadata about the project.                                                                                                            |
| `ledger_reference` | [Ledger Reference Object](#331-ledger-reference-object) | OPTIONAL. Added by the registry or notarization service. Records the hash anchoring on-chain. Immutable proof of document existence.                                                                        |
| `links`            | \[[Link Object](#332-link-object)]                      | OPTIONAL. Related resources such as methodologies, MRVs, and provenance relations. MUST include at least a `self` link if present.                                                                          |

> **Control Metadata Principle**: All fields outside `properties` are control metadata supporting governance, versioning, lifecycle traceability, and interoperability. They MUST NOT be altered during domain-specific content editing.

#### 3.1.2 PDD Properties Object

The `properties` object contains project-specific metadata owned and edited by the project proponent. These fields support validation, monitoring, lifecycle transitions, and CRU issuance.

| Field Name      | Type   | Description                                                                                                                                                                       |
| --------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`          | string | **REQUIRED.** Human-readable project name. Should remain stable across document versions.                                                                                         |
| `description`   | string | Short summary of project goals, scope, and expected outcomes.                                                                                                                     |
| `creation_date` | string | ISO 8601 date of initial submission. Immutable.                                                                                                                                   |
| `last_updated`  | string | ISO 8601 timestamp of last substantive update. Updated only when project content changes, not ledger metadata.                                                                    |
| `project_type`  | string | Classification of removal activity (e.g., `"soil_carbon"`, `"afforestation"`). SHOULD align with methodology domain.                                                              |
| `status`        | string | Current PDD lifecycle state. MUST be one of: `draft`, `submitted`, `under_review`, `approved`, `rejected`, `archived`. Used to control downstream actions. |
| `version`       | string | Version label of the PDD payload. Follows internal project versioning scheme (e.g., `"v1.0"`).                                                                                     |
| `actor_id`      | string | Reference to the authorized project proponent, as defined in the [Actor Profile](actor.md). MUST be resolvable.                                                                   |

#### 3.1.3 Canonical Serialization and Ledger Anchoring

CRGF PDD documents MUST be serialized deterministically prior to cryptographic hashing for ledger anchoring. The hash SHALL be computed on the canonical JSON string using SHA-256 or another registry-approved algorithm.

**Hash Scope**

The entire PDD object, including nested fields, SHALL be included in the canonical serialization. If the `ledger_reference` field is present, it MUST be removed prior to serialization to avoid circular dependencies.

**Canonicalization Rules**

1. Object keys SHALL be sorted lexicographically at all levels.
2. Insignificant whitespace SHALL be removed.
3. The resulting JSON string SHALL be UTF-8 encoded before hashing.

#### 3.1.4 Registry Workflow Integration

The PDD plays a foundational role in the lifecycle of a carbon project within a registry system.

1. **Preparation** – The project proponent prepares the PDD according to the CRGF schema and lifecycle rules.
2. **Submission to Registry** – The PDD is submitted to a compliant registry endpoint via the API, typically in the `draft` state.
3. **Schema Conformance Check** – The registry performs automated checks against `pdd-schema.json` to verify required fields, geometry, and link consistency.
4. **Canonicalization and Hashing** – After conformance, the PDD (excluding `ledger_reference`) is canonically serialized and hashed.
5. **Ledger Anchoring** – The hash is notarized on the ledger and the resulting `ledger_reference` is injected into the document.
6. **State Transition** – Upon successful anchoring, the PDD transitions to a new lifecycle state (`submitted` or `approved`) according to registry policy. No further edits are permitted.

### 3.2 Monitoring, Reporting, and Verification (MRV)

The MRV document captures quantitative results from project monitoring and verification activities. Serialized as a GeoJSON Feature, it records monitoring periods, methodology inputs, net removal calculations, and verification outcomes. Each MRV MUST link to a single parent PDD and represent a distinct monitoring interval.

#### 3.2.1 MRV Fields

| Field Name         | Type                                                | Description                                                                                                                                 |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`             | string                                              | **REQUIRED.** MUST be `"Feature"` per GeoJSON. Identifies the object as a geographic feature with spatial footprint and metadata.            |
| `id`               | string                                              | **REQUIRED.** Globally unique, immutable identifier for the MRV. MUST be stable across versions. Recommended: UUIDv4 or hash-based ID.      |
| `crgf_version`     | string                                              | **REQUIRED.** Indicates the version of the CRGF spec this document conforms to. Follows [Semantic Versioning](https://semver.org).          |
| `profile`          | string                                              | **REQUIRED.** MUST be `"mrv"`. Identifies the document type for validation purposes.                                                        |
| `geometry`         | GeoJSON Geometry Object                             | **REQUIRED.** Geographic footprint of the project. MUST comply with [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946).               |
| `bbox`             | [number]                                           | REQUIRED if `geometry` is not null. Bounding box array for fast spatial filtering. Format: `[west, south, east, north]`.                   |
| `properties`       | [MRV Properties Object](#322-mrv-properties-object) | **REQUIRED.** Domain-specific metadata about the monitoring results, calculations, and verification status.                               |
| `ledger_reference` | [Ledger Reference Object](#331-ledger-reference-object) | OPTIONAL. Added by the registry or notarization service. Records the hash anchoring on-chain.                                             |
| `links`            | [[Link Object](#332-link-object)]                   | OPTIONAL. Related resources such as methodologies, PDDs, datasets, and provenance relations. MUST include at least a `self` link if present. |

> **Control Metadata Principle**: All fields outside `properties` are control metadata supporting governance, versioning, lifecycle traceability, and interoperability. They MUST NOT be altered during domain-specific content editing.

#### 3.2.2 MRV Properties Object

The `properties` object encapsulates the domain-specific content of the MRV document, including monitoring results, calculations, and verification status.

| Field Name             | Type                                                        | Description                                                                                                                                    |
| ---------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `project_id`           | string                                                      | **REQUIRED.** References the `id` of the associated PDD Feature. Ensures the MRV is correctly linked to a certified project scope.            |
| `methodology_id`       | string                                                      | **REQUIRED.** Identifier of the methodology applied for monitoring and calculation. Enables schema validation of methodology data.            |
| `start_date`           | string (ISO 8601)                                           | **REQUIRED.** Start date of the monitoring period covered by this report.                                                                      |
| `end_date`             | string (ISO 8601)                                           | **REQUIRED.** End date of the monitoring period covered by this report.                                                                        |
| `methodology_data`     | [Methodology Data Object](#323-methodology-data-object)     | **REQUIRED.** Structured container for method-specific measurements and inputs.                                                                |
| `net_removal_estimate` | [Net Removal Estimate Object](#324-net-removal-estimate-object) | **REQUIRED.** Reported net benefit of the monitoring period, including unit and basis.                                                        |
| `total_uncertainty`    | [Uncertainty Object](#325-uncertainty-object)               | OPTIONAL. Characterizes the uncertainty of the benefit estimate.                                                                               |
| `verification_status`  | string (enum)                                               | OPTIONAL. Current verification state. Valid values: `unverified`, `pending`, `verified`, `rejected`.                                           |
| `verification_date`    | string (ISO 8601)                                           | OPTIONAL. Date when verification was completed. Required if `verification_status = verified`.                                                  |
| `verifier_info`        | [Verifier Object](#326-verifier-object)                     | OPTIONAL. Information about the verifying entity or person.                                                                                    |
| `raw_data`             | array of [Raw Data Reference](#327-raw-data-reference-object) | OPTIONAL. References to original measurement datasets or acquisition sources.                                                                  |
| `links`                | array of [Link Object](#332-link-object)                    | OPTIONAL. External or internal references, e.g., related documentation, datasets, registry entries.                                            |

#### 3.2.3 Methodology Data Object

| Field Name            | Type                                     | Description                                                                                                 |
| --------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `parameters`          | object                                   | Key-value map of input parameters specific to the methodology.                                              |
| `measurement_devices` | array of object              | Description of the instruments used to collect data, including identifiers or model information.             |
| `sampling_strategy`   | string                                   | Description of spatial or temporal sampling approach.                                                       |
| `data_quality_flags`  | object                                   | Optional flags or indicators on data reliability.                                                           |
| `processing_notes`    | string                                   | Free text field for preprocessing, adjustments, or calculation assumptions.                                 |

#### 3.2.4 Net Removal Estimate Object

| Field Name | Type   | Description                                           |
| ---------- | ------ | ----------------------------------------------------- |
| `value`    | number | **REQUIRED.** Estimated net removal quantity.         |
| `unit`     | string | **REQUIRED.** Measurement unit (e.g., `"tCO2e"`).     |
| `basis`    | string | OPTIONAL. Description of the calculation context.     |

#### 3.2.5 Uncertainty Object

| Field Name         | Type   | Description                             |
| ------------------ | ------ | --------------------------------------- |
| `min`              | number | Lower bound of uncertainty interval.    |
| `max`              | number | Upper bound of uncertainty interval.    |
| `confidence_level` | number | Confidence level (e.g., `0.95` for 95%). |

#### 3.2.6 Verifier Object

| Field Name         | Type   | Description                                            |
| ------------------ | ------ | ------------------------------------------------------ |
| `organization`     | string | Name of the verifying organization.                    |
| `accreditation_id` | string | Accreditation identifier issued by a registry or body. |
| `reviewer_name`    | string | OPTIONAL. Individual responsible for the review.       |

#### 3.2.7 Raw Data Reference Object

| Field Name    | Type   | Description                                                             |
| ------------- | ------ | ----------------------------------------------------------------------- |
| `id`          | string | Unique identifier for the raw data source.                              |
| `type`        | string | Type of data (e.g., `"lidar"`, `"soil_sample"`, `"satellite_imagery"`). |
| `access_uri`  | string | URI or path where the data can be retrieved.                            |
| `description` | string | Short description of the dataset.                                       |

#### 3.2.8 Canonical Serialization and Ledger Anchoring

MRV documents MUST be serialized deterministically prior to cryptographic hashing for ledger anchoring. The canonicalization and hashing requirements are identical to those defined in [Section 3.1.3](#313-canonical-serialization-and-ledger-anchoring). The `ledger_reference` field is added after hashing and MUST NOT be included in the hash input.

### 3.3 Common Object Structures

Canonical object definitions reused across PDD and MRV documents.

#### 3.3.1 Ledger Reference Object

This object links canonical documents (e.g., PDDs and MRVs) to their notarized state on a blockchain or distributed ledger. It is added post-submission and is used for anchoring, integrity proof, and non-repudiation.

| Field Name       | Type    | Description |
| ---------------- | ------- | ----------- |
| `transaction_id` | string  | **REQUIRED.** Transaction hash or ID on the ledger. Used to verify the presence of the content hash on-chain. |
| `block_number`   | integer | **REQUIRED.** Block number containing the transaction. Aids in timeline reconstruction and conflict resolution. |
| `timestamp`      | string  | **REQUIRED.** ISO 8601 UTC timestamp of the notarization event. |
| `ledger_id`      | string  | **REQUIRED.** Identifier of the ledger network (e.g., `eth-mainnet`, `polygon-testnet`). Used for multi-ledger resolution. |

#### 3.3.2 Link Object

Links define structured relationships between canonical documents, enabling traceability and navigation within the registry system.

| Field   | Type   | Description |
| ------- | ------ | ----------- |
| `rel`   | string | **REQUIRED.** Relationship type. |
| `href`  | string | **REQUIRED.** Fully qualified URI of the linked resource. |
| `type`  | string | Optional MIME type of the target resource (e.g., `application/json`). |
| `title` | string | Optional human-readable description of the resource. |

##### Recommended `rel` values for PDD

| `rel` value   | Description |
| ------------- | ----------- |
| `self`        | Link to the current PDD document instance. |
| `related-mrv` | Reference to an associated MRV document. |
| `methodology` | Link to the methodology document referenced by the PDD. |
| `monitor`     | External monitoring data sources. |
| `predecessor` | Link to a previous version of the PDD. |
| `successor`   | Link to the next version of the PDD (if available). |

##### Recommended `rel` values for MRV

| `rel` value      | Description |
| ---------------- | ----------- |
| `self`           | Link to the current MRV document instance. |
| `pdd`            | Reference to the associated Project Design Document. |
| `methodology`    | Link to the methodology used for calculations and verification. |
| `supporting-doc` | External documents providing evidence or reports supporting the MRV claims. |
| `data-source`    | Source systems or repositories containing raw monitoring data. |
| `verifier`       | Profile or identifier of the verifying entity or actor. |
| `predecessor`    | Link to a previous version of the MRV document. |
| `successor`      | Link to the next version of the MRV document (if available). |

##### Best Practices

* Use HTTPS URIs that are resolvable and permanent.
* Avoid relative URLs; use absolute paths to ensure portability.
* Provide `type` and `title` where applicable to facilitate automated and human interpretation.

### 3.4 Carbon Removal Units (CRUs)

Carbon Removal Units (CRUs) represent attested net removals of CO₂ equivalent. Each CRU SHALL be linked to a validated MRV and a parent PDD, and SHALL correspond to a quantifiable and verifiable removal amount.

CRUs SHALL be uniquely identifiable and SHALL include metadata that binds them to the underlying monitoring and verification context. Implementations MAY use token-based representations such as ERC-721 for lifecycle tracking, transferability, and retirement.

CRUs MAY be issued in fractional quantities where permitted by the registry. Each unit SHALL retain a one-to-one mapping to its provenance data. Retired CRUs SHALL be excluded from transfer and SHALL be cryptographically flagged as withdrawn from circulation.


## 4. API Design

### 4.1 API Design Philosophy

The OGCR API defines a resource-oriented interface for managing registry artifacts and lifecycle operations. All endpoints SHALL conform to REST architectural constraints and SHALL operate over standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).

The API SHALL expose resource collections for projects, monitoring reports, and removal units. Each resource type SHALL implement a consistent set of operations for creation, retrieval, update (where allowed), and archival.

Implementations SHALL require only the minimum data necessary for conformance with the document schema and lifecycle rules. Optional fields MAY be used for extended functionality, provided they do not conflict with required validation logic.

Error responses SHALL follow a uniform structure, including HTTP status codes, machine-readable error identifiers, and human-readable messages. Validation errors SHALL include field-level annotations and reason codes.

The API interface, including endpoints, parameters, request/response structures, and authentication flows, SHALL be documented in a machine-readable format (e.g., OpenAPI). The documentation SHALL include example requests and expected responses for each operation.

### 4.2 Core API Endpoints

The OGCR API defines a set of resource-oriented endpoints for managing the lifecycle of registry documents and issued carbon removal units. Each endpoint group corresponds to a distinct functional process: project registration, monitoring and verification, and credit issuance and retirement.

All endpoints SHALL implement authenticated access, schema validation, and consistent response structures.

#### 4.2.1 Project Management

Project endpoints manage the creation, retrieval, update, and status tracking of carbon removal projects. A project is represented by a Project Design Document (PDD) and is associated with a unique identifier.

* **`POST /projects`**

  Submits a new project to the registry. The request body SHALL conform to the canonical PDD schema. The system SHALL validate document structure, methodology reference, and spatial geometry. Upon acceptance, a unique project identifier SHALL be issued and the PDD SHALL enter the `submitted` state.

![Project Registration Workflow](../diagrams/project-registration-sequence.png)
*Figure 2: Project registration lifecycle, from submission to validation and anchoring.*

* **`GET /projects/{projectId}`**

  Retrieves the full project record, including document content, status, version history, and links to associated monitoring reports.

* **`PUT /projects/{projectId}`**

  Updates a project document prior to validation. After validation, modifications SHALL be restricted to permitted metadata fields (e.g., contact information). All changes SHALL be versioned and timestamped.

* **`GET /projects`**

  Returns a paginated list of project entries. Query parameters MAY include status, methodology, actor, bounding box, and creation or approval date ranges.

#### 4.2.2 Monitoring and Verification

Monitoring endpoints handle submission and retrieval of monitoring reports (MRVs). Verification endpoints manage the attestation process by authorized verifiers.

* **`POST /projects/{projectId}/monitoring`**

  Submits a monitoring report for the specified project. The report SHALL conform to the MRV schema and SHALL not overlap temporally with any existing MRV for the same project. The system SHALL validate schema conformance, reporting period boundaries, and methodology consistency.

![MRV Workflow](../diagrams/mrv-workflow-sequence.png)
*Figure 3: MRV submission, verification, and issuance process.*

* **`GET /projects/{projectId}/monitoring`**

  Returns monitoring reports associated with a project. Filtering options MAY include reporting period, verification status, or verifier identity.

* **`POST /projects/{projectId}/monitoring/{reportId}/verify`**

  Submits a verification decision. Only authorized verifiers MAY call this endpoint. The request SHALL include verification status, documented outcome, and the amount of verified removal in metric tonnes CO₂e. Upon acceptance, the system SHALL update the MRV status and trigger credit issuance logic.

#### 4.2.3 Credit Management

Credit endpoints manage the lifecycle of Carbon Removal Units (CRUs), from issuance through transfer and retirement. Each unit represents a verified quantity of net CO₂ removal.

* **`GET /credits`**

  Returns a list of issued CRUs. Query parameters MAY include project ID, issuance year, owner address, and retirement status.

* **`POST /credits/transfer`**

  Transfers one or more CRUs to a new account. The request MUST include identifiers for the units to be transferred and the recipient’s address. The system SHALL verify ownership, recipient eligibility, and transaction validity before completing the operation.

* **`POST /credits/{creditId}/retire`**

  Permanently retires a CRU. The request SHALL include the retirement reason and MAY include beneficiary or use-case metadata. Retired units SHALL become non-transferable and remain publicly traceable in the registry.

### 4.3 Authentication and Authorization

The OGCR API SHALL implement authentication and authorization mechanisms to control access to registry operations. Access control MUST be enforced at the interface, resource, and operation levels.

* **OAuth 2.0**

  SHALL be supported for authenticating human users and web-based clients. Supported flows SHALL include authorization code and client credentials. Access tokens SHALL define scoped permissions, restricting access to specific endpoints and operations.

* **API Keys**

  MAY be issued for server-to-server integrations or automated agents. Each API key SHALL be bound to an organization and associated with defined scopes and rate limits. Keys SHALL be revocable.

* **Role-Based Access Control (RBAC)**

  SHALL be used to restrict operations based on assigned roles. Core roles include `developer`, `verifier`, `operator`, and `holder`. Each role SHALL be associated with a defined set of permissions. The system SHALL validate role-based permissions on all sensitive operations.

All access attempts and authorization decisions SHALL be logged. Audit logs SHALL record timestamps, actor identity, resource identifiers, and outcome status. Logs MUST be available for inspection by authorized administrators.

### 4.4 Data Validation and Quality Assurance

All submitted documents and requests to the API SHALL be subject to multi-level validation to ensure schema compliance, business rule conformity, and data quality.

Registries implementing this specification SHOULD support validation dashboards and issue tracking interfaces to enable continuous improvement in submission accuracy and consistency.

#### 4.4.1 Schema Validation

Schema Validation SHALL be applied to all resource submissions. Each core document type (PDD, MRV) SHALL be validated against its corresponding JSON Schema ([PDD Schema](../schemas/pdd-schema.json) or [MRV Schema](../schemas/mrv-schema.json))

Validation SHALL include type checking, required fields, format constraints, and enumerated values. Error responses MUST reference the failing field and SHALL include human-readable correction guidance.

#### 4.4.2 Business Rule Validation

Business Rule Validation SHALL enforce constraints beyond schema structure, including:

  * Non-overlapping monitoring periods per project
  * Valid methodology reference and version
  * Non-intersecting project geometries
  * Role-based operation limits

These rules MAY be adapted based on jurisdictional or methodological requirements and SHALL be documented.

#### 4.4.3 Data Quality Assessment

MAY be applied to submitted documents. Quality indicators MAY include completeness, internal consistency, and adherence to reporting best practices. The registry MAY assign a non-normative quality score to each submission for reporting or review prioritization purposes.

### 4.5 Performance and Scalability

The OGCR API SHALL support scalable operation under variable load conditions. Implementations SHALL include mechanisms for performance optimization, fault tolerance, and efficient access to large datasets.

Implementations SHOULD monitor system performance and provide administrative access to runtime metrics for operational oversight.

#### 4.5.1 Caching

Responses to frequently accessed resources MAY be cached at the server or proxy level. Cache invalidation mechanisms SHALL ensure consistency with underlying registry state. Time-to-live (TTL) policies and conditional request headers (e.g., `ETag`) MAY be used.

#### 4.5.2 Pagination and Filtering

Collection endpoints SHALL support pagination. Offset-based pagination SHALL be supported by default; cursor-based pagination MAY be provided for large or real-time datasets. Query parameters for filtering and sorting by attributes (e.g., status, date, geography) SHALL be implemented to limit payload size and improve response performance.

#### 4.5.3 Asynchronous Operations

Time-intensive processes such as schema validation, verification submission, and ledger anchoring MAY be handled asynchronously. The initiating endpoint SHALL return a task identifier, and a separate status endpoint SHALL provide progress updates and final outcomes.

#### 4.5.4 Rate Limiting

The API SHALL enforce rate limits to manage resource usage. Limits MAY vary by role, client type, or endpoint category. When a rate limit is exceeded, the API SHALL return an HTTP 429 response with a `Retry-After` header.


## 5. Smart Contract Requirements

### 5.1 Smart Contract Architecture

The OGCR Specification defines requirements for smart contracts that SHALL provide immutable state anchoring, verifiable state transitions, and support for decentralized governance. The architecture SHALL follow modular design principles and MUST emit event logs for all critical operations.

#### 5.1.1 Modular Contract Design

Smart contract logic SHALL be separated into components with defined responsibilities. Each contract SHALL handle one core function: project registration, MRV anchoring, unit issuance, or access control. Contracts MAY be independently deployed and upgraded.

#### 5.1.2 Upgradeability

Implementations MAY use proxy patterns to enable logic upgrades. Upgrade mechanisms SHOULD include governance constraints such as delay periods, multi-signature authorization, or stakeholder voting. State variables MUST remain consistent across upgrades.

#### 5.1.3 Event Emission

All state-changing actions (e.g., registration, approval, issuance) MUST emit events. Events SHALL include sufficient metadata to support off-chain indexing, registry reconciliation, and external monitoring.

### 5.2 Core Contract Types

A conforming implementation SHALL deploy the following smart contract types. Each contract SHALL expose interfaces required for integration with the API and registry backend. Access to state-changing functions MUST be restricted to authorized roles.

#### 5.2.1 Project Registry Contract

The Project Registry Contract SHALL store immutable references to submitted project design documents and track project lifecycle status.

* **Registration**

  The contract SHALL accept project document hashes, unique identifiers, and metadata submitted by authorized actors. On success, the contract SHALL emit a `PDDRegistered` event.

* **Approval and Rejection**

  Validators MAY update project status by invoking approval or rejection functions. Each decision MUST be logged with a timestamp and validator address. Rejections MAY include justification metadata.

* **Status Transitions**

  Projects MAY transition through states including `draft`, `submitted`, `validated`, `rejected`, or `archived`. Each transition MUST be recorded via event emission.

![Project Lifecycle States](../diagrams/lifecycle-states.png)
*Figure 5: Valid state transitions for registered projects.*

Read access to project metadata and status MUST be publicly available. Write operations MUST be restricted to accounts with appropriate roles (e.g., `developer`, `validator`, `operator`).

#### 5.2.2 MRV Registry Contract

The MRV Registry Contract SHALL manage hashes and metadata for monitoring, reporting, and verification (MRV) records. Each MRV record MUST reference an approved project and a specific reporting period.

* **Submission**

  Authorized actors MAY submit monitoring report hashes along with associated metadata. The contract SHALL validate that the referenced project is approved and that the reporting period does not overlap with existing entries.

* **Verification**

  Authorized verifiers MAY record verification outcomes, including net removal quantities and dates. The contract MUST emit a `MRVVerified` event containing the MRV ID, verifier address, and quantified amount.

* **Hash Integrity**

  The contract SHALL store cryptographic hashes of each MRV report. Off-chain systems MAY verify report integrity by comparing content hashes to on-chain references.

Temporal constraints MUST ensure that monitoring reports do not overlap and that all periods align with project timelines and methodology requirements.

#### 5.2.3 Carbon Credit Token Contract

The Carbon Credit Token Contract SHALL represent Carbon Removal Units (CRUs) as non-fungible tokens (NFTs) conforming to the ERC-721 standard [[3](#ref-3)]. Each token MUST represent a verified quantity of carbon removal and MUST be traceable to its source MRV and project.

* **Minting**

  Only authorized actors MAY mint tokens. Each mint operation MUST reference a verified MRV, and the resulting token MUST include metadata fields for project ID, MRV ID, vintage year, and amount. A `CRUMinted` event MUST be emitted.

* **Transfer**

  Token holders MAY transfer tokens subject to registry rules. All transfers MUST be logged with timestamps and involved addresses. Optional restrictions MAY be applied based on regulatory constraints or credit type.

* **Retirement**

  Tokens MAY be retired to finalize a carbon offset claim. Retired tokens MUST be non-transferable and MUST retain all metadata for auditability. A `CRURetired` event MUST be emitted with a reason code.

Each token’s metadata structure SHALL include project identifiers, reporting period, carbon amount, issuance and retirement status, and any relevant compliance attributes.

#### 5.2.4 Access Control Contract

The Access Control Contract SHALL define and enforce role-based permissions across all smart contract components. It SHALL provide centralized role assignment and delegation, authorization enforcement, and support for multi-signature governance.

* **Role Management**

  The contract SHALL implement functions to assign, update, and revoke roles. Roles SHALL include at minimum:

  * `developer`
  * `verifier`
  * `registry_operator`
  * `administrator`

  Each role SHALL be associated with a predefined set of permissions. Role changes SHALL emit traceable events.

* **Authorization Logic**

  All state-changing functions across contracts SHALL invoke permission checks defined in the access control layer. Unauthorized calls SHALL revert. Authorization failures SHALL be logged.

* **Multi-Signature Operations**

  The contract MAY support multi-signature approval for selected administrative functions, including role assignment and contract upgrades. Thresholds SHALL be configurable and enforced at the contract level.

* **Emergency Controls**

  The contract MAY implement pause and recovery mechanisms. These SHALL be restricted to privileged roles and SHALL emit events recording the initiating actor and timestamp.

### 5.3 Integration Requirements

Smart contracts defined by this specification SHALL interoperate with off-chain registry systems. All on-chain actions affecting registry state SHALL emit events suitable for real-time or deferred processing.

#### 5.3.1 Event Monitoring

Off-chain components SHALL subscribe to contract events to maintain registry state. Event handlers SHALL implement error handling, deduplication, and retry logic. Events SHALL include sufficient metadata to reconstruct associated off-chain actions.

#### 5.3.2 State Synchronization

Registries SHALL implement synchronization mechanisms to resolve discrepancies between ledger and database state. Reconciliation procedures SHALL be invoked on failure or inconsistency. Blockchain reorganizations SHALL be accounted for.

#### 5.3.3 Gas Optimization

Contract functions SHALL be designed to minimize execution costs. Implementations MAY include batch operations and efficient data encoding. Computation-heavy tasks SHOULD be offloaded to the registry or avoided entirely.

#### 5.3.4 Network Compatibility

Contracts SHALL support deployment across multiple EVM-compatible networks. Network-specific parameters (e.g., gas limits, block time) SHALL be configurable. Interactions with external systems SHALL account for network constraints and finality assumptions.

### 5.4 Security Requirements

Smart contracts implementing this specification SHALL include controls to mitigate known vulnerabilities and ensure secure operation throughout their lifecycle. Security requirements apply to all contract modules and interfaces affecting registry state or token issuance.

#### 5.4.1 Access Control Validation

All externally accessible functions SHALL validate the caller's permissions prior to execution. Role-based access control MUST be enforced consistently. Critical operations MAY include multi-signature thresholds. Emergency pause and recovery functions SHALL be restricted to privileged roles.

#### 5.4.2 Input Validation

Contracts SHALL validate input parameters for type, range, and expected state conditions. This includes protection against arithmetic overflows, zero-value identifiers, and inconsistent internal state. Inputs affecting identifiers, timestamps, or transfer amounts MUST be explicitly checked.

#### 5.4.3 Reentrancy Protection

Contracts SHALL prevent reentrancy by applying function modifiers or the checks-effects-interactions pattern. Functions that modify contract state and initiate external calls MUST implement explicit reentrancy guards.

#### 5.4.4 Upgrade Security

If upgradeable proxy patterns are used, upgrade operations SHALL be protected by governance procedures. These MAY include time-locked execution, multi-party approval, and audit checkpoints. Migration functions MUST ensure state continuity and prevent unauthorized access.

#### 5.4.5 Audit and Verification

All contract modules affecting issuance, registry status, or state transitions SHALL undergo security review prior to deployment. Audit processes MAY include:

* Static analysis
* Manual code review
* Test coverage reporting
* Formal verification (where applicable)

Audits SHALL be repeated after any material change to contract logic. Results SHOULD be published where transparency is required by the registry governance policy.


## 6. Extensibility Framework

The specification defines a modular extensibility framework that allows registry systems to incorporate new carbon removal methodologies without altering the core protocol. Methodologies MAY define custom rules for monitoring, quantification, and validation, provided they conform to the interface and schema extension mechanisms defined below.

### 6.1 Methodology Extension System

This specification supports the use of versioned methodologies to define quantification logic, input requirements, validation procedures, and conformance rules for carbon removal activities.

The process of introducing, modifying, or approving methodologies SHALL be subject to registry-level governance, as defined in Section 6.3. In regulated environments, methodology approval SHALL conform to applicable legal frameworks, including Article 8 of Regulation (EU) 2024/3012 [[4](#ref-4)]. The governance process MAY involve public consultation, expert review, or delegated authority.

#### 6.1.1 Methodology Registration

Each methodology SHALL be registered with a globally unique identifier, semantic version string, list of supported project types, and references to applicable monitoring protocols and calculation procedures.

Only registered methodologies MAY be referenced in PDD or MRV documents. Revisions to a methodology that affect validation, calculation, or conformance SHALL result in a new version. A registry MAY impose governance review or approval conditions prior to activation or publication of a methodology.

#### 6.1.2 Schema Extension

Registered methodologies MAY extend the core schemas for PDD and MRV documents using [JSON Schema composition](https://json-schema.org/understanding-json-schema/structuring.html). Extensions SHALL NOT override or remove any required fields defined in the base schema. All additional fields SHALL be namespaced to avoid naming collisions and SHALL maintain backward compatibility.

#### 6.1.3 Validation Plugin Architecture

Methodologies MAY include executable validation logic. Plugins SHALL operate in isolated environments and SHALL accept only document inputs and associated metadata. Plugins SHALL return a machine-readable validation result and SHALL NOT modify registry state or access external resources.

Plugin deployment MAY be subject to governance approval. All plugin logic SHALL be version-controlled and auditable.

#### 6.1.4 Calculation Engine Integration

Methodologies MAY delegate quantification to an external calculation engine that implements a deterministic input/output contract. Engines SHALL accept structured monitoring data and produce a net removal estimate with associated uncertainty bounds.

Calculation logic SHALL be transparent and reproducible. Registries MAY cache, inspect, or independently verify outputs. Governance policies MAY define procedures for engine registration, audit, or revocation.

### 6.2 Integration Extension Points

The specification defines extension points for interoperating with external systems and services. These extension points SHALL enable integration without altering core registry logic or compromising data integrity.

#### 6.2.1 Data Source Connectors

Connectors MAY be implemented to ingest data from external sources, including satellite imagery, IoT sensors, and third-party monitoring platforms. Each connector SHALL support:

* Authenticated data retrieval
* Format transformation to registry-compliant structures
* Provenance tracking and timestamp preservation

Connectors SHALL NOT modify core registry data. Data received via connectors SHALL be treated as input to monitoring or validation processes.

#### 6.2.2 Verification Service Integration

Verification workflows MAY be delegated to accredited third-party services. The registry SHALL support:

* Verifier identity resolution and credential validation
* Submission and retrieval of verification documents
* Recording of outcomes with audit references

Verification services SHALL operate independently of project developers and SHALL comply with applicable role-based access controls.

#### 6.2.3 Federated Platform Integration

Registries MAY expose endpoints for integration with trading platforms, offset marketplaces, and federation networks. Market-facing interfaces SHALL include:

* Access to certified unit metadata
* Traceability to originating MRV and PDD
* Status updates reflecting transfer, retirement, or revocation

Federated registries SHALL implement conflict prevention mechanisms to avoid duplicate issuance or double use.

#### 6.2.4 Regulatory Reporting Integration

Registry systems MAY support automated reporting to public or private compliance authorities. Reporting interfaces SHALL enable:

* Data export in regulatory-compliant formats
* Schedule-based or event-based submission
* Confirmation logging and delivery status tracking

Personal and sensitive data submitted to regulatory bodies SHALL be protected in accordance with applicable legal requirements.

### 6.3 Governance Extension Framework

The Governance Extension Framework defines optional mechanisms that MAY be implemented by registry operators to support structured participation, oversight, and transparency. It enables stakeholder engagement in operational and methodological decision-making, while preserving the integrity of the core specification.

This extension does not modify conformance classes, document schemas, or defined lifecycle transitions. It applies only to registry-level governance processes that operate within the normative boundaries of this specification.

#### 6.3.1 Scope and Limitations

Governance extensions MAY be used to manage:

* Proposals for methodology additions or updates
* Operational policy decisions (e.g., audit frequency, data disclosure rules)
* Verifier accreditation, registry service provider oversight, or stakeholder participation
* Controlled adoption of new specification versions or optional modules
* Dispute resolution, audit response, and compliance enforcement

They SHALL NOT override:

* Canonical document structures (PDD, MRV, CRU)
* Defined lifecycle transitions or validation logic
* Hashing, anchoring, and reconciliation procedures
* Specification-level conformance rules

#### 6.3.2 Governance Procedures

A registry implementing this extension MAY define one or more of the following procedures:

* **Proposal System**

  Registries MAY implement a structured process for submitting and evaluating governance or methodology proposals. Proposals SHOULD include an impact assessment, implementation plan, and record of stakeholder consultation.

* **Voting Mechanisms**

  Where applicable, proposals MAY be subject to stakeholder voting. Voting systems SHALL define eligibility, quorum thresholds, voting weights (if applicable), and time limits. Results SHALL be recorded and implemented according to predefined rules.

* **Advisory Committee Integration**

  Registries MAY establish advisory committees to provide technical or policy guidance. Procedures for committee formation, member selection, meeting management, and recommendation tracking SHALL be documented.

* **Audit and Compliance Framework**

  Registries MAY define independent audit mechanisms for registry operations, certification workflows, or governance decisions. Audit procedures SHALL include scope definitions, auditor selection criteria, and result publication requirements.

All governance activities SHALL be documented and made available for public or regulatory inspection, as appropriate to the operating context.

### 6.4 Technical Extension Architecture

The Technical Extension Architecture defines optional implementation-level extension points that MAY be used to enhance registry functionality. Extensions SHALL operate outside the normative scope of this specification and SHALL NOT alter core document models, state transitions, or conformance logic.

Extensions MAY be used to support observability, non-canonical API functions, registry-specific workflows, and internal tooling. Implementations SHALL ensure that all extensions are isolated from core protocol logic and SHALL maintain compatibility with conformance rules.

#### 6.4.1 Plugin Interface

Registries MAY support a plugin interface for loading modular components such as internal jobs, visualization tools, or secondary data processors. Plugins SHALL operate in isolated environments and SHALL communicate only through defined interfaces. Resource constraints and execution boundaries SHALL be enforced.

#### 6.4.2 API Extension Layer

Implementations MAY expose additional API endpoints beyond those defined in the core specification. These endpoints SHALL be clearly documented and SHALL NOT conflict with canonical routes. Extensions MAY include authentication, rate limiting, and monitoring integration.

#### 6.4.3 Supplemental Data Schemas

Registries MAY extend internal database schemas to support additional metadata or analytic structures. Extended schemas SHALL maintain referential integrity with canonical identifiers and SHALL not affect lifecycle decisions or hashing logic. Schema extensions SHOULD follow migration and indexing procedures consistent with registry stability requirements.

#### 6.4.4 Observability Integration

Monitoring and alerting systems MAY be extended to support registry-specific metrics, dashboards, and threshold-based alerts. These extensions SHALL operate alongside core observability components and MAY support domain-specific visualizations, e.g., for methodology categories or verification throughput.

This extension architecture is intended to support operational flexibility and system-specific enhancements without compromising interoperability, auditability, or specification compliance.


## References

<a id="ref-1"></a>
[1] RFC 7946: The GeoJSON Format. https://tools.ietf.org/html/rfc7946  

<a id="ref-2"></a>
[2] JSON Schema Specification. https://json-schema.org/  

<a id="ref-3"></a>
[3] ERC-721: Non-Fungible Token Standard. https://eips.ethereum.org/EIPS/eip-721  

<a id="ref-4"></a>
[4] Regulation (EU) 2024/3012 establishing a Union certification framework for permanent carbon removals. https://eur-lex.europa.eu/eli/reg/2024/3012/oj
