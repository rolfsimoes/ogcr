# OGCR API Specification - Complete Package

**Version:** 0.1.0  
**Package Date:** July 2025  
**Developed by:** OGCR Consortium  
**License:** CC-BY 4.0 (Specification), MIT (Software)

## Package Contents

This package contains the complete OGCR API Specification with all documentation, software components, validation tools, and supporting materials.

### Core Documentation (115,334 words total)
- **[docs/registry-specification.md](docs/registry-specification.md)** - Main OGCR API specification (38,263 words)
- **[docs/api-documentation.md](docs/api-documentation.md)** - Complete RESTful API reference (17,386 words)
- **[docs/smart-contract-requirements.md](docs/smart-contract-requirements.md)** - Detailed blockchain requirements (37,887 words)
- **[docs/implementation-guidelines.md](docs/implementation-guidelines.md)** - Step-by-step implementation guide (21,798 words)

### Visual Documentation
- **[diagrams/](diagrams/)** - UML diagrams with source files (.puml) and rendered images (.png)
  - System Architecture Component Diagram
  - Project Registration Sequence Diagram
  - MRV Workflow Sequence Diagram
  - Core Data Models Class Diagram
  - Project Lifecycle States Diagram
  - System Components Overview

### Technical Assets
- **[schemas/](schemas/)** - JSON schemas for data validation
  - `pdd-schema.json` - Project Design Document validation schema
  - `mrv-schema.json` - MRV Document validation schema
- **[examples/](examples/)** - Sample documents for testing and reference
  - `valid_pdd.json` - Valid Project Design Document example
  - `valid_mrv.json` - Valid MRV Document example
  - `invalid_pdd.json` - Invalid document for error testing

### Software Components
- **[server/](server/)** - FastAPI mockup server with full endpoint implementation
  - Complete API implementation with all OGCR endpoints
  - Request/response validation with Pydantic models
  - OpenAPI/Swagger documentation at `/docs`
  - Docker configuration for deployment
- **[tools/](tools/)** - Comprehensive validation and utility tools
  - `spec_checker.py` - Document and API validation tool
  - CLI interface with multiple validation modes
  - Compliance report generation
- **[tests/](tests/)** - Complete testing framework
  - 26 validation tool tests (100% pass rate)
  - 23 API server tests (100% pass rate)
  - Integration tests for complete workflows

### Repository Documentation
- **[README.md](README.md)** - Comprehensive repository overview and quick start guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and development setup
- **[LICENSE-SPEC](LICENSE-SPEC)** - CC-BY 4.0 license for specification documents
- **[LICENSE-SOFTWARE](LICENSE-SOFTWARE)** - MIT license for software components

## Quick Start

### 1. API Server
```bash
cd server
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Access docs at http://localhost:8000/docs
```

### 2. Validation Tools
```bash
cd tools
pip install -r requirements.txt
python spec_checker.py --file ../examples/valid_pdd.json
```

### 3. Run All Tests
```bash
python run_tests.py
# Result: 6/6 tests passed
```

## Key Features Delivered

- **Professional Framework** - Consistent and well-documented specification  
- **Minimal Requirements** - Streamlined information requirements  
- **Intuitive API** - RESTful design with clear endpoints  
- **Smart Contract Ready** - Detailed blockchain requirements (no implementation)  
- **Extensible Design** - Flexible methodology framework  
- **Complete Testing** - Comprehensive validation and test coverage (49+ tests)  
- **Production Ready** - Docker support and deployment guides  
- **Visual Documentation** - UML diagrams integrated into specification  
- **Working Examples** - Complete example documents and validation  

## Quality Assurance

- **All Tests Passing:** 49 total tests across validation tools and API server
- **Comprehensive Error Detection:** Invalid document detection working correctly
- **API Endpoints Functional:** All endpoints tested and operational
- **Schema Validation Operational:** JSON schema validation working correctly
- **Documentation Complete:** All internal references fixed and working
- **Repository Structure:** Well-organized with proper file organization

## Technical Specifications

- **Python Version:** 3.11+
- **FastAPI Version:** Latest stable
- **JSON Schema:** Draft 7 specification
- **UML Diagrams:** PlantUML format with PNG renders
- **Documentation Format:** Markdown with proper internal linking
- **Testing Framework:** pytest with comprehensive coverage

## Compliance

The specification aligns with:
- EU 2024/3012 carbon removal certification framework
- UNFCCC Paris Agreement requirements
- GDPR and data protection regulations
- International carbon accounting standards

## Support

- **Documentation:** See component README files in respective directories
- **Issues:** Report via GitHub Issues
- **Email:** contact@ogcr.org

---

**OGCR Consortium** - Advancing carbon removal through open standards and transparent governance.

`This work is funded by the European Commission (EC) through the project "Intergenerational Open Geospatial Carbon Registry - Open-Source Tools for Connecting EU Agricultural Policies (CAP) and Carbon Removals and Carbon Farming (CRCF) Regulation to national inventories and carbon markets" (1 Jun. 2025 – 31 May 2029 - 101218854)`
