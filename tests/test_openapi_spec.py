"""Tests for OGCR OpenAPI specification"""

from pathlib import Path
import yaml
from openapi_spec_validator import validate_spec


def test_openapi_spec_valid() -> None:
    spec_path = Path(__file__).resolve().parents[1] / "docs" / "openapi.yaml"
    with spec_path.open("r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    validate_spec(spec)
