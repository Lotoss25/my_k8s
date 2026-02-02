terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  
  # МАГІЯ: Перенаправляємо всі запити на твій комп'ютер!
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  s3_use_path_style           = true 
  endpoints {
    s3  = "http://localhost:4566"  # Фейковий S3
    ec2 = "http://localhost:4566"  # Фейковий EC2 (сервери)
  }
}

# Ресурс: Створити "Відро" (Bucket) для файлів
resource "aws_s3_bucket" "my_bucket" {
  bucket = "arden-test-bucket"
}
