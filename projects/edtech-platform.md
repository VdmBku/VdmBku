# EdTech platform

<sub>From a broken pipeline to stable cloud releases</sub>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/edtech-release/dark-narrow.svg?v=3">
  <source media="(max-width: 600px)" srcset="../assets/edtech-release/light-narrow.svg?v=3">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/edtech-release/dark.svg?v=3">
  <img src="../assets/edtech-release/light.svg?v=3" alt="A release: pick component versions, dry run, deploy to a cloud stage with Terraform and Ansible, check it, then roll the same release out to about 20 client servers on-prem." width="100%">
</picture>

## Where it started

The platform (Moodle, a student information system and single sign-on) had no DevOps. The existing deployment pipeline didn't work, and Moodle wouldn't build in a container.

## What I did

I reviewed and refactored the whole delivery setup:

- **Images.** Moodle and the other components build in Docker on a current Ubuntu base instead of an old CentOS one.
- **Pipelines.** Jenkins and Terraform create single-node and multi-node environments on Azure. Environment, VM size and the version of every component are parameters, and a dry-run mode checks a change before it touches anything.
- **Configuration.** Ansible installs and configures each component, with configs managed per environment instead of edited on servers.
- **Security and upkeep.** Automatic security updates, antivirus scanning, web server security headers and IP allow-lists, log rotation.
- **Local environments.** Vagrant boxes so changes can be tried before they reach the cloud.
- **Kubernetes proof of concept.** The whole stack on AKS with managed storage, a managed MySQL server and Key Vault.

Then I moved the servers to ARM to cut the cloud bill.

## Releases

A release goes to a stage environment in the cloud first. Once it is checked, the same release goes to about 20 client servers on-prem. That is a Jenkins job with Ansible: you pick the code versions, the domain and the web server flavor, and switch each component (Moodle, CAS, the SIS parts, post-install steps) on or off for that client.

**Tools:** Jenkins, Terraform, Azure, Ansible, Docker, Vagrant, Kubernetes (AKS).

[Back to profile](../README.md)
