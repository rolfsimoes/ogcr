"""
Tests for OGCR API Specification Checker

License: MIT
Copyright (c) 2025 OGCR Consortium
"""

import pytest
import json
import tempfile
import os
import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from spec_checker import OGCRSpecChecker

class TestOGCRSpecChecker:
    """Test the OGCR specification checker"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.checker = OGCRSpecChecker()
        
        # Valid PDD document
        self.valid_pdd = {
            "type": "Feature",
            "id": "test_project",
            "ogcr_version": "0.1.0",
            "profile": "pdd",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            "properties": {
                "name": "Test Project",
                "creation_date": "2024-12-07T10:00:00Z",
                "project_type": "afforestation",
                "status": "draft",
                "actor_id": "test-actor"
            }
        }
        
        # Valid MRV document
        self.valid_mrv = {
            "type": "Feature",
            "id": "test_mrv",
            "ogcr_version": "0.1.0",
            "profile": "mrv",
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0]
            },
            "properties": {
                "project_id": "test_project",
                "methodology_id": "test_methodology",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "methodology_data": {
                    "parameters": {},
                    "measurement_devices": [],
                    "sampling_strategy": "Random"
                },
                "net_removal_estimate": {
                    "value": 1000.0,
                    "unit": "tCO2e"
                }
            }
        }

class TestDocumentValidation(TestOGCRSpecChecker):
    """Test document validation functionality"""
    
    def test_valid_pdd_document(self):
        """Test validation of valid PDD document"""
        valid, errors = self.checker.validate_document(self.valid_pdd, "pdd")
        assert valid, f"Validation failed with errors: {errors}"
        assert len(errors) == 0
    
    def test_valid_mrv_document(self):
        """Test validation of valid MRV document"""
        valid, errors = self.checker.validate_document(self.valid_mrv, "mrv")
        assert valid, f"Validation failed with errors: {errors}"
        assert len(errors) == 0
    
    def test_auto_detect_pdd_type(self):
        """Test auto-detection of PDD document type"""
        valid, errors = self.checker.validate_document(self.valid_pdd)
        assert valid
    
    def test_auto_detect_mrv_type(self):
        """Test auto-detection of MRV document type"""
        valid, errors = self.checker.validate_document(self.valid_mrv)
        assert valid
    
    def test_invalid_document_type(self):
        """Test handling of invalid document type"""
        invalid_doc = self.valid_pdd.copy()
        invalid_doc["type"] = "InvalidType"
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("Document must be a GeoJSON Feature" in error for error in errors)
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields"""
        invalid_doc = self.valid_pdd.copy()
        del invalid_doc["geometry"]
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("Missing required geometry field" in error for error in errors)
    
    def test_invalid_geometry_type(self):
        """Test validation with invalid geometry type"""
        invalid_doc = self.valid_pdd.copy()
        invalid_doc["geometry"]["type"] = "InvalidGeometry"
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("Invalid geometry type" in error for error in errors)
    
    def test_invalid_ogcr_version(self):
        """Test validation with invalid OGCR version"""
        invalid_doc = self.valid_pdd.copy()
        invalid_doc["ogcr_version"] = "invalid-version"
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("Invalid ogcr_version format" in error for error in errors)

class TestPDDSpecificValidation(TestOGCRSpecChecker):
    """Test PDD-specific validation rules"""
    
    def test_invalid_creation_date(self):
        """Test validation with invalid creation date"""
        invalid_doc = self.valid_pdd.copy()
        invalid_doc["properties"]["creation_date"] = "invalid-date"
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("Invalid creation_date format" in error for error in errors)
    
    def test_negative_expected_benefit(self):
        """Test validation with negative expected benefit"""
        invalid_doc = self.valid_pdd.copy()
        invalid_doc["properties"]["expected_annual_benefit"] = -100
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("expected_annual_benefit must be non-negative" in error for error in errors)
    
    def test_invalid_methodology_version(self):
        """Test validation with invalid methodology version"""
        invalid_doc = self.valid_pdd.copy()
        invalid_doc["properties"]["methodology"] = {
            "id": "test",
            "version": "invalid-version"
        }
        
        valid, errors = self.checker.validate_document(invalid_doc, "pdd")
        assert not valid
        assert any("Invalid methodology version format" in error for error in errors)

class TestMRVSpecificValidation(TestOGCRSpecChecker):
    """Test MRV-specific validation rules"""
    
    def test_invalid_date_range(self):
        """Test validation with invalid date range"""
        invalid_doc = self.valid_mrv.copy()
        invalid_doc["properties"]["start_date"] = "2024-12-31"
        invalid_doc["properties"]["end_date"] = "2024-01-01"
        
        valid, errors = self.checker.validate_document(invalid_doc, "mrv")
        assert not valid
        assert any("start_date must be before end_date" in error for error in errors)
    
    def test_negative_removal_estimate(self):
        """Test validation with negative removal estimate"""
        invalid_doc = self.valid_mrv.copy()
        invalid_doc["properties"]["net_removal_estimate"]["value"] = -100
        
        valid, errors = self.checker.validate_document(invalid_doc, "mrv")
        assert not valid
        assert any("net_removal_estimate value must be non-negative" in error for error in errors)
    
    def test_invalid_carbon_unit(self):
        """Test validation with invalid carbon unit"""
        invalid_doc = self.valid_mrv.copy()
        invalid_doc["properties"]["net_removal_estimate"]["unit"] = "invalid_unit"
        
        valid, errors = self.checker.validate_document(invalid_doc, "mrv")
        assert not valid
        assert any("Invalid unit" in error for error in errors)
    
    def test_invalid_uncertainty_range(self):
        """Test validation with invalid uncertainty range"""
        invalid_doc = self.valid_mrv.copy()
        invalid_doc["properties"]["total_uncertainty"] = {
            "min": 1000,
            "max": 500,
            "confidence_level": 0.95
        }
        
        valid, errors = self.checker.validate_document(invalid_doc, "mrv")
        assert not valid
        assert any("uncertainty min must be <= max" in error for error in errors)
    
    def test_invalid_confidence_level(self):
        """Test validation with invalid confidence level"""
        invalid_doc = self.valid_mrv.copy()
        invalid_doc["properties"]["total_uncertainty"] = {
            "min": 500,
            "max": 1000,
            "confidence_level": 1.5
        }
        
        valid, errors = self.checker.validate_document(invalid_doc, "mrv")
        assert not valid
        assert any("confidence_level must be between 0 and 1" in error for error in errors)

