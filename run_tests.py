#!/usr/bin/env python3
"""
OGCR API Test Runner

Comprehensive test runner for all OGCR API components.

License: MIT
Copyright (c) 2025 OGCR Consortium
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ {command}")
            if result.stdout:
                print(f"  Output: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {command}")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"✗ {command} - Exception: {e}")
        return False

def main():
    """Run all tests"""
    print("OGCR API Test Suite")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    success_count = 0
    total_count = 0
    
    # Test 1: Validation Tools Tests
    print("\n1. Running Validation Tools Tests...")
    total_count += 1
    if run_command("python -m pytest tests/test_spec_checker.py -v", cwd=base_dir):
        success_count += 1
    
    # Test 2: API Server Tests
    print("\n2. Running API Server Tests...")
    total_count += 1
    if run_command("python -m pytest tests/test_api.py -v", cwd=base_dir):
        success_count += 1
    
    # Test 3: Spec Checker CLI Tests
    print("\n3. Testing Spec Checker CLI...")
    total_count += 1
    if run_command("python tools/spec_checker.py --file examples/valid_pdd.json", cwd=base_dir):
        success_count += 1
    
    # Test 4: Schema Validation Tests
    print("\n4. Testing Schema Validation...")
    total_count += 1
    if run_command("python tools/spec_checker.py --file examples/valid_mrv.json", cwd=base_dir):
        success_count += 1
    
    # Test 5: Error Detection Tests
    print("\n5. Testing Error Detection...")
    total_count += 1
    # This should fail (return non-zero), so we invert the logic
    result = subprocess.run(
        "python tools/spec_checker.py --file examples/invalid_pdd.json",
        shell=True,
        cwd=base_dir,
        capture_output=True
    )
    if result.returncode != 0:  # Should fail for invalid document
        print("✓ Error detection working correctly")
        success_count += 1
    else:
        print("✗ Error detection not working")
    
    # Test 6: FastAPI Server Startup
    print("\n6. Testing FastAPI Server Startup...")
    total_count += 1
    if run_command("python -c 'import sys; sys.path.append(\"server\"); from app.main import app; print(\"FastAPI loaded successfully\")'", cwd=base_dir):
        success_count += 1

    # Test 7: OpenAPI Specification Validation
    print("\n7. Validating OpenAPI Specification...")
    total_count += 1
    if run_command("python tools/validate_openapi.py", cwd=base_dir):
        success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Test Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

