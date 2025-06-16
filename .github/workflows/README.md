# CI/CD Pipeline Documentation

## Overview

This repository contains a streamlined CI/CD pipeline that automates the deployment of the SRE Challenge application from development to production with proper validation, testing, and approval workflows.

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

#### Production Deployment Process
- **Plan Generation**: Creates Terraform plan for production with human-readable output
- **Approval Request**: Creates GitHub issue with embedded Terraform plan
- **Manual Approval**: Requires `/approve-prod` comment to proceed
- **Production Deploy**: Deploys to production after approval
- **Health Check**: Validates production deployment

## Workflow Files

### `ci-cd-pipeline.yml`
Main pipeline that orchestrates the entire CI/CD process.

### `approval-handler.yml`
Handles production deployment approvals through GitHub issue comments.

## Environment Configuration

### Development Environment
- **Protection**: Minimal protection rules
- **Approval**: 1 reviewer required
- **Auto-deploy**: Enabled for PR and merge

### Production Environment
- **Protection**: 
  - 2 reviewers required for approval
  - Only main branch can trigger deployments
  - Environment protection enabled
- **Approval**: 2 reviewers required
- **Manual approval**: Required via GitHub issue


## Configuration

### Required Secrets

```bash
# GitHub Container Registry (auto-provided)
GITHUB_TOKEN

# Kubernetes Cluster Access (if needed)
KUBECONFIG_BASE64

# Additional secrets as needed
```