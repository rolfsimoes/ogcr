# OGCR API Implementation Guidelines

**Version:** 0.1.0  
**Date:** July 2025   
**Authors:** OGCR Consortium  
**Status:** Draft  
**License:** CC-BY 4.0

## Overview

This document provides comprehensive implementation guidelines for the OGCR API Specification, covering technical requirements, best practices, and step-by-step implementation procedures. These guidelines ensure consistent, secure, and interoperable implementations across different organizations and technical environments.

## 1. Getting Started

### 1.1 Prerequisites

Before implementing the Carbon Registry Specification, ensure your development environment meets the following requirements:

**Technical Infrastructure:**
- Modern web development environment with Node.js 18+ or Python 3.9+
- Database system supporting JSON documents (PostgreSQL 13+, MongoDB 5+)
- Blockchain development environment (Hardhat, Truffle, or similar)
- Container orchestration platform (Docker, Kubernetes)

**Regulatory Compliance:**
- Understanding of applicable carbon market regulations
- Data protection and privacy compliance framework (GDPR, CCPA)
- Security audit and penetration testing capabilities

**Team Expertise:**
- Blockchain development experience
- Carbon market domain knowledge
- API design and implementation skills
- Security and compliance expertise

### 1.2 Architecture Planning

**System Sizing:** Determine expected transaction volumes, user counts, and data storage requirements. The specification supports implementations ranging from small pilot projects to large-scale international registries.

**Network Selection:** Choose appropriate blockchain networks based on cost, performance, and regulatory requirements. Consider layer-2 solutions for high-volume applications.

**Integration Requirements:** Identify existing systems that need integration including monitoring equipment, verification bodies, and market platforms.

## 2. Core Implementation Steps

### 2.1 Database Schema Implementation

Implement the core data models following the JSON schemas provided in the specification:

**Project Design Document Storage:**
```sql
CREATE TABLE projects (
    id VARCHAR(100) PRIMARY KEY,
    document JSONB NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    blockchain_hash VARCHAR(66),
    CONSTRAINT valid_status CHECK (status IN ('draft', 'submitted', 'approved', 'rejected', 'archived'))
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created ON projects(created_at);
CREATE INDEX idx_projects_hash ON projects(blockchain_hash);
```

**MRV Document Storage:**
```sql
CREATE TABLE mrv_reports (
    id VARCHAR(100) PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(id),
    document JSONB NOT NULL,
    verification_status VARCHAR(50) NOT NULL,
    reporting_period_start DATE NOT NULL,
    reporting_period_end DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    verified_at TIMESTAMP,
    CONSTRAINT valid_verification_status CHECK (verification_status IN ('unverified', 'pending', 'verified', 'rejected')),
    CONSTRAINT valid_period CHECK (reporting_period_end > reporting_period_start)
);

CREATE INDEX idx_mrv_project ON mrv_reports(project_id);
CREATE INDEX idx_mrv_period ON mrv_reports(reporting_period_start, reporting_period_end);
CREATE INDEX idx_mrv_status ON mrv_reports(verification_status);
```

**Carbon Credit Tracking:**
```sql
CREATE TABLE carbon_credits (
    token_id VARCHAR(100) PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(id),
    mrv_id VARCHAR(100) NOT NULL REFERENCES mrv_reports(id),
    owner_address VARCHAR(42) NOT NULL,
    carbon_amount DECIMAL(15,6) NOT NULL,
    vintage_year INTEGER NOT NULL,
    retired BOOLEAN DEFAULT FALSE,
    retirement_timestamp TIMESTAMP,
    serial_number VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_credits_owner ON carbon_credits(owner_address);
CREATE INDEX idx_credits_project ON carbon_credits(project_id);
CREATE INDEX idx_credits_vintage ON carbon_credits(vintage_year);
CREATE INDEX idx_credits_retired ON carbon_credits(retired);
```

### 2.2 API Implementation

Implement RESTful APIs following the specification requirements:

**Express.js Example Structure:**
```javascript
const express = require('express');
const { body, param, query, validationResult } = require('express-validator');

const app = express();

// Project management endpoints
app.post('/projects', 
  body('type').equals('Feature'),
  body('ogcr_version').matches(/^\d+\.\d+\.\d+$/),
  body('profile').equals('pdd'),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    // Implementation logic
    const project = await createProject(req.body);
    res.status(201).json(project);
  }
);

app.get('/projects/:id',
  param('id').isAlphanumeric(),
  async (req, res) => {
    const project = await getProject(req.params.id);
    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }
    res.json(project);
  }
);
```

