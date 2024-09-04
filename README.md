# DevSecOps Playground

This is a sample GitHub repository that implements DevSecOps principles and processes.

## Features

### Infrastructure-as-Code (IaC)

The repository is defined in Terraform for reproducible configurations. The following settings and protection rules are in place:

- Prevent deletion of `main` branch
- Prevent pushes and force-pushes to `main`
- Changes to `main` must be introduced via PRs
- PRs must have passing status checks, and all conversations must be resolved before merging is allowed
- Require PRs to be updated with the latest code from `main`
- Dismiss PR approvals when new code is pushed
- Disable merge commits
- Automatically delete PR branches after merging
- Require linear history

### Automated security scans in CI

GitHub Actions are configured for the following:

- Validate Terraform configuration in PRs; apply only once merged to `main`
- Run pre-commit hooks on all files
- Run security scans both in PRs and in `main`. [Snyk](https://snyk.io) is used as the main code scanner
  - Run **Snyk Code** and upload the results to GitHub Code Scanning so that they are visible in the Security tab (accessible only to collaborators with at least _Maintain_ permissions)
  - (WIP) Run **Snyk Container** and upload the results to GitHub Code Scanning
  - Run **Snyk IaC** and upload the results to GitHub Code Scanning
  - Run **Bandit** to scan for OWASP Top 10 vulnerabilities, as well as other common issues
  - Run **Hadolint** to scan for vulnerabilities and other issues in Dockerfiles
  - Run **Gitleaks** to scan for committed secrets
