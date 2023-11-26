resource "kubernetes_namespace" "production" {
  metadata {
    name = var.namespace_name
  }
}

resource "kubernetes_config_map" "database_config" {
  metadata {
    name      = "database-config"
    namespace = kubernetes_namespace.production.metadata[0].name
  }

  data = {
    host     = "postgres.postgres"
    port     = "5432"
    dbname   = var.postgres_dbname 
    user     = var.postgres_user
    password = var.postgres_password
  }
}

resource "kubernetes_deployment" "database" {
  metadata {
    name      = "database-deployment"
    labels = {
      app = "database"
    }
    namespace = kubernetes_namespace.production.metadata[0].name
  }


  spec {
    selector {
      match_labels = {
        app = "database" 
      }
    }

    template {
      metadata {
        labels = {
          app = "database"
        }
      }

      spec {
        container {
          name  = "database"
          image = "postgres:latest"

          env {
            name  = "POSTGRES_DB"
            value = kubernetes_config_map.database_config.data["dbname"]
          }

          env {
            name  = "POSTGRES_USER"
            value = kubernetes_config_map.database_config.data["user"]
          }

          env {
            name  = "POSTGRES_PASSWORD"
            value = kubernetes_config_map.database_config.data["password"]
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "database" {
  metadata {
    name      = "database-service"
    labels = {
      app = "database"
    }
    namespace = kubernetes_namespace.production.metadata[0].name
  }

  spec {
    selector = {
        app = "database"
    }

    port {
      port        = kubernetes_config_map.database_config.data["port"]
      target_port = kubernetes_config_map.database_config.data["port"]
    }
  }
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = var.deployment_name
    labels = {
      app = "app"
    }
    namespace = kubernetes_namespace.production.metadata[0].name
  }

  spec {
    replicas = var.replica_count

    selector {
      match_labels = {
        app = "app" 
      }
    }

    template {
      metadata {
        labels = {
          app = "app" 
        }
      }

      spec {
        container {
          image = var.container_image
          name  = var.container_name

          env {
            name  = "DATABASE_URL"
            value = format("postgres://%s:%s@%s:%s/%s",
              kubernetes_config_map.database_config.data["user"],
              kubernetes_config_map.database_config.data["password"],
              kubernetes_config_map.database_config.data["host"],
              kubernetes_config_map.database_config.data["port"],
              kubernetes_config_map.database_config.data["dbname"]
            )
          }
        }
      }
    }
  }

  depends_on = [kubernetes_deployment.database, kubernetes_service.database]
}
