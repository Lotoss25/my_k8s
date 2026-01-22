terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}



provider "docker" {
host = "unix:///var/run/docker.sock"
}




resource "docker_image" "my_nginx_img"{
name = "nginx:latest"
keep_locally = false
}



resource "docker_container" "my_nginx_cont"{
image = docker_image.my_nginx_img.image_id
name = "terraform_test_nginx"

ports {
internal = 80
external = 8088
}
}
