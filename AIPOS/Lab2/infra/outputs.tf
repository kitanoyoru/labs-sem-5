output "namespace_name" {
    description = "Name of the Kubernetes namespace"
    value       = kubernetes_namespace.lab2_production.metadata[0].name
}

output "deployment_name" {
    description = "Name of the Kubernetes deployment"
    value       = kubernetes_deployment.lab2.metadata.name
}

output "replica_count" {
    description = "Number of replicas for the deployment"
    value       = kubernetes_deployment.lab2.spec.replicas
}

output "app_label" {
    description = "Label for the application"
    value       = kubernetes_deployment.lab2.spec.selector.match_labels.app
}

output "container_image" {
    description = "Docker image for the container"
    value       = kubernetes_deployment.lab2.spec.template.spec.container.image
}

output "container_name" {
    description = "Name of the container"
    value       = kubernetes_deployment.lab2.spec.template.spec.container.name
}
