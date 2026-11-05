# Company infrastructure

<sub>Servers as code</sub>

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
