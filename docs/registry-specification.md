# OGCR API Specification

**Version:** 0.1.0  
**Date:** July 2025   
**Authors:** OGCR Consortium  
**Status:** Draft  
**License:** CC-BY 4.0

## Abstract

The OGCR API Specification defines a registry framework for carbon removal certification based on open geospatial standards and verifiable ledger integration. It specifies canonical data formats, lifecycle states, API interfaces, and blockchain anchoring methods for managing project design, monitoring, verification, and issuance of removal attestations. The specification builds upon GeoJSON \[1], JSON Schema \[2], and ERC-721 \[3] to support traceable, interoperable, and auditable carbon removal systems consistent with the Carbon Removal Certification Framework (CRCF) and Regulation (EU) 2024/3012 \[4].

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

This specification is intended to support implementation of Article 9 and Annexes I–III of Regulation (EU) 2024/3012 \[4]. It addresses certification requirements for permanent carbon removals, carbon farming, and carbon storage in products. It specifies data fields and workflows necessary for compliance with monitoring, verification, additionality, permanence, and liability provisions. The architecture supports registry interoperability, auditability, and integration with national and international carbon accounting mechanisms.

## 2. System Architecture

### 2.1 Architectural Overview

A registry system conforming to this specification SHALL implement a three-layer architecture that separates interface logic, application state management, and verifiable state anchoring. Each layer SHALL be functionally distinct and interoperable with external systems and services.

![System Architecture](../diagrams/system-architecture-component.png)

*Figure 1: Reference system architecture defining application, API, and ledger layers.*

The **Application Layer** provides interfaces for human and machine actors. This includes web portals, mobile clients, and automated integrations. It SHALL support user interaction, identity delegation, and task coordination.

The **API Layer** exposes a RESTful interface for lifecycle operations on registry artifacts. It SHALL implement validation, access control, schema enforcement, and canonical serialization. It MAY coordinate with external services for verification or monitoring.

The **Blockchain Layer** maintains immutable references to registry state. It SHALL record document hashes, lifecycle events, and token-related actions. Ledger anchoring MUST be cryptographically verifiable and support independent audit.

### 2.2 Data Flow

A conforming implementation SHALL support structured data flows for project registration, monitoring, verification, and issuance. Each transition SHALL be deterministic, auditable, and linked to a canonical document reference.

**Project Registration** begins with the submission of a Project Design Document (PDD). The API layer SHALL validate schema conformance, methodology references, and geospatial footprint. Upon approval, a unique identifier SHALL be assigned and the document hash anchored on-chain.

**Monitoring and Verification** involves the submission of Monitoring, Reporting, and Verification (MRV) documents. These SHALL include quantified removals, methodology-specific inputs, and verifier attestations. Verified reports SHALL be linked to prior PDDs and recorded for audit and credit issuance.

**Credit Management** includes the creation, transfer, and retirement of carbon removal attestations. These SHALL be represented as cryptographically bound units (e.g., tokens), linked to verified removals and anchored for lifecycle traceability.

### 2.3 Integration Patterns

The specification defines standard integration patterns for registry federation, blockchain abstraction, and third-party system interoperability.

**Registry Federation** enables interoperability between multiple registry implementations. Federated systems SHALL prevent double counting, preserve provenance, and maintain cross-jurisdictional coherence.

**Blockchain Integration** SHALL support verifiable anchoring of document state and token issuance. The specification defines minimum on-chain data requirements, while allowing optimizations for gas efficiency, throughput, and chain-agnostic deployments.

**External System Integration** MAY include data providers, verifiers, or market actors. All integrations SHALL conform to standardized data schemas and authenticated communication protocols to ensure consistency and integrity.

## 3. Core Data Models

![Core Data Models](../diagrams/core-data-models-class.png)
*Figure 4: UML class diagram of canonical document types and their relationships.*

This specification defines three canonical document types used to represent project declarations, monitoring results, and verified removal units. All core documents SHALL be serialized as GeoJSON Features \[1] and SHALL follow schema constraints defined in the corresponding conformance classes.

