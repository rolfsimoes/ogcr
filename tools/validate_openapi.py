#!/usr/bin/env python3
"""
OGCR OpenAPI Specification Validator

License: MIT
Copyright (c) 2025 OGCR Consortium
"""

from pathlib import Path
import yaml
from openapi_spec_validator import validate_spec


def main() -> None:
    """Validate the OpenAPI specification file."""
    spec_path = Path(__file__).resolve().parents[1] / "docs" / "openapi.yaml"
    with spec_path.open("r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    validate_spec(spec)
    print("OpenAPI specification is valid.")


if __name__ == "__main__":
    main()
