resource "helm_release" "sre_challenge" {
  name       = var.release_name
  chart      = "./helm-chart"
  namespace  = var.namespace
  create_namespace = true

  set {
    name  = "replicaCount"
    value = var.replica_count
  }

  set {
    name  = "image.repository"
    value = var.image_repository
  }

  set {
    name  = "image.tag"
    value = var.image_tag
  }

  set {
    name  = "ingress.host"
    value = var.ingress_host
  }

  set {
    name  = "env.ENVIRONMENT"
    value = var.environment
  }

  set {
    name  = "env.DB_PASSWORD"
    value = var.db_password
  }
} 