### 3.1 Project Design Document (PDD)

The Project Design Document (PDD) defines the initial parameters of a carbon removal project. It SHALL contain project geometry, activity classification, actor identifiers, and methodological references. The PDD establishes the scope against which monitoring, verification, and issuance processes are evaluated.

Each PDD SHALL conform to the GeoJSON Feature model and SHALL include a valid `geometry` field representing the project boundary in WGS84 coordinates. The `properties` object SHALL contain required fields including project name, type, actor ID, and methodology reference.

PDDs SHALL reference approved methodologies that define quantification rules, monitoring requirements, and validation conditions. The PDD MAY include versioning metadata to track document evolution. Once validated, PDDs SHALL be immutable and anchored via cryptographic hash for audit purposes.

### 3.2 Monitoring, Reporting, and Verification (MRV)

The MRV document captures quantitative results from project monitoring and verification activities. Each MRV SHALL reference a single parent PDD and SHALL represent a defined monitoring period. Overlapping reporting periods for the same project SHALL be disallowed.

MRV documents SHALL include temporal coverage, methodology-specific inputs, calculated net removal values, and uncertainty estimates. Measurement types MAY include field observations, remote sensing outputs, or direct measurement instruments, subject to methodology compatibility.

Verification metadata SHALL be included for independently validated MRVs. This MAY contain verifier identity, accreditation ID, verification outcome, and date. Verified MRVs form the basis for issuance of removal attestations.

### 3.3 Carbon Removal Units (CRUs)

Carbon Removal Units (CRUs) represent attested net removals of CO₂ equivalent. Each CRU SHALL be linked to a validated MRV and a parent PDD, and SHALL correspond to a quantifiable and verifiable removal amount.

CRUs SHALL be uniquely identifiable and SHALL include metadata that binds them to the underlying monitoring and verification context. Implementations MAY use token-based representations such as ERC-721 for lifecycle tracking, transferability, and retirement.

CRUs MAY be issued in fractional quantities where permitted by the registry. Each unit SHALL retain a one-to-one mapping to its provenance data. Retired CRUs SHALL be excluded from transfer and SHALL be cryptographically flagged as withdrawn from circulation.

## References

[1] RFC 7946: The GeoJSON Format. https://tools.ietf.org/html/rfc7946  
[2] JSON Schema Specification. https://json-schema.org/  
[3] ERC-721: Non-Fungible Token Standard. https://eips.ethereum.org/EIPS/eip-721  
[4] Regulation (EU) 2024/3012 establishing a Union certification framework for permanent carbon removals. https://eur-lex.europa.eu/eli/reg/2024/3012/oj



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

The API implements comprehensive authentication and authorization mechanisms that ensure secure access while supporting various integration patterns. The system supports both human users and automated systems with appropriate security controls for each use case.

**OAuth 2.0 Integration** provides secure authentication for web applications and mobile clients. The system supports standard OAuth flows including authorization code, client credentials, and refresh token patterns. Token scopes control access to specific API endpoints and operations.

**API Key Authentication** enables secure access for automated systems and server-to-server integrations. API keys are associated with specific organizations and include rate limiting and access scope controls.

**Role-Based Access Control** ensures that users can only perform operations appropriate to their roles within the registry system. Roles include project developers, verifiers, registry operators, and credit holders with specific permissions for each role type.

Permission validation occurs at multiple levels including endpoint access, resource ownership, and operation authorization. The system maintains audit logs of all access attempts and permission decisions for security monitoring and compliance purposes.

### 4.4 Data Validation and Quality Assurance

The API implements comprehensive data validation mechanisms that ensure data quality while providing clear feedback for correction and improvement. Validation occurs at multiple levels from basic schema compliance to complex business rule enforcement.

**Schema Validation** ensures that all submitted data conforms to defined JSON schemas with appropriate field types, required fields, and format constraints. Schema validation provides immediate feedback on structural issues with specific field references and correction guidance.

