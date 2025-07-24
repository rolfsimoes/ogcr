# OGCR API Specification

**Version:** 0.1.0  
**Developed by:** OGCR Consortium  
**License:** CC-BY 4.0 (Specification), MIT (Software)

## Overview

The Open Geospatial Carbon Registry (OGCR) API Specification defines a normative framework for carbon removal certification systems, aligned with the principles of the Carbon Removal Certification Framework (CRCF). It establishes open standards for data models, lifecycle control, and verifiable state transitions, enabling transparent governance, interoperability, and auditability across distributed registry infrastructures.

## Repository Structure

```
ogcr-api-repo/
├── docs/                           # Core specification documents
│   ├── registry-specification.md   # Main OGCR API specification
│   ├── api-documentation.md        # Complete RESTful API reference
│   ├── smart-contract-requirements.md # Blockchain requirements
│   └── implementation-guidelines.md # Implementation guide
├── schemas/                        # JSON schemas
│   ├── pdd-schema.json            # Project Design Document schema
│   └── mrv-schema.json            # MRV Document schema
├── diagrams/                       # UML diagrams
│   ├── *.puml                     # PlantUML source files
│   └── *.png                      # Rendered diagrams
├── examples/                       # Example documents
│   ├── valid_pdd.json             # Valid PDD example
│   ├── valid_mrv.json             # Valid MRV example
│   └── invalid_pdd.json           # Invalid example for testing
├── server/                         # FastAPI mockup server
│   ├── app/                       # Application code
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile                 # Docker configuration
│   └── README.md                  # Server documentation
├── tools/                          # Validation and utility tools
│   ├── spec_checker.py            # Specification validator
│   ├── requirements.txt           # Tool dependencies
│   └── README.md                  # Tools documentation
├── tests/                          # Test suites
│   ├── test_api.py                # API server tests
│   ├── test_spec_checker.py       # Validation tool tests
│   └── requirements.txt           # Test dependencies
├── run_tests.py                    # Comprehensive test runner
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE-SPEC                    # CC-BY 4.0 license for specification
└── LICENSE-SOFTWARE               # MIT license for software
```

## Quick Start

### 1. API Server

Start the FastAPI mockup server:

```bash
cd server
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access API documentation at: http://localhost:8000/docs

### 2. Validation Tools

Validate OGCR documents:

```bash
cd tools
pip install -r requirements.txt

# Validate a document
python spec_checker.py --file ../examples/valid_pdd.json

# Validate API endpoints
python spec_checker.py --api http://localhost:8000
```

### 3. Run All Tests

Execute the complete test suite:

```bash
python run_tests.py
```

## Documentation

### Core Specification
- **[Registry Specification](docs/registry-specification.md)** - Main OGCR API specification
- **[API Documentation](docs/api-documentation.md)** - Complete RESTful API reference
- **[Smart Contract Requirements](docs/smart-contract-requirements.md)** - Detailed blockchain requirements
- **[Implementation Guidelines](docs/implementation-guidelines.md)** - Step-by-step implementation guide

### Technical Assets
- **[JSON Schemas](schemas/)** - Data validation schemas for PDD and MRV documents
- **[UML Diagrams](diagrams/)** - Visual representations of system architecture and workflows
- **[Examples](examples/)** - Sample documents for testing and reference

### Software Components
- **[API Server](server/)** - FastAPI implementation with full endpoint coverage
- **[Validation Tools](tools/)** - Comprehensive document and API validation utilities
- **[Test Suite](tests/)** - Complete testing framework with 49+ tests

## Key Features

- **Professional Framework** - Consistent and well-documented specification  
- **Minimal Requirements** - Streamlined information requirements  
- **Intuitive API** - RESTful design with clear endpoints  
- **Smart Contract Ready** - Detailed blockchain requirements (no implementation)  
- **Extensible Design** - Flexible methodology framework  
- **Complete Testing** - Comprehensive validation and test coverage  
- **Production Ready** - Docker support and deployment guides  

## Example Usage

### Create a Project via API

```bash
curl -X POST "http://localhost:8000/projects" \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d @examples/valid_pdd.json
```

### Validate a Document

```bash
cd tools
python spec_checker.py --file ../examples/valid_pdd.json --verbose
```

### Generate Compliance Report

```bash
cd tools
python spec_checker.py --file ../examples/valid_pdd.json --report compliance_report.txt
```

## Development

### Prerequisites
- Python 3.11+
- pip package manager

### Installation
1. Clone or extract the repository
2. Install dependencies for each component
3. Run tests to verify installation

### Testing
- **API Server:** `cd server && python -m pytest ../tests/test_api.py -v`
- **Validation Tools:** `cd tools && python -m pytest ../tests/test_spec_checker.py -v`
- **All Tests:** `python run_tests.py`

## Deployment

### API Server
- **Docker:** Use provided Dockerfile in `server/`
- **Cloud:** Deploy to any platform supporting Python/FastAPI
- **Local:** Run with uvicorn for development

### Validation Tools
- **CI/CD:** Integrate spec checker into build pipelines
- **Pre-commit:** Use as git pre-commit hook
- **Standalone:** Run as command-line tool

## Compliance

The specification aligns with:
- EU 2024/3012 carbon removal certification framework
- UNFCCC Paris Agreement requirements
- GDPR and data protection regulations
- International carbon accounting standards

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project uses dual licensing:

- **Specification Documents:** Licensed under [CC-BY 4.0](LICENSE-SPEC)
  - Includes specification documents, schemas, and documentation
- **Software Components:** Licensed under [MIT License](LICENSE-SOFTWARE)
  - Includes API implementations, validation tools, and test suites

## Citation

If you use this specification in your research or implementation, please cite:

```
OGCR API Specification v0.1.0
OGCR Consortium, 2025
https://github.com/ogcr-consortium/ogcr-api-specification
```

## Support

- **Documentation:** See component README files in respective directories
- **Issues:** Report via GitHub Issues

---

**OGCR Consortium** - Advancing carbon removal through open standards and transparent governance.

>*This work is funded by the European Commission (EC) through the project "Intergenerational Open Geospatial Carbon Registry - Open-Source Tools for Connecting EU Agricultural Policies (CAP) and Carbon Removals and Carbon Farming (CRCF) Regulation to national inventories and carbon markets" (1 Jun. 2025 – 31 May 2029 - 101218854)*