class TestLinksValidation(TestOGCRSpecChecker):
    """Test links validation"""
    
    def test_valid_links(self):
        """Test validation with valid links"""
        doc_with_links = self.valid_pdd.copy()
        doc_with_links["links"] = [
            {
                "rel": "methodology",
                "href": "https://example.com/methodology",
                "type": "text/html",
                "title": "Methodology Document"
            }
        ]
        
        valid, errors = self.checker.validate_document(doc_with_links, "pdd")
        assert valid
    
    def test_invalid_link_url(self):
        """Test validation with invalid link URL"""
        doc_with_links = self.valid_pdd.copy()
        doc_with_links["links"] = [
            {
                "rel": "methodology",
                "href": "not-a-url"
            }
        ]
        
        valid, errors = self.checker.validate_document(doc_with_links, "pdd")
        assert not valid
        assert any("href is not a valid URL" in error for error in errors)
    
    def test_missing_link_fields(self):
        """Test validation with missing link fields"""
        doc_with_links = self.valid_pdd.copy()
        doc_with_links["links"] = [
            {
                "href": "https://example.com"
                # Missing 'rel' field
            }
        ]

        valid, errors = self.checker.validate_document(doc_with_links, "pdd")
        assert not valid
        assert any("missing required 'rel' field" in error for error in errors)

    def test_links_field_not_array(self):
        """Links field must be an array of link objects"""
        doc_with_links = self.valid_pdd.copy()
        # Provide a single link object instead of an array
        doc_with_links["links"] = {
            "rel": "self",
            "href": "https://example.com"
        }

        valid, errors = self.checker.validate_document(doc_with_links, "pdd")
        assert not valid
        # Schema should complain about type mismatch, and our validator should
        # add a clear error without emitting per-character object errors.
        assert any("is not of type 'array'" in error for error in errors)
        assert any("links must be an array" in error for error in errors)
        assert not any("Link 0 must be an object" in error for error in errors)

class TestBboxValidation(TestOGCRSpecChecker):
    """Test bbox validation"""
    
    def test_valid_bbox(self):
        """Test validation with valid bbox"""
        doc_with_bbox = self.valid_pdd.copy()
        doc_with_bbox["bbox"] = [0, 0, 1, 1]
        
        valid, errors = self.checker.validate_document(doc_with_bbox, "pdd")
        assert valid
    
    def test_invalid_bbox_length(self):
        """Test validation with invalid bbox length"""
        doc_with_bbox = self.valid_pdd.copy()
        doc_with_bbox["bbox"] = [0, 0, 1]  # Should be 4 elements
        
        valid, errors = self.checker.validate_document(doc_with_bbox, "pdd")
        assert not valid
        assert any("bbox must be an array of 4 numbers" in error for error in errors)
    
    def test_invalid_bbox_values(self):
        """Test validation with invalid bbox values"""
        doc_with_bbox = self.valid_pdd.copy()
        doc_with_bbox["bbox"] = [0, 0, "invalid", 1]
        
        valid, errors = self.checker.validate_document(doc_with_bbox, "pdd")
        assert not valid
        assert any("bbox values must be numbers" in error for error in errors)

class TestFileValidation(TestOGCRSpecChecker):
    """Test file validation functionality"""
    
    def test_validate_valid_file(self):
        """Test validation of valid JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_pdd, f)
            temp_file = f.name
        
        try:
            valid, errors = self.checker.validate_file(temp_file)
            assert valid
            assert len(errors) == 0
        finally:
            os.unlink(temp_file)
    
    def test_validate_invalid_json_file(self):
        """Test validation of invalid JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name
        
        try:
            valid, errors = self.checker.validate_file(temp_file)
            assert not valid
            assert any("Invalid JSON" in error for error in errors)
        finally:
            os.unlink(temp_file)
    
    def test_validate_nonexistent_file(self):
        """Test validation of non-existent file"""
        valid, errors = self.checker.validate_file("nonexistent.json")
        assert not valid
        assert any("File not found" in error for error in errors)

class TestComplianceReport(TestOGCRSpecChecker):
    """Test compliance report generation"""
    
    def test_generate_compliance_report(self):
        """Test compliance report generation"""
        results = [
            {
                "name": "Test 1",
                "valid": True,
                "errors": []
            },
            {
                "name": "Test 2",
                "valid": False,
                "errors": ["Error 1", "Error 2"]
            }
        ]
        
        report = self.checker.generate_compliance_report(results)
        
        assert "OGCR API Specification Compliance Report" in report
        assert "Summary: 1/2 tests passed" in report
        assert "[PASS] Test 1" in report
        assert "[FAIL] Test 2" in report
        assert "Error 1" in report
        assert "Error 2" in report

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

