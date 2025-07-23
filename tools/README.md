# OGCR API Validation Tools

Comprehensive validation tools for OGCR API documents and implementations.

## Features

- JSON Schema validation for PDD and MRV documents
- OGCR-specific compliance checking
- API endpoint validation
- Compliance report generation
- Command-line interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Validate a Document File

```bash
python spec_checker.py --file document.json
```

### Validate API Endpoints

```bash
python spec_checker.py --api http://localhost:8000
```

### Generate Compliance Report

```bash
python spec_checker.py --file document.json --report compliance_report.txt
```

### Validate Specific API Endpoint

```bash
python spec_checker.py --api http://localhost:8000 --endpoint /projects
```

## Validation Features

### JSON Schema Validation
- Validates against PDD and MRV JSON schemas
- Checks required fields and data types
- Validates field constraints and patterns

### OGCR-Specific Validation
- GeoJSON compliance checking
- OGCR version format validation
- Link structure and URL validation
- Date format and range validation
- Methodology reference validation
- Carbon unit validation
- Uncertainty range validation

### API Validation
- HTTP response status checking
- JSON response format validation
- Document structure validation
- Pagination structure validation

## Example Documents

### Valid PDD Document

```json
{
  "type": "Feature",
  "id": "project_001",
  "ogcr_version": "0.1.0",
  "profile": "pdd",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
  },
  "properties": {
    "name": "Test Forest Project",
    "project_type": "afforestation",
    "status": "draft",
    "creation_date": "2024-12-07T10:00:00Z",
    "actor_id": "test-developer"
  }
}
```

### Valid MRV Document

```json
{
  "type": "Feature",
  "id": "mrv_001",
  "ogcr_version": "0.1.0",
  "profile": "mrv",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
  },
  "properties": {
    "project_id": "project_001",
    "methodology_id": "methodology_001",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "methodology_data": {
      "parameters": {},
      "measurement_devices": [],
      "sampling_strategy": "Random sampling"
    },
    "net_removal_estimate": {
      "value": 1000.0,
      "unit": "tCO2e",
      "basis": "Field measurements"
    }
  }
}
```

## Command Line Options

- `--file, -f`: Validate a JSON file
- `--api, -a`: Validate API endpoint (base URL)
- `--endpoint, -e`: Specific endpoint to test
- `--schema-dir, -s`: Directory containing JSON schemas
- `--report, -r`: Generate compliance report to file
- `--verbose, -v`: Verbose output

## Exit Codes

- `0`: All validations passed
- `1`: One or more validations failed

## Integration

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Validate OGCR Documents
  run: |
    python validation-tools/spec_checker.py --file examples/pdd.json
    python validation-tools/spec_checker.py --file examples/mrv.json
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python validation-tools/spec_checker.py --file documents/*.json
```

## License

MIT License - see LICENSE-SOFTWARE file for details.

Copyright (c) 2025 OGCR Consortium

