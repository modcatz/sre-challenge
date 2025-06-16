# Terraform Deployment for SRE Challenge

Simple Terraform configuration to deploy the SRE Challenge application using Helm.

## Prerequisites

- Terraform 1.0+
- kubectl configured with your cluster
- Helm chart in `../helm-chart/`

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Deploy Development

```bash
# Deploy to development environment
terraform plan -var-file="terraform.tfvars.dev"
terraform apply -var-file="terraform.tfvars.dev"
```

### 3. Deploy Production

```bash
# Deploy to production environment
terraform plan -var-file="terraform.tfvars.prod"
terraform apply -var-file="terraform.tfvars.prod"
```

## Environment Files

### Development (`terraform.tfvars.dev`)
- Single replica
- `develop` image tag
- Development namespace
- Local hostname

### Production (`terraform.tfvars.prod`)
- 3 replicas
- `latest` image tag
- Production namespace
- Production hostname

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `release_name` | Helm release name | `sre-challenge` |
| `namespace` | Kubernetes namespace | `default` |
| `replica_count` | Number of replicas | `1` |
| `image_repository` | Container image repository | `ghcr.io/your-org/sre-challenge` |
| `image_tag` | Container image tag | `latest` |
| `ingress_host` | Ingress hostname | `sre-challenge.local` |
| `environment` | Environment name | `production` |

## Commands

```bash
# Plan deployment
terraform plan -var-file="terraform.tfvars.dev"    # Development
terraform plan -var-file="terraform.tfvars.prod"   # Production

# Apply deployment
terraform apply -var-file="terraform.tfvars.dev"   # Development
terraform apply -var-file="terraform.tfvars.prod"  # Production

# Destroy deployment
terraform destroy -var-file="terraform.tfvars.dev"  # Development
terraform destroy -var-file="terraform.tfvars.prod" # Production

# Show outputs
terraform output
```

## Environment Configurations

### Development
```hcl
release_name    = "sre-challenge-dev"
namespace       = "development"
replica_count   = 1
image_tag       = "develop"
ingress_host    = "sre-challenge-dev.local"
environment     = "development"
```

### Production
```hcl
release_name    = "sre-challenge-prod"
namespace       = "production"
replica_count   = 3
image_tag       = "latest"
ingress_host    = "sre-challenge.example.com"
environment     = "production"
``` 