# 1. Провайдер (Інструмент)
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# 2. Ресурс: Образ (Цегла)
resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

# 3. Ресурс: Контейнер (Стіна)
resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "terraform_web_server"
  
  ports {
    internal = 80
    external = 8080
  }
}
