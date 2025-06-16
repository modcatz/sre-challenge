variable "release_name" {
  description = "Name of the Helm release"
  type        = string
  default     = "sre-challenge"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "default"
}

variable "replica_count" {
  description = "Number of replicas"
  type        = number
  default     = 1
}

variable "image_repository" {
  description = "Container image repository"
  type        = string
  default     = "ghcr.io/your-org/sre-challenge"
}

variable "image_tag" {
  description = "Container image tag"
  type        = string
  default     = "latest"
}

variable "ingress_host" {
  description = "Ingress hostname"
  type        = string
  default     = "sre-challenge.local"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
} 