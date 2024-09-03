provider "github" {
  token = var.github_token
  owner = "kvdomingo"
}

locals {
  repo_name = "devsecops-play"
  status_checks = toset([
    "Run Snyk security scans",
    "Run pre-commit checks",
    "Run Bandit security scan",
    "Run Gitleaks secret scan",
    "Run Hadolint scan",
    "Apply Terraform infrastructure",
  ])
}

resource "github_repository" "default" {
  name                   = local.repo_name
  description            = "DevSecOps Playground"
  allow_merge_commit     = false
  delete_branch_on_merge = true
  allow_update_branch    = true

  security_and_analysis {
    secret_scanning {
      status = "enabled"
    }

    secret_scanning_push_protection {
      status = "enabled"
    }
  }
}

resource "github_repository_ruleset" "default" {
  name        = "Default"
  repository  = github_repository.default.name
  enforcement = "active"
  target      = "branch"

  conditions {
    ref_name {
      exclude = []
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    required_linear_history = true
    deletion                = true
    non_fast_forward        = true

    pull_request {
      dismiss_stale_reviews_on_push     = true
      required_review_thread_resolution = true
    }

    required_status_checks {
      strict_required_status_checks_policy = true

      dynamic "required_check" {
        for_each = local.status_checks
        content {
          context        = required_check.value
          integration_id = 15368
        }
      }
    }
  }
}