The specification defines comprehensive JSON schemas for all core data types:
- **[PDD Schema](../schemas/pdd-schema.json)** - Validates Project Design Document structure and content
- **[MRV Schema](../schemas/mrv-schema.json)** - Validates Monitoring, Reporting, and Verification document structure and content

These schemas provide machine-readable validation rules that ensure data consistency across all registry implementations.

**Business Rule Validation** enforces complex constraints such as temporal consistency, spatial boundaries, and methodology compliance. Business rules are configurable to accommodate different regulatory requirements and methodology specifications.

**Data Quality Scoring** provides quantitative assessments of data completeness, accuracy, and consistency. Quality scores help users identify areas for improvement while enabling registry operators to prioritize review and verification activities.

Quality assurance processes include automated checks, manual review workflows, and continuous monitoring of data quality trends. The system provides dashboards and reports that enable stakeholders to track data quality improvements over time.

### 4.5 Performance and Scalability

The API design incorporates performance optimization and scalability features that ensure responsive operation under varying load conditions. These features enable the system to handle growing numbers of projects, monitoring reports, and credit transactions.

**Caching Strategies** reduce response times and server load by caching frequently accessed data at multiple levels. Cache invalidation ensures data consistency while maximizing performance benefits.

**Pagination and Filtering** enable efficient access to large datasets by limiting response sizes and providing targeted data access. Pagination supports both offset-based and cursor-based patterns for different use cases.

**Asynchronous Processing** handles time-intensive operations such as document validation, verification workflows, and blockchain transactions without blocking API responses. Status endpoints provide progress updates for long-running operations.

**Rate Limiting** protects system resources while ensuring fair access for all users. Rate limits are configurable by user type and endpoint category with clear error messages when limits are exceeded.

## 5. Smart Contract Requirements

### 5.1 Smart Contract Architecture

The Carbon Registry Specification defines smart contract requirements that provide immutable record-keeping, transparent governance, and trustless verification capabilities. The smart contract architecture separates concerns between different contract types while maintaining interoperability and upgradeability.

**Modular Design** organizes smart contract functionality into specialized contracts that handle specific aspects of registry operations. This approach enables independent upgrades, testing, and optimization while maintaining system coherence.

**Proxy Patterns** enable contract upgrades while preserving state and maintaining user trust. Upgrade mechanisms include time delays, multi-signature requirements, and governance voting to ensure that changes are legitimate and beneficial.

**Event-Driven Architecture** ensures that all significant contract actions emit events that can be monitored by off-chain systems. Events provide the basis for synchronization between blockchain and registry systems while enabling real-time monitoring and alerting.

### 5.2 Core Contract Types

The specification defines four primary smart contract types that handle different aspects of registry operations. Each contract type has specific responsibilities and interfaces that enable integration while maintaining security and efficiency.

#### 5.2.1 Project Registry Contract

The Project Registry Contract manages the registration and approval status of carbon removal projects. This contract provides immutable records of project submissions, approval decisions, and status changes while enabling authorized updates by registry operators.

**Project Registration** functions accept project document hashes and metadata from authorized submitters. Registration creates permanent records that link project identifiers to document hashes and submission timestamps.

**Approval Management** functions enable authorized validators to approve or reject submitted projects. Approval decisions are recorded with validator identities, timestamps, and supporting documentation references.

**Status Tracking** functions maintain current project status and enable authorized status changes. Status transitions are logged with complete audit trails including timestamps, responsible parties, and change reasons.

![Project Lifecycle States](../diagrams/lifecycle-states.png)

*Figure 5: Project Lifecycle States - State diagram showing the possible states and transitions for carbon removal projects throughout their lifecycle.*

Access control mechanisms ensure that only authorized parties can perform specific operations while maintaining transparency through public read access to project information.

#### 5.2.2 MRV Registry Contract

The MRV Registry Contract manages monitoring, reporting, and verification records for approved projects. This contract links monitoring reports to projects while tracking verification status and outcomes.

**Report Submission** functions accept monitoring report hashes and metadata from authorized submitters. Submissions are validated against project approval status and temporal requirements before creating permanent records.

