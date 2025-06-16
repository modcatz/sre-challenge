# SRE Challenge - Solution Guide

This document provides comprehensive instructions for running, deploying, and verifying the SRE Challenge application.

## Table of Contents

1. [How to Run the Code Locally](#how-to-run-the-code-locally)
2. [Pipeline Workflow](#pipeline-workflow)
   - [Environment Configuration](#environment-configuration)
3. [How to Verify the Application is Running](#how-to-verify-the-application-is-running)
4. [Security Considerations](#security-considerations)
5. [Security Changes to Code](#security-changes-to-code)
6. [Tradeoffs](#tradeoffs)
   - [LLMs note](#llms-note)

## How to Run the Code Locally

### Option 1: Direct Python Execution

```bash
cd src
pip install -r requirements.txt
export DB_PASSWORD="your-database-password"
export API_BASE_URL="http://localhost:8000"
export LOG_LEVEL="INFO"
export MAX_CONNECTIONS="10"
export ENVIRONMENT="local"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Using Docker

1. **Build the Docker image:**
   ```bash
   docker build -t sre-challenge .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 \
     -e DB_PASSWORD="your-database-password" \
     -e API_BASE_URL="http://localhost:8000" \
     -e LOG_LEVEL="INFO" \
     -e MAX_CONNECTIONS="10" \
     -e ENVIRONMENT="local" \
     sre-challenge
   ```

## Pipeline Workflow

### 1. Pull Request Pipeline

When a PR is created, the following steps are executed:

#### Validation Phase
- **Code Quality**: Linting (Black, Flake8)
- **Security**: Security scanning (Bandit, Safety)
- **Testing**: Unit tests with pytest
- **Infrastructure**: Helm chart validation, Terraform format and validation
- **Container**: Dockerfile linting with Hadolint

#### Build Phase
- **Image Building**: Builds and pushes Docker image to GitHub Container Registry
- **Image Tagging**: Tags with commit SHA, branch-prefixed SHA, and latest (for main branch)

#### Development Deployment
- **Terraform Deploy**: Deploys to development environment
- **Health Check**: Waits 60 seconds, then runs smoke tests

### 2. Merge Pipeline

When PR is merged to main/develop:

#### Automatic Development Deployment
- **Build**: Builds and pushes new image
- **Deploy**: Automatically deploys to development
- **Health Check**: Validates deployment with smoke tests
- **Rollback on failure**: Rollbacks helm to previous revision
- **Status reports**: Reports deployment status to Slack and a timestamp to Prometheus

#### Production Deployment Process
- **Plan Generation**: Creates Terraform plan for production with human-readable output
- **Approval Request**: Creates GitHub issue with embedded Terraform plan
- **Manual Approval**: Requires `/approve-prod` comment to proceed
- **Production Deploy**: Deploys to production after approval
- **Health Check**: Validates production deployment
- **Rollback on failure**: Rollbacks helm to previous revision
- **Status reports**: Reports deployment status to Slack and a timestamp to Prometheus

### Environment Configuration

Each environment is protected by the following rules:

#### Development Environment
- **Protection**: Minimal protection rules
- **Approval**: 1 reviewer required
- **Auto-deploy**: Enabled for PR and merge

#### Production Environment
- **Protection**: 
  - 2 reviewers required for approval
  - Only main branch can trigger deployments
  - Environment protection enabled
- **Approval**: 2 reviewers required
- **Manual approval**: Required via GitHub issue

## How to Verify the Application is Running

### Automated Verification

The CI/CD pipeline includes automated verification:

1. **Health Checks:** Automatic health checks after deployment
2. **Rollback:** Automatic rollback on health check failure
3. **Monitoring:** Integration with Prometheus for metrics
4. **Notifications:** Slack notifications for deployment status

## Security Considerations

- `DB_PASSWORD` is marked as sensitive in Terraform
- Secrets are stored in GitHub Secrets, not in code
- Production deployments require manual approval
- Health checks ensure application stability
- Automatic rollback on deployment failures

## Security Changes to Code

- Removed unused dependencies from requirements.txt
- Removed exposure of database password

## Tradeoffs

I had very limited time and in production environment I would add at least features:

### Infrastructure Improvements
- **OIDC GitHub Cloud Provider Authentication**
- **Secret management with rotation**
- **Terraform S3 State + State Lock in DynamoDB**

### Kubernetes Enhancements
- **TLS for Ingress**
- **Resources Specified (CPU/Memory limits)**
- **Horizontal Pod Autoscaler (HPA)**
- **Secrets Properly Mounted from Secret Management System**
- **Readiness Probe/Liveness Probe**
- **Network Policies**

### LLMs note

Code is written in Cursor under my full supervision and endless rewrites. 
