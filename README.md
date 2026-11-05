<h1 align="center">Vadim Bykov</h1>

<p align="center">
  <b>DevOps Tech Lead</b> · 10+ years in IT, 7+ in DevOps
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=2000&color=1E9E96&center=true&vCenter=true&width=720&height=40&lines=I+love+it+when+things+just+work.;CI%2FCD+%C2%B7+Infrastructure+as+Code+%C2%B7+Kubernetes+%26+GitOps" alt="I love it when things just work." />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/vadik-bkv"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square" alt="LinkedIn" /></a>
  <a href="mailto:vadim_bkv@yahoo.com"><img src="https://img.shields.io/badge/Email-vadim__bkv%40yahoo.com-555555?style=flat-square" alt="Email: vadim_bkv@yahoo.com" /></a>
</p>

I work at [Silk Data](https://github.com/SilkData), a machine-learning R&D company. Most of my work is CI/CD pipelines and the infrastructure under them: Jenkins, GitLab CI, Terraform, Ansible and Kubernetes. I started as a sysadmin in 2013, moved to DevOps in 2018 and have led and mentored a team of two engineers.

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/pipeline/dark-narrow.svg?v=5">
  <source media="(max-width: 600px)" srcset="./assets/pipeline/light-narrow.svg?v=5">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/pipeline/dark-vertical.svg?v=5">
  <img src="./assets/pipeline/light-vertical.svg?v=5" alt="Delivery pipeline. Commit. Build and test, with build, lint, unit tests and a secret scan in parallel. Package: the artifact goes to a registry. Provision: plan and apply create or change the servers. Deploy: a rolling update onto those servers. Observe runs 24/7 and alerts the on-call SRE or DevOps engineer; fixes come back as commits. Tools: Git, GitLab, GitHub, Jenkins, GitLab CI, GitHub Actions, Docker, Harbor, Nexus, Terraform on AWS, Azure, GCP and Hetzner, Ansible, Helm, Argo CD, Prometheus, Grafana, Zabbix, Wazuh." width="100%">
</picture>

<sub>How the pipelines I build usually look. On the right are the tools I've used for each step in production.</sub>

## Selected work

<sub>Each title opens a page with the details and a diagram.</sub>

### [Media CMS](projects/media-cms.md)
<sub>Microservices behind a high-traffic media portal</sub>

I run the delivery pipelines for all environments and I'm building a new cloud production environment for it, fully described in code.

### [Legacy servers of the same portal](projects/legacy-servers.md)
<sub>Incident response and security</sub>

Brought server load from ~85 down to under 7 during a bot-driven incident, contained a critical remote code execution bug on a runtime that could not be patched, and moved the origin behind the CDN step by step with zero downtime.

### [Cross-platform product](projects/cross-platform-product.md)
<sub>Backend, web and mobile apps · since 2018</sub>

I moved the legacy backend from plain servers to a managed container platform in the cloud, back when that was not yet the usual move: containerized the app, moved file storage to object storage and the database to a managed service. The big processing servers started only when a task landed in the queue and shut down after, which kept the cloud bill low from day one. Build and release pipelines cover every part, including the mobile apps and their distribution outside the app stores.

### [Enterprise product](projects/enterprise-product.md)
<sub>Release builds, security checks, testing on four database engines</sub>

One pipeline builds the release, others audit dependencies and rebuild the antivirus image. Every release is also tested on four database engines: a production-like dump, the migration, and a check that the server comes up.

### [Company infrastructure](projects/company-infrastructure.md)
<sub>Servers as code</sub>

All internal and client servers are described in code, each with its own firewall. One pipeline brings any new server to the same secure, monitored baseline.

### [Anti-plagiarism SaaS](projects/anti-plagiarism-saas.md)
<sub>Demo environments on request</sub>

A prospect clicks "Request a demo" on the landing page. After a quick approval, one pipeline builds a complete environment for them from scratch: cloud server, security baseline, monitoring and all six services behind a proxy with TLS.

### [EdTech platform](projects/edtech-platform.md)
<sub>From a broken pipeline to stable cloud releases</sub>

There was no DevOps: the existing pipeline didn't work and the app wouldn't build in a container. I reviewed and refactored the whole delivery setup, which gave stable pipelines and cloud releases with managed configuration. Then I moved the servers to ARM to cut the cloud bill.

## Stack

| Area | Tools |
|---|---|
| CI/CD & GitOps | <img src="./assets/icons/jenkins.svg?v=5" alt="Jenkins" title="Jenkins" width="40" height="40">&nbsp;<img src="./assets/icons/gitlab.svg?v=5" alt="GitLab CI" title="GitLab CI" width="40" height="40">&nbsp;<img src="./assets/icons/github-actions.svg?v=5" alt="GitHub Actions" title="GitHub Actions" width="40" height="40">&nbsp;<img src="./assets/icons/argo-cd.svg?v=5" alt="Argo CD" title="Argo CD" width="40" height="40"> |
| IaC & Config | <img src="./assets/icons/terraform.svg?v=5" alt="Terraform" title="Terraform" width="40" height="40">&nbsp;<img src="./assets/icons/ansible.svg?v=5" alt="Ansible" title="Ansible" width="40" height="40">&nbsp;<img src="./assets/icons/helm.svg?v=5" alt="Helm" title="Helm" width="40" height="40">&nbsp;<img src="./assets/icons/infracost.svg?v=5" alt="Infracost" title="Infracost" width="40" height="40"> |
| Containers | <img src="./assets/icons/docker.svg?v=5" alt="Docker" title="Docker" width="40" height="40">&nbsp;<img src="./assets/icons/docker-compose.svg?v=5" alt="Docker Compose" title="Docker Compose" width="40" height="40">&nbsp;<img src="./assets/icons/docker-swarm.svg?v=5" alt="Docker Swarm" title="Docker Swarm" width="40" height="40">&nbsp;<img src="./assets/icons/kubernetes.svg?v=5" alt="Kubernetes" title="Kubernetes" width="40" height="40">&nbsp;<img src="./assets/icons/diun.svg?v=5" alt="Diun" title="Diun" width="40" height="40"> |
| Cloud | <img src="./assets/icons/aws.svg?v=5" alt="AWS" title="AWS" width="40" height="40">&nbsp;<img src="./assets/icons/azure.svg?v=5" alt="Azure" title="Azure" width="40" height="40">&nbsp;<img src="./assets/icons/gcp.svg?v=5" alt="Google Cloud" title="Google Cloud" width="40" height="40">&nbsp;<img src="./assets/icons/hetzner.svg?v=5" alt="Hetzner" title="Hetzner" width="40" height="40">&nbsp;<img src="./assets/icons/akamai.svg?v=5" alt="Linode / Akamai" title="Linode / Akamai" width="40" height="40"> |
| Observability | <img src="./assets/icons/prometheus.svg?v=5" alt="Prometheus" title="Prometheus" width="40" height="40">&nbsp;<img src="./assets/icons/grafana.svg?v=5" alt="Grafana" title="Grafana" width="40" height="40">&nbsp;<img src="./assets/icons/zabbix.svg?v=5" alt="Zabbix" title="Zabbix" width="40" height="40">&nbsp;<img src="./assets/icons/elasticsearch.svg?v=5" alt="ELK" title="ELK" width="40" height="40">&nbsp;<img src="./assets/icons/sentry.svg?v=5" alt="Sentry" title="Sentry" width="40" height="40">&nbsp;<img src="./assets/icons/dozzle.svg?v=5" alt="Dozzle" title="Dozzle" width="40" height="40"> |
| Security | <img src="./assets/icons/wazuh.svg?v=5" alt="Wazuh" title="Wazuh" width="40" height="40">&nbsp;<img src="./assets/icons/defectdojo.svg?v=5" alt="DefectDojo" title="DefectDojo" width="40" height="40"> |
| Edge & Networking | <img src="./assets/icons/nginx.svg?v=5" alt="Nginx" title="Nginx" width="40" height="40">&nbsp;<img src="./assets/icons/traefik.svg?v=5" alt="Traefik" title="Traefik" width="40" height="40">&nbsp;<img src="./assets/icons/cloudflare.svg?v=5" alt="Cloudflare" title="Cloudflare" width="40" height="40">&nbsp;<img src="./assets/icons/fastly.svg?v=5" alt="Fastly" title="Fastly" width="40" height="40">&nbsp;<img src="./assets/icons/wireguard.svg?v=5" alt="WireGuard" title="WireGuard" width="40" height="40"> |
| OS & Scripting | <img src="./assets/icons/linux.svg?v=5" alt="Linux" title="Linux" width="40" height="40">&nbsp;<img src="./assets/icons/bash.svg?v=5" alt="Bash" title="Bash" width="40" height="40"> |
| Collaboration | <img src="./assets/icons/jira.svg?v=5" alt="Jira" title="Jira" width="40" height="40">&nbsp;<img src="./assets/icons/slack.svg?v=5" alt="Slack" title="Slack" width="40" height="40">&nbsp;<img src="./assets/icons/teams.svg?v=5" alt="Microsoft Teams" title="Microsoft Teams" width="40" height="40"> |
| AI | <img src="./assets/icons/claude-code.svg?v=5" alt="Claude Code" title="Claude Code" width="40" height="40"> |

<sub>Jenkins and Ansible run most of my deploys, GitLab CI builds the mobile apps, Terraform covers AWS, Azure, GCP and Hetzner. For new Kubernetes environments I use Helm and Argo CD. Monitoring and security: Prometheus, Grafana, Zabbix, ELK, Sentry, Wazuh and DefectDojo. Icons from [skill-icons](https://github.com/tandpfun/skill-icons) (MIT) and [Simple Icons](https://simpleicons.org) (CC0); Dozzle, DefectDojo, Diun and Docker Compose logos from their own repositories.</sub>

---

<p align="center">
  <a href="https://www.linkedin.com/in/vadik-bkv">LinkedIn</a> ·
  <a href="mailto:vadim_bkv@yahoo.com">vadim_bkv@yahoo.com</a>
</p>