**Verification Management** functions enable authorized verifiers to record verification outcomes and quantified carbon removal amounts. Verification records include verifier identities, verification dates, and outcome determinations.

**Data Integrity** functions provide cryptographic verification of monitoring report contents through hash comparison. These functions enable independent verification of report authenticity and completeness.

Temporal validation ensures that monitoring reports cover appropriate time periods without overlaps or gaps while maintaining consistency with project timelines and methodology requirements.

#### 5.2.3 Carbon Credit Token Contract

The Carbon Credit Token Contract implements carbon removal units as non-fungible tokens that provide unique identification, ownership tracking, and transfer capabilities. This contract follows ERC-721 standards while adding carbon-specific functionality.

**Token Minting** functions create new carbon credit tokens based on verified monitoring results. Minting is restricted to authorized registry operators and includes metadata linking tokens to underlying projects and monitoring periods.

**Transfer Management** functions handle token transfers between registry participants while maintaining ownership records and transfer histories. Transfer restrictions can be implemented for specific token types or regulatory requirements.

**Retirement Functions** enable permanent retirement of carbon credits for offsetting purposes. Retired tokens cannot be transferred or traded while maintaining traceability to underlying carbon removal activities.

Token metadata includes project identifiers, vintage years, verification details, and retirement status to provide complete traceability and transparency.

#### 5.2.4 Access Control Contract

The Access Control Contract manages roles, permissions, and authorization across the entire smart contract system. This contract provides centralized access control while enabling role delegation and permission management.

**Role Management** functions enable administrators to assign and revoke roles for different types of registry participants. Roles include project developers, verifiers, registry operators, and system administrators with specific permissions for each role type.

**Permission Validation** functions provide authorization checking for all contract operations. Permission validation ensures that only authorized parties can perform specific operations while maintaining audit trails of access attempts.

**Multi-Signature Support** enables critical operations to require approval from multiple authorized parties. Multi-signature requirements provide additional security for sensitive operations such as contract upgrades and role assignments.

Emergency functions enable rapid response to security issues or system problems while maintaining appropriate governance controls and audit trails.

### 5.3 Integration Requirements

Smart contracts must integrate seamlessly with off-chain registry systems while maintaining data consistency and security. Integration requirements define interfaces, data formats, and synchronization mechanisms that enable reliable operation.

**Event Monitoring** systems must monitor contract events in real-time to maintain synchronization between blockchain and registry systems. Event processing includes validation, error handling, and retry mechanisms to ensure reliable data synchronization.

**State Synchronization** mechanisms ensure that off-chain systems accurately reflect on-chain state while handling network issues, reorganizations, and other blockchain-specific challenges.

**Gas Optimization** strategies minimize transaction costs while maintaining functionality and security. Optimization includes batch operations, efficient data structures, and careful function design to reduce computational requirements.

**Network Compatibility** ensures that contracts can operate on multiple blockchain networks with appropriate modifications for network-specific features and limitations.

### 5.4 Security Requirements

Smart contract security is paramount given the immutable nature of blockchain systems and the value of carbon credits. Security requirements address common vulnerabilities while providing defense-in-depth protection.

**Access Control Validation** ensures that all functions properly validate caller permissions before executing operations. Access control includes role-based permissions, multi-signature requirements, and emergency controls.

**Input Validation** prevents malicious or malformed inputs from causing contract failures or security vulnerabilities. Validation includes parameter checking, overflow protection, and state consistency verification.

**Reentrancy Protection** prevents reentrancy attacks through appropriate function modifiers and state management. Protection mechanisms include checks-effects-interactions patterns and reentrancy guards.

**Upgrade Security** ensures that contract upgrades maintain security properties while enabling necessary improvements. Upgrade mechanisms include time delays, governance requirements, and migration procedures.

**Audit Requirements** mandate comprehensive security audits before contract deployment and after significant upgrades. Audit processes include automated testing, manual review, and formal verification where appropriate.

## 6. Extensibility Framework

### 6.1 Methodology Extension System

