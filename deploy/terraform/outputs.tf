output "release_name" {
  description = "Name of the Helm release"
  value       = helm_release.sre_challenge.name
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = helm_release.sre_challenge.namespace
}

output "status" {
  description = "Status of the Helm release"
  value       = helm_release.sre_challenge.status
}

output "ingress_host" {
  description = "Ingress hostname"
  value       = var.ingress_host
} 