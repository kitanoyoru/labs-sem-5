resource "kubernetes_namespace" "lab2_production" {
    metadata {
        name = var.namespace_name
    }
}

resource "kubernetes_deployment" "lab2" {
    metadata {
        name      = var.deployment_name
        namespace = kubernetes_namespace.lab2_production.metadata[0].name
    }

    spec {
        replicas = var.replica_count

        selector {
            match_labels = {
                app = var.app_label
            }
        }

        template {
            metadata {
                labels = {
                    app = var.app_label
                }
            }

            spec {
                container {
                    image = var.container_image
                    name  = var.container_name
                }
            }
        }
    }
}