**Python FastAPI Example:**
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

app = FastAPI(title="Carbon Registry API", version="0.1.0")

class PDDCreate(BaseModel):
    type: str = Field(..., regex="^Feature$")
    ogcr_version: str = Field(..., regex=r"^\d+\.\d+\.\d+$")
    profile: str = Field(..., regex="^pdd$")
    geometry: dict
    properties: dict

@app.post("/projects", status_code=201)
async def create_project(pdd: PDDCreate):
    project_id = str(uuid.uuid4())
    # Implementation logic
    return {"id": project_id, "status": "draft"}

@app.get("/projects/{project_id}")
async def get_project(project_id: str):
    project = await fetch_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
```

### 2.3 Smart Contract Implementation

Deploy smart contracts following the requirements specification:

**Development Environment Setup:**
```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545"
    },
    sepolia: {
      url: process.env.SEPOLIA_URL,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

**Contract Deployment Script:**
```javascript
// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  // Deploy AccessControl first
  const AccessControl = await ethers.getContractFactory("AccessControl");
  const accessControl = await AccessControl.deploy();
  await accessControl.deployed();
  
  // Deploy ProjectRegistry
  const ProjectRegistry = await ethers.getContractFactory("ProjectRegistry");
  const projectRegistry = await ProjectRegistry.deploy(accessControl.address);
  await projectRegistry.deployed();
  
  // Deploy MRVRegistry
  const MRVRegistry = await ethers.getContractFactory("MRVRegistry");
  const mrvRegistry = await MRVRegistry.deploy(
    accessControl.address,
    projectRegistry.address
  );
  await mrvRegistry.deployed();
  
  // Deploy CRUToken
  const CRUToken = await ethers.getContractFactory("CRUToken");
  const cruToken = await CRUToken.deploy(
    "Carbon Removal Units",
    "CRU",
    accessControl.address
  );
  await cruToken.deployed();
  
  console.log("Contracts deployed:");
  console.log("AccessControl:", accessControl.address);
  console.log("ProjectRegistry:", projectRegistry.address);
  console.log("MRVRegistry:", mrvRegistry.address);
  console.log("CRUToken:", cruToken.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

## 3. Security Implementation

### 3.1 Authentication and Authorization

Implement comprehensive security measures:

**JWT Token Implementation:**
```javascript
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

class AuthService {
  async authenticateUser(email, password) {
    const user = await User.findOne({ email });
    if (!user || !await bcrypt.compare(password, user.passwordHash)) {
      throw new Error('Invalid credentials');
    }
    
    const token = jwt.sign(
      { userId: user.id, roles: user.roles },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    return { token, user: { id: user.id, email: user.email, roles: user.roles } };
  }
  
  verifyToken(token) {
    return jwt.verify(token, process.env.JWT_SECRET);
  }
}
```

**Role-Based Access Control:**
```javascript
const authorize = (requiredRoles) => {
  return (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      const userRoles = decoded.roles || [];
      
      const hasRequiredRole = requiredRoles.some(role => userRoles.includes(role));
      if (!hasRequiredRole) {
        return res.status(403).json({ error: 'Insufficient permissions' });
      }
      
      req.user = decoded;
      next();
    } catch (error) {
      return res.status(401).json({ error: 'Invalid token' });
    }
  };
};

// Usage
app.post('/projects/:id/approve', 
  authorize(['validator', 'admin']),
  async (req, res) => {
    // Approval logic
  }
);
```

### 3.2 Data Validation and Sanitization

Implement comprehensive input validation:

**Schema Validation Middleware:**
```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const validateSchema = (schema) => {
  const validate = ajv.compile(schema);
  
  return (req, res, next) => {
    const valid = validate(req.body);
    if (!valid) {
      return res.status(400).json({
        error: 'Validation failed',
        details: validate.errors
      });
    }
    next();
  };
};

// Load schemas
const pddSchema = require('../schemas/pdd-schema.json');
const mrvSchema = require('../schemas/mrv-schema.json');

// Apply validation
app.post('/projects', validateSchema(pddSchema), createProject);
app.post('/projects/:id/monitoring', validateSchema(mrvSchema), createMRV);
```

### 3.3 Blockchain Security

Implement secure blockchain interactions:

**Safe Contract Interaction:**
```javascript
const { ethers } = require('ethers');

class BlockchainService {
  constructor(providerUrl, privateKey, contractAddresses) {
    this.provider = new ethers.providers.JsonRpcProvider(providerUrl);
    this.wallet = new ethers.Wallet(privateKey, this.provider);
    this.contracts = this.initializeContracts(contractAddresses);
  }
  
  async registerProject(projectId, documentHash, storageUri) {
    try {
      // Estimate gas first
      const gasEstimate = await this.contracts.projectRegistry.estimateGas
        .registerProject(documentHash, projectId, storageUri);
      
      // Add 20% buffer to gas estimate
      const gasLimit = gasEstimate.mul(120).div(100);
      
      const tx = await this.contracts.projectRegistry.registerProject(
        documentHash,
        projectId,
        storageUri,
        { gasLimit }
      );
      
      const receipt = await tx.wait();
      return {
        transactionHash: receipt.transactionHash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString()
      };
    } catch (error) {
      console.error('Blockchain transaction failed:', error);
      throw new Error('Failed to register project on blockchain');
    }
  }
}
```

## 4. Testing Strategy

### 4.1 Unit Testing

Implement comprehensive unit tests:

**API Testing with Jest:**
```javascript
const request = require('supertest');
const app = require('../server/app');

describe('Project API', () => {
  test('POST /projects should create a new project', async () => {
    const projectData = {
      type: 'Feature',
      ogcr_version: '0.1.0',
      profile: 'pdd',
      geometry: {
        type: 'Polygon',
        coordinates: [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
      },
      properties: {
        name: 'Test Project',
        project_type: 'afforestation',
        status: 'draft',
        creation_date: '2024-12-07T10:00:00Z',
        actor_id: 'test-actor'
      }
    };
    
    const response = await request(app)
      .post('/projects')
      .send(projectData)
      .expect(201);
    
    expect(response.body).toHaveProperty('id');
    expect(response.body.status).toBe('draft');
  });
  
  test('GET /projects/:id should return project details', async () => {
    const projectId = 'test-project-123';
    
    const response = await request(app)
      .get(`/projects/${projectId}`)
      .expect(200);
    
    expect(response.body).toHaveProperty('id', projectId);
    expect(response.body).toHaveProperty('type', 'Feature');
  });
});
```

**Smart Contract Testing:**
```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ProjectRegistry", function () {
  let projectRegistry;
  let accessControl;
  let owner, validator, developer;
  
  beforeEach(async function () {
    [owner, validator, developer] = await ethers.getSigners();
    
    const AccessControl = await ethers.getContractFactory("AccessControl");
    accessControl = await AccessControl.deploy();
    
    const ProjectRegistry = await ethers.getContractFactory("ProjectRegistry");
    projectRegistry = await ProjectRegistry.deploy(accessControl.address);
    
    // Grant validator role
    await accessControl.grantRole(
      await accessControl.VALIDATOR_ROLE(),
      validator.address
    );
  });
  
  it("Should register a new project", async function () {
    const projectId = "test-project-001";
    const documentHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("test"));
    const storageUri = "https://example.com/project.json";
    
    await expect(
      projectRegistry.connect(developer).registerProject(
        documentHash,
        projectId,
        storageUri
      )
    ).to.emit(projectRegistry, "ProjectRegistered")
     .withArgs(projectId, documentHash, developer.address, storageUri);
    
    const project = await projectRegistry.getProject(projectId);
    expect(project.projectId).to.equal(projectId);
    expect(project.pddHash).to.equal(documentHash);
  });
});
```

### 4.2 Integration Testing

Test complete workflows:

**End-to-End Workflow Testing:**
```javascript
describe('Complete Project Workflow', () => {
  test('Project creation to credit issuance', async () => {
    // 1. Create project
    const projectResponse = await request(app)
      .post('/projects')
      .send(validProjectData)
      .expect(201);
    
    const projectId = projectResponse.body.id;
    
    // 2. Submit for approval
    await request(app)
      .post(`/projects/${projectId}/submit`)
      .set('Authorization', `Bearer ${developerToken}`)
      .expect(200);
    
    // 3. Approve project
    await request(app)
      .post(`/projects/${projectId}/approve`)
      .set('Authorization', `Bearer ${validatorToken}`)
      .send({ validation_report_hash: 'test-hash' })
      .expect(200);
    
    // 4. Submit MRV report
    const mrvResponse = await request(app)
      .post(`/projects/${projectId}/monitoring`)
      .set('Authorization', `Bearer ${developerToken}`)
      .send(validMrvData)
      .expect(201);
    
    const mrvId = mrvResponse.body.id;
    
    // 5. Verify MRV report
    await request(app)
      .post(`/projects/${projectId}/monitoring/${mrvId}/verify`)
      .set('Authorization', `Bearer ${verifierToken}`)
      .send({ verified_removals: 1000, verification_outcome: 'approved' })
      .expect(200);
    
    // 6. Check credit issuance
    const creditsResponse = await request(app)
      .get('/credits')
      .query({ project_id: projectId })
      .expect(200);
    
    expect(creditsResponse.body.data).toHaveLength(1000);
  });
});
```

## 5. Deployment and Operations

### 5.1 Production Deployment

Deploy using containerized infrastructure:

**Docker Configuration:**
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

USER node

CMD ["npm", "start"]
```

