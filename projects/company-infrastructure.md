# Company infrastructure

<sub>Servers as code</sub>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/company-infra/dark-narrow.svg?v=1">
  <source media="(max-width: 600px)" srcset="../assets/company-infra/light-narrow.svg?v=1">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/company-infra/dark.svg?v=1">
  <img src="../assets/company-infra/light.svg?v=1" alt="A Terraform server module creates every server on Hetzner Cloud with its own firewall, a primary IP and a private network attachment. Internal services and each client project are separate stacks. A new server then goes through one Jenkins pipeline with Ansible: the inventory is built at run time, secrets come from Ansible Vault, and each part (Docker, log rotation, security updates, fail2ban, the Zabbix and Wazuh agents, hardening, users) is switched on or off for the run, until the server reaches the same baseline as the rest." width="100%">
</picture>

## Every server described in code

All internal and client servers on Hetzner Cloud are described in Terraform. One reusable server module creates the server, its own firewall, a primary IP and the private network attachment, so no server shares firewall rules with another by accident. Internal services and each client project live in separate stacks: CI masters and workers (including ARM), the Git server and its runner, the image registry, monitoring, security monitoring, logging and file sharing.

## One baseline for every new server

A Jenkins pipeline with Ansible brings any new server to the same state:

- Docker, log rotation, unattended security updates and fail2ban,
- monitoring and security agents,
- hardening: SSH, audit, file integrity checks, AppArmor,
- user management through a simple form in Jenkins.

Each part can be switched on or off per run, the inventory is generated at build time, secrets live in Ansible Vault, and the pipeline itself is released in versions. My team and I built and run it.

**Tools:** Terraform, Hetzner Cloud, Jenkins, Ansible, Ansible Vault, Docker, Zabbix, Wazuh.

[Back to profile](../README.md)
