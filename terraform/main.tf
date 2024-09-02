terraform {
  required_version = "~>1.8"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>5.32"
    }
  }

  backend "local" {}
}

provider "google" {
  project = "my-projects-306716"
  region  = "asia-southeast1"
}