**Kubernetes Deployment:**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: carbon-registry-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: carbon-registry-api
  template:
    metadata:
      labels:
        app: carbon-registry-api
    spec:
      containers:
      - name: api
        image: carbon-registry:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: carbon-registry-secrets
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: carbon-registry-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: carbon-registry-service
spec:
  selector:
    app: carbon-registry-api
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

### 5.2 Monitoring and Observability

Implement comprehensive monitoring:

**Application Metrics:**
```javascript
const prometheus = require('prom-client');

// Create metrics
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code']
});

const projectsCreated = new prometheus.Counter({
  name: 'projects_created_total',
  help: 'Total number of projects created'
});

// Middleware to collect metrics
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });
  
  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(await prometheus.register.metrics());
});
```

**Health Checks:**
```javascript
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    checks: {}
  };
  
  try {
    // Database health check
    await db.query('SELECT 1');
    health.checks.database = 'healthy';
  } catch (error) {
    health.checks.database = 'unhealthy';
    health.status = 'unhealthy';
  }
  
  try {
    // Blockchain health check
    await blockchainService.getBlockNumber();
    health.checks.blockchain = 'healthy';
  } catch (error) {
    health.checks.blockchain = 'unhealthy';
    health.status = 'unhealthy';
  }
  
  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

## 6. Compliance and Auditing

### 6.1 Audit Trail Implementation

Maintain comprehensive audit trails:

**Audit Logging:**
```javascript
class AuditLogger {
  async logAction(userId, action, resourceType, resourceId, details = {}) {
    const auditEntry = {
      timestamp: new Date(),
      userId,
      action,
      resourceType,
      resourceId,
      details,
      ipAddress: details.ipAddress,
      userAgent: details.userAgent
    };
    
    await db.collection('audit_log').insertOne(auditEntry);
    
    // Also emit event for real-time monitoring
    eventEmitter.emit('audit', auditEntry);
  }
}

