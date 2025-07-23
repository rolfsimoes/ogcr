"""
Comprehensive tests for OGCR API

License: MIT
Copyright (c) 2025 OGCR Consortium
"""

import pytest
import json
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from app.main import app

# Create test client
client = TestClient(app)

# Test data
VALID_PDD = {
    "type": "Feature",
    "ogcr_version": "0.1.0",
    "profile": "pdd",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    },
    "properties": {
        "name": "Test Forest Project",
        "description": "A test afforestation project",
        "creation_date": "2024-12-07T10:00:00Z",
        "project_type": "afforestation",
        "status": "draft",
        "actor_id": "test-developer"
    }
}

VALID_MRV = {
    "type": "Feature",
    "ogcr_version": "0.1.0",
    "profile": "mrv",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    },
    "properties": {
        "project_id": "test-project",
        "methodology_id": "test-methodology",
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

MOCK_TOKEN = "Bearer mock-token"

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

class TestProjectEndpoints:
    """Test project-related endpoints"""
    
    def test_create_project_success(self):
        """Test successful project creation"""
        response = client.post(
            "/projects",
            json=VALID_PDD,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["status"] == "draft"
        assert "created_at" in data
        assert "validation_results" in data
        
        return data["id"]  # Return for use in other tests
    
    def test_create_project_unauthorized(self):
        """Test project creation without authentication"""
        response = client.post("/projects", json=VALID_PDD)
        assert response.status_code == 403  # FastAPI returns 403 for missing auth
    
    def test_create_project_invalid_data(self):
        """Test project creation with invalid data"""
        invalid_pdd = VALID_PDD.copy()
        invalid_pdd["type"] = "InvalidType"
        
        response = client.post(
            "/projects",
            json=invalid_pdd,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 422  # Validation error
    
    def test_get_project_success(self):
        """Test getting project details"""
        # First create a project
        create_response = client.post(
            "/projects",
            json=VALID_PDD,
            headers={"Authorization": MOCK_TOKEN}
        )
        project_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(f"/projects/{project_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == project_id
        assert data["type"] == "Feature"
        assert data["properties"]["name"] == "Test Forest Project"
    
    def test_get_project_not_found(self):
        """Test getting non-existent project"""
        response = client.get("/projects/non-existent")
        assert response.status_code == 404
    
    def test_list_projects(self):
        """Test listing projects"""
        response = client.get("/projects")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
        
        pagination = data["pagination"]
        assert "total" in pagination
        assert "limit" in pagination
        assert "offset" in pagination
        assert "has_more" in pagination
    
    def test_list_projects_with_filters(self):
        """Test listing projects with filters"""
        response = client.get("/projects?status=draft&limit=5")
        assert response.status_code == 200
        
        data = response.json()
        assert data["pagination"]["limit"] == 5
    
    def test_update_project_success(self):
        """Test updating a draft project"""
        # Create a project
        create_response = client.post(
            "/projects",
            json=VALID_PDD,
            headers={"Authorization": MOCK_TOKEN}
        )
        project_id = create_response.json()["id"]
        
        # Update it
        updated_pdd = VALID_PDD.copy()
        updated_pdd["properties"]["name"] = "Updated Project Name"
        
        response = client.put(
            f"/projects/{project_id}",
            json=updated_pdd,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["properties"]["name"] == "Updated Project Name"
    
    def test_submit_project_success(self):
        """Test submitting a project"""
        # Create a project
        create_response = client.post(
            "/projects",
            json=VALID_PDD,
            headers={"Authorization": MOCK_TOKEN}
        )
        project_id = create_response.json()["id"]
        
        # Submit it
        response = client.post(
            f"/projects/{project_id}/submit",
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "submitted"
        assert "blockchain_reference" in data
        assert "submitted_at" in data
    
    def test_approve_project_success(self):
        """Test approving a submitted project"""
        # Create and submit a project
        create_response = client.post(
            "/projects",
            json=VALID_PDD,
            headers={"Authorization": MOCK_TOKEN}
        )
        project_id = create_response.json()["id"]
        
        client.post(
            f"/projects/{project_id}/submit",
            headers={"Authorization": MOCK_TOKEN}
        )
        
        # Approve it
        approval_data = {"notes": "Project approved"}
        response = client.post(
            f"/projects/{project_id}/approve",
            json=approval_data,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "approved"
        assert "approved_at" in data
        assert "approved_by" in data

class TestMRVEndpoints:
    """Test MRV-related endpoints"""
    
    def setup_method(self):
        """Set up an approved project for MRV tests"""
        # Create and approve a project
        create_response = client.post(
            "/projects",
            json=VALID_PDD,
            headers={"Authorization": MOCK_TOKEN}
        )
        self.project_id = create_response.json()["id"]
        
        client.post(
            f"/projects/{self.project_id}/submit",
            headers={"Authorization": MOCK_TOKEN}
        )
        
        client.post(
            f"/projects/{self.project_id}/approve",
            json={"notes": "Approved for testing"},
            headers={"Authorization": MOCK_TOKEN}
        )
    
    def test_create_mrv_report_success(self):
        """Test creating MRV report"""
        mrv_data = VALID_MRV.copy()
        mrv_data["properties"]["project_id"] = self.project_id
        
        response = client.post(
            f"/projects/{self.project_id}/monitoring",
            json=mrv_data,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["status"] == "pending_verification"
        assert "validation_results" in data
    
    def test_get_mrv_report_success(self):
        """Test getting MRV report details"""
        # Create MRV report
        mrv_data = VALID_MRV.copy()
        mrv_data["properties"]["project_id"] = self.project_id
        
        create_response = client.post(
            f"/projects/{self.project_id}/monitoring",
            json=mrv_data,
            headers={"Authorization": MOCK_TOKEN}
        )
        mrv_id = create_response.json()["id"]
        
        # Get MRV report
        response = client.get(f"/projects/{self.project_id}/monitoring/{mrv_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == mrv_id
        assert data["properties"]["project_id"] == self.project_id
    
    def test_list_mrv_reports(self):
        """Test listing MRV reports for a project"""
        response = client.get(f"/projects/{self.project_id}/monitoring")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_verify_mrv_report_success(self):
        """Test verifying MRV report"""
        # Create MRV report
        mrv_data = VALID_MRV.copy()
        mrv_data["properties"]["project_id"] = self.project_id
        
        create_response = client.post(
            f"/projects/{self.project_id}/monitoring",
            json=mrv_data,
            headers={"Authorization": MOCK_TOKEN}
        )
        mrv_id = create_response.json()["id"]
        
        # Verify it
        verification_data = {"verified_removals": 950.0}
        response = client.post(
            f"/projects/{self.project_id}/monitoring/{mrv_id}/verify",
            json=verification_data,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "verified"
        assert "verified_at" in data
        assert "verified_by" in data

class TestCreditEndpoints:
    """Test credit-related endpoints"""
    
    def test_list_credits(self):
        """Test listing credits"""
        response = client.get("/credits")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_list_credits_with_filters(self):
        """Test listing credits with filters"""
        response = client.get("/credits?status=active&vintage=2024")
        assert response.status_code == 200
    
    def test_transfer_credits(self):
        """Test transferring credits"""
        transfer_data = {
            "credit_ids": ["credit_1", "credit_2"],
            "recipient": "0x1234567890abcdef"
        }
        
        response = client.post(
            "/credits/transfer",
            json=transfer_data,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "transfer_id" in data
        assert "status" in data
        assert "blockchain_transaction" in data

class TestValidation:
    """Test data validation"""
    
    def test_invalid_geometry_type(self):
        """Test invalid geometry type rejection"""
        invalid_pdd = VALID_PDD.copy()
        invalid_pdd["geometry"]["type"] = "InvalidType"
        
        response = client.post(
            "/projects",
            json=invalid_pdd,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 422
    
    def test_invalid_project_type(self):
        """Test invalid project type rejection"""
        invalid_pdd = VALID_PDD.copy()
        invalid_pdd["properties"]["project_type"] = "invalid_type"
        
        response = client.post(
            "/projects",
            json=invalid_pdd,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 422
    
    def test_invalid_ogcr_version(self):
        """Test invalid OGCR version rejection"""
        invalid_pdd = VALID_PDD.copy()
        invalid_pdd["ogcr_version"] = "invalid"
        
        response = client.post(
            "/projects",
            json=invalid_pdd,
            headers={"Authorization": MOCK_TOKEN}
        )
        assert response.status_code == 422

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_for_invalid_endpoint(self):
        """Test 404 for non-existent endpoints"""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Test 405 for invalid HTTP methods"""
        response = client.delete("/projects")
        assert response.status_code == 405

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

