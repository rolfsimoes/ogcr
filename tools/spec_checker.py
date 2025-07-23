#!/usr/bin/env python3
"""
OGCR API Specification Checker

A comprehensive validation tool for OGCR API documents and implementations.

License: MIT
Copyright (c) 2025 OGCR Consortium
"""

import json
import jsonschema
import argparse
import sys
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime
import re
import requests
from urllib.parse import urlparse

class OGCRSpecChecker:
    """Comprehensive OGCR API specification checker"""
    
    def __init__(self, schema_dir: str = None):
        """Initialize the spec checker with schema directory"""
        if schema_dir is None:
            # Default to schemas directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_dir = os.path.join(os.path.dirname(current_dir), "schemas")
        
        self.schema_dir = schema_dir
        self.schemas = {}
        self.load_schemas()
        
    def load_schemas(self):
        """Load JSON schemas from the schema directory"""
        try:
            # Load PDD schema
            pdd_schema_path = os.path.join(self.schema_dir, "pdd-schema.json")
            if os.path.exists(pdd_schema_path):
                with open(pdd_schema_path, 'r') as f:
                    self.schemas['pdd'] = json.load(f)
            
            # Load MRV schema
            mrv_schema_path = os.path.join(self.schema_dir, "mrv-schema.json")
            if os.path.exists(mrv_schema_path):
                with open(mrv_schema_path, 'r') as f:
                    self.schemas['mrv'] = json.load(f)
                    
            print(f"Loaded {len(self.schemas)} schemas from {self.schema_dir}")
            
        except Exception as e:
            print(f"Error loading schemas: {e}")
            
    def validate_document(self, document: Dict[str, Any], doc_type: str = None) -> Tuple[bool, List[str]]:
        """
        Validate a document against the appropriate schema
        
        Args:
            document: The document to validate
            doc_type: Document type ('pdd' or 'mrv'), auto-detected if None
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Auto-detect document type if not provided
        if doc_type is None:
            doc_type = self._detect_document_type(document)
            
        if doc_type not in self.schemas:
            errors.append(f"Unknown document type: {doc_type}")
            return False, errors
            
        # Validate against JSON schema
        try:
            jsonschema.validate(document, self.schemas[doc_type])
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
            if e.path:
                errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
            
        # Additional OGCR-specific validations
        additional_errors = self._validate_ogcr_requirements(document, doc_type)
        errors.extend(additional_errors)
        
        return len(errors) == 0, errors
        
    def _detect_document_type(self, document: Dict[str, Any]) -> str:
        """Auto-detect document type from profile field"""
        profile = document.get('profile', '')
        if profile == 'pdd':
            return 'pdd'
        elif profile == 'mrv':
            return 'mrv'
        else:
            # Fallback detection based on properties
            properties = document.get('properties', {})
            if 'project_type' in properties:
                return 'pdd'
            elif 'methodology_data' in properties:
                return 'mrv'
            else:
                return 'unknown'
                
    def _validate_ogcr_requirements(self, document: Dict[str, Any], doc_type: str) -> List[str]:
        """Validate OGCR-specific requirements beyond JSON schema"""
        errors = []
        
        # Common validations for all documents
        errors.extend(self._validate_geojson_compliance(document))
        errors.extend(self._validate_ogcr_version(document))
        errors.extend(self._validate_links(document))
        
        # Document-specific validations
        if doc_type == 'pdd':
            errors.extend(self._validate_pdd_specific(document))
        elif doc_type == 'mrv':
            errors.extend(self._validate_mrv_specific(document))
            
        return errors
        
    def _validate_geojson_compliance(self, document: Dict[str, Any]) -> List[str]:
        """Validate GeoJSON compliance"""
        errors = []
        
        # Check required GeoJSON fields
        if document.get('type') != 'Feature':
            errors.append("Document must be a GeoJSON Feature")
            
        # Validate geometry
        geometry = document.get('geometry')
        if not geometry:
            errors.append("Missing required geometry field")
        else:
            if 'type' not in geometry or 'coordinates' not in geometry:
                errors.append("Invalid geometry structure")
            else:
                geom_type = geometry.get('type')
                valid_types = ['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon']
                if geom_type not in valid_types:
                    errors.append(f"Invalid geometry type: {geom_type}")
                    
        # Validate bbox if present
        bbox = document.get('bbox')
        if bbox is not None:
            if not isinstance(bbox, list) or len(bbox) != 4:
                errors.append("bbox must be an array of 4 numbers")
            elif not all(isinstance(x, (int, float)) for x in bbox):
                errors.append("bbox values must be numbers")
                
        return errors
        
    def _validate_ogcr_version(self, document: Dict[str, Any]) -> List[str]:
        """Validate OGCR version format"""
        errors = []
        
        version = document.get('ogcr_version')
        if not version:
            errors.append("Missing ogcr_version field")
        else:
            # Check semantic version format
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                errors.append(f"Invalid ogcr_version format: {version} (must be semantic version)")
                
        return errors
        
    def _validate_links(self, document: Dict[str, Any]) -> List[str]:
        """Validate links array"""
        errors = []
        
        links = document.get('links', [])
        if links:
            for i, link in enumerate(links):
                if not isinstance(link, dict):
                    errors.append(f"Link {i} must be an object")
                    continue
                    
                # Check required fields
                if 'rel' not in link:
                    errors.append(f"Link {i} missing required 'rel' field")
                if 'href' not in link:
                    errors.append(f"Link {i} missing required 'href' field")
                    
                # Validate href is a valid URL
                href = link.get('href')
                if href:
                    try:
                        result = urlparse(href)
                        if not all([result.scheme, result.netloc]):
                            errors.append(f"Link {i} href is not a valid URL: {href}")
                    except Exception:
                        errors.append(f"Link {i} href is not a valid URL: {href}")
                        
        return errors
        
    def _validate_pdd_specific(self, document: Dict[str, Any]) -> List[str]:
        """Validate PDD-specific requirements"""
        errors = []
        
        properties = document.get('properties', {})
        
        # Validate creation_date format
        creation_date = properties.get('creation_date')
        if creation_date:
            try:
                datetime.fromisoformat(creation_date.replace('Z', '+00:00'))
            except ValueError:
                errors.append(f"Invalid creation_date format: {creation_date}")
                
        # Validate methodology reference
        methodology = properties.get('methodology')
        if methodology:
            if not isinstance(methodology, dict):
                errors.append("Methodology must be an object")
            else:
                if 'id' not in methodology:
                    errors.append("Methodology missing required 'id' field")
                if 'version' not in methodology:
                    errors.append("Methodology missing required 'version' field")
                    
                version = methodology.get('version')
                if version and not re.match(r'^\d+\.\d+(\.\d+)?$', version):
                    errors.append(f"Invalid methodology version format: {version}")
                    
        # Validate expected_annual_benefit
        benefit = properties.get('expected_annual_benefit')
        if benefit is not None and benefit < 0:
            errors.append("expected_annual_benefit must be non-negative")
            
        return errors
        
    def _validate_mrv_specific(self, document: Dict[str, Any]) -> List[str]:
        """Validate MRV-specific requirements"""
        errors = []
        
        properties = document.get('properties', {})
        
        # Validate date range
        start_date = properties.get('start_date')
        end_date = properties.get('end_date')
        
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                if start >= end:
                    errors.append("start_date must be before end_date")
            except ValueError as e:
                errors.append(f"Invalid date format: {e}")
                
        # Validate net_removal_estimate
        estimate = properties.get('net_removal_estimate')
        if estimate:
            if not isinstance(estimate, dict):
                errors.append("net_removal_estimate must be an object")
            else:
                value = estimate.get('value')
                if value is not None and value < 0:
                    errors.append("net_removal_estimate value must be non-negative")
                    
                unit = estimate.get('unit')
                valid_units = ['tCO2e', 'kgCO2e', 'tCO2', 'kgCO2']
                if unit and unit not in valid_units:
                    errors.append(f"Invalid unit: {unit} (must be one of {valid_units})")
                    
        # Validate uncertainty if present
        uncertainty = properties.get('total_uncertainty')
        if uncertainty:
            if not isinstance(uncertainty, dict):
                errors.append("total_uncertainty must be an object")
            else:
                min_val = uncertainty.get('min')
                max_val = uncertainty.get('max')
                confidence = uncertainty.get('confidence_level')
                
                if min_val is not None and max_val is not None and min_val > max_val:
                    errors.append("uncertainty min must be <= max")
                    
                if confidence is not None and not (0 <= confidence <= 1):
                    errors.append("confidence_level must be between 0 and 1")
                    
        return errors
        
    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate a JSON file"""
        try:
            with open(file_path, 'r') as f:
                document = json.load(f)
            return self.validate_document(document)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        except FileNotFoundError:
            return False, [f"File not found: {file_path}"]
        except Exception as e:
            return False, [f"Error reading file: {e}"]
            
    def validate_api_endpoint(self, base_url: str, endpoint: str) -> Tuple[bool, List[str]]:
        """Validate an API endpoint response"""
        errors = []
        
        try:
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                errors.append(f"HTTP {response.status_code}: {response.reason}")
                return False, errors
                
            try:
                data = response.json()
            except json.JSONDecodeError:
                errors.append("Response is not valid JSON")
                return False, errors
                
            # If it's a single document, validate it
            if isinstance(data, dict) and data.get('type') == 'Feature':
                return self.validate_document(data)
                
            # If it's a list response, validate each document
            if isinstance(data, dict) and 'data' in data:
                all_valid = True
                for i, item in enumerate(data['data']):
                    if isinstance(item, dict) and item.get('type') == 'Feature':
                        valid, item_errors = self.validate_document(item)
                        if not valid:
                            all_valid = False
                            errors.extend([f"Item {i}: {err}" for err in item_errors])
                            
                return all_valid, errors
                
            return True, []  # Non-document endpoints
            
        except requests.RequestException as e:
            return False, [f"Request error: {e}"]
            
    def generate_compliance_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate a compliance report from validation results"""
        report = []
        report.append("OGCR API Specification Compliance Report")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r['valid'])
        
        report.append(f"Summary: {passed_tests}/{total_tests} tests passed")
        report.append("")
        
        for result in results:
            status = "PASS" if result['valid'] else "FAIL"
            report.append(f"[{status}] {result['name']}")
            
            if not result['valid'] and result['errors']:
                for error in result['errors']:
                    report.append(f"  - {error}")
            report.append("")
            
        return "\n".join(report)

def main():
    """Command-line interface for the spec checker"""
    parser = argparse.ArgumentParser(description="OGCR API Specification Checker")
    parser.add_argument('--file', '-f', help="Validate a JSON file")
    parser.add_argument('--api', '-a', help="Validate API endpoint (base URL)")
    parser.add_argument('--endpoint', '-e', help="Specific endpoint to test")
    parser.add_argument('--schema-dir', '-s', help="Directory containing JSON schemas")
    parser.add_argument('--report', '-r', help="Generate compliance report to file")
    parser.add_argument('--verbose', '-v', action='store_true', help="Verbose output")
    
    args = parser.parse_args()
    
    # Initialize checker
    checker = OGCRSpecChecker(args.schema_dir)
    
    results = []
    
    if args.file:
        # Validate file
        valid, errors = checker.validate_file(args.file)
        results.append({
            'name': f"File: {args.file}",
            'valid': valid,
            'errors': errors
        })
        
    elif args.api:
        # Validate API endpoints
        endpoints = [
            '/health',
            '/projects',
        ]
        
        if args.endpoint:
            endpoints = [args.endpoint]
            
        for endpoint in endpoints:
            valid, errors = checker.validate_api_endpoint(args.api, endpoint)
            results.append({
                'name': f"API: {args.api}{endpoint}",
                'valid': valid,
                'errors': errors
            })
    else:
        print("Please specify --file or --api option")
        sys.exit(1)
        
    # Output results
    if args.report:
        report = checker.generate_compliance_report(results)
        with open(args.report, 'w') as f:
            f.write(report)
        print(f"Compliance report written to {args.report}")
    else:
        for result in results:
            status = "✓" if result['valid'] else "✗"
            print(f"{status} {result['name']}")
            
            if not result['valid'] and (args.verbose or not args.report):
                for error in result['errors']:
                    print(f"  - {error}")
                    
    # Exit with error code if any validation failed
    if any(not r['valid'] for r in results):
        sys.exit(1)

if __name__ == "__main__":
    main()