The Carbon Registry Specification provides a comprehensive framework for extending the system to support new carbon removal methodologies without requiring core system modifications. This extensibility ensures that the registry can adapt to emerging technologies and evolving scientific understanding while maintaining consistency and interoperability.

**Methodology Registration** enables the addition of new methodologies through a standardized process that includes methodology documentation, validation rules, and monitoring requirements. Registered methodologies receive unique identifiers and version numbers that enable precise referencing and evolution tracking.

**Schema Extension** allows methodologies to define additional data fields and validation rules that extend the core project and monitoring data models. Extensions are implemented through JSON Schema composition that maintains backward compatibility while enabling methodology-specific requirements.

**Validation Plugin Architecture** enables methodologies to implement custom validation logic that enforces methodology-specific requirements. Validation plugins operate within sandboxed environments that prevent interference with core system operations while enabling sophisticated validation capabilities.

**Calculation Engine Integration** provides interfaces for methodology-specific calculation engines that quantify carbon removal amounts based on monitoring data. Calculation engines operate as independent services that receive standardized inputs and produce standardized outputs with uncertainty estimates.

### 6.2 Integration Extension Points

The specification defines multiple extension points that enable integration with external systems, services, and data sources without modifying core registry functionality. These extension points provide flexibility while maintaining system security and data integrity.

**Data Source Connectors** enable integration with external monitoring systems, satellite data providers, and IoT sensor networks. Connectors implement standardized interfaces that handle authentication, data retrieval, and format conversion while maintaining data provenance and quality tracking.

**Verification Service Integration** allows the system to work with different verification bodies and automated verification systems. Integration includes credential verification, workflow management, and result recording while maintaining independence and avoiding conflicts of interest.

**Market Platform Integration** enables connectivity with carbon credit trading platforms, offset marketplaces, and registry federation systems. Integration maintains credit authenticity and prevents double-counting while enabling market liquidity and price discovery.

**Regulatory Reporting Integration** provides interfaces for automated reporting to regulatory bodies and compliance systems. Reporting integration includes data formatting, submission scheduling, and confirmation tracking while maintaining data privacy and security.

### 6.3 Governance Extension Framework

The specification includes governance mechanisms that enable stakeholder participation in system evolution while maintaining stability and security. Governance extensions provide transparency and accountability in decision-making processes.

**Proposal System** enables stakeholders to propose system improvements, methodology additions, and policy changes through structured processes. Proposals include impact assessments, implementation plans, and stakeholder consultation requirements.

**Voting Mechanisms** provide transparent decision-making processes for governance proposals with appropriate weighting for different stakeholder types. Voting systems include quorum requirements, time limits, and result implementation procedures.

**Advisory Committee Integration** enables the formation of technical and policy advisory committees that provide expertise and guidance for system development. Committee integration includes member selection, meeting management, and recommendation tracking.

**Audit and Compliance Framework** provides mechanisms for independent auditing of system operations, methodology implementations, and governance decisions. Audit frameworks include scope definition, auditor selection, and result publication requirements.

### 6.4 Technical Extension Architecture

The technical architecture provides multiple layers of extensibility that enable customization and enhancement without compromising system integrity or performance. Technical extensions operate within defined boundaries that maintain security and compatibility.

**Plugin Architecture** enables the addition of new functionality through standardized plugin interfaces. Plugins operate in isolated environments with defined resource limits and communication channels that prevent interference with core operations.

**API Extension Framework** allows the addition of new API endpoints and functionality while maintaining consistency with existing interfaces. API extensions include authentication integration, rate limiting, and documentation requirements.

**Database Extension Schema** provides mechanisms for adding new data types and relationships while maintaining referential integrity and performance. Schema extensions include migration procedures, indexing requirements, and backup considerations.

**Monitoring and Alerting Extensions** enable the addition of custom monitoring metrics, alerting rules, and dashboard components. Monitoring extensions integrate with existing observability infrastructure while providing methodology-specific insights and alerts.

The extensibility framework ensures that the Carbon Registry Specification can evolve to meet changing requirements while maintaining the core principles of minimalism, transparency, and interoperability that define the system architecture.

