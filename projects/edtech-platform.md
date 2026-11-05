# EdTech platform

<sub>From a broken pipeline to stable cloud releases</sub>

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

**Tools:** Jenkins, Terraform, Azure, Ansible, Docker, Vagrant, Kubernetes (AKS).

[Back to profile](../README.md)