// Usage in API endpoints
app.post('/projects/:id/approve', async (req, res) => {
  try {
    const result = await approveProject(req.params.id, req.body);
    
    await auditLogger.logAction(
      req.user.id,
      'project_approved',
      'project',
      req.params.id,
      {
        validationReportHash: req.body.validation_report_hash,
        ipAddress: req.ip,
        userAgent: req.get('User-Agent')
      }
    );
    
    res.json(result);
  } catch (error) {
    // Error handling
  }
});
```

### 6.2 Data Privacy and GDPR Compliance

Implement privacy protection measures:

**Data Anonymization:**
```javascript
class PrivacyService {
  anonymizePersonalData(data) {
    const anonymized = { ...data };
    
    // Remove or hash personal identifiers
    if (anonymized.email) {
      anonymized.email = this.hashEmail(anonymized.email);
    }
    
    if (anonymized.name) {
      anonymized.name = 'ANONYMIZED';
    }
    
    return anonymized;
  }
  
  async handleDataDeletionRequest(userId) {
    // Mark user data for deletion
    await db.collection('users').updateOne(
      { _id: userId },
      { 
        $set: { 
          deleted: true,
          deletedAt: new Date(),
          email: 'DELETED',
          name: 'DELETED'
        }
      }
    );
    
    // Anonymize audit logs
    await db.collection('audit_log').updateMany(
      { userId },
      { $set: { userId: 'ANONYMIZED' } }
    );
  }
}
```

This comprehensive implementation guide provides the foundation for building secure, scalable, and compliant carbon registry systems following the Carbon Registry Specification. Regular updates and community feedback will ensure these guidelines remain current with evolving best practices and regulatory requirements.

