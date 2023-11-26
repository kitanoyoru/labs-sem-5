variable "namespace_name" {
    description = "Name of the Kubernetes namespace"
    type        = string
    default     = "k8s-ns-for-lab2"
}




variable "deployment_name" {
    description = "Name of the Kubernetes deployment"
    type        = string
    default     = "lab2-app"
}

variable "replica_count" {
    description = "Number of replicas for the deployment"
    type        = number
    default     = 2
}





variable "app_label" {
    description = "Label for the application"
    type        = string
    default     = "App"
}

variable "container_image" {
    description = "Docker image for the container"
    type        = string
    default     = "kitanoyoru/db-lab2-app:latest"
}

variable "container_name" {
    description = "Name of the container"
    type        = string
    default     = "app"
}




variable "postgres_user" {
    description = "Username for PostgreSQL"
    type        = string
    default     = "kitanoyoru"
}

variable "postgres_password" {
    description = "Password for PostgreSQL"
    type        = string
    default     = "1234"
}

variable "postgres_dbname" {
    description = "Database for PostgreSQL"
    type        = string
    default     = "main"
}
