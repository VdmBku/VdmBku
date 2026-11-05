<h1 align="center">Vadim Bykov</h1>

<p align="center">
  <b>DevOps Tech Lead</b> · 10+ years in IT, 7+ in DevOps
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=2000&color=1E9E96&center=true&vCenter=true&width=600&height=40&lines=I+love+it+when+things+just+work.;CI%2FCD+%C2%B7+Infrastructure+as+Code+%C2%B7+Kubernetes+%26+GitOps" alt="I love it when things just work." />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/vadik-bkv"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square" alt="LinkedIn" /></a>
  <a href="mailto:vadim_bkv@yahoo.com"><img src="https://img.shields.io/badge/Email-vadim__bkv%40yahoo.com-555555?style=flat-square" alt="Email: vadim_bkv@yahoo.com" /></a>
</p>

I work at [Silk Data](https://github.com/SilkData), a machine-learning R&D company. Most of my work is CI/CD pipelines and the infrastructure under them: Jenkins, GitLab CI, Terraform, Ansible and Kubernetes. I started as a sysadmin in 2013, moved to DevOps in 2018 and have led and mentored a team of two engineers.

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/pipeline/dark-narrow.svg">
  <source media="(max-width: 600px)" srcset="./assets/pipeline/light-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/pipeline/dark.svg">
  <img src="./assets/pipeline/light.svg" alt="Delivery pipeline in six steps. Commit: Git, GitLab, GitHub. Build and test: Jenkins, GitLab CI, GitHub Actions. Package: Docker, Harbor, Nexus. Provision: Terraform on AWS, Azure, GCP and Hetzner. Deploy: Ansible, Helm, Argo CD. Observe: Prometheus, Grafana, Zabbix, Wazuh. Metrics and alerts loop back to the next change." width="100%">
</picture>

<sub>How the pipelines I build usually look. The names under each step are the tools I've used for it in production.</sub>

## What I work on

**Media CMS on GCP.** 11 microservice repos behind a high-traffic media portal. Jenkins and Ansible deploy them with Docker and Traefik to dev, stage and prod. Right now I'm building a second production environment for it on GKE Autopilot with Terraform, Helm and Argo CD.

**Cross-platform product on Azure AKS.** Backend microservices, web, Android and iOS. Jenkins and Ansible build and release the backend into a private registry, GitLab CI builds the mobile apps on a self-hosted Mac mini, and our own OTA server ships the apps outside Google Play and the App Store.

**Anti-plagiarism SaaS** <sub>(part-time, 2024-2025)</sub>. One parameterized Jenkins pipeline creates a whole environment on Hetzner with Terraform, hardens the servers with Ansible (SSH baseline, Wazuh, Zabbix) and deploys 6+ services behind Traefik with automatic TLS.

**EdTech platform** <sub>(part-time, 2023-2025)</sub>. Deployment used to be manual. I replaced it with idempotent Ansible for Moodle, SIS, CAS SSO and Redis, added Terraform and Jenkins pipelines on Azure, and moved the stack from CentOS to Ubuntu.

## Tools I use

<p>
  <img src="./assets/icons/jenkins.svg" alt="Jenkins" width="40" height="40">&nbsp;
  <img src="./assets/icons/gitlab.svg" alt="GitLab CI" width="40" height="40">&nbsp;
  <img src="./assets/icons/github-actions.svg" alt="GitHub Actions" width="40" height="40">&nbsp;
  <img src="./assets/icons/argo-cd.svg" alt="Argo CD" width="40" height="40">&nbsp;
  <img src="./assets/icons/terraform.svg" alt="Terraform" width="40" height="40">&nbsp;
  <img src="./assets/icons/ansible.svg" alt="Ansible" width="40" height="40">&nbsp;
  <img src="./assets/icons/helm.svg" alt="Helm" width="40" height="40">&nbsp;
  <img src="./assets/icons/docker.svg" alt="Docker" width="40" height="40">&nbsp;
  <img src="./assets/icons/kubernetes.svg" alt="Kubernetes" width="40" height="40">
</p>
<p>
  <img src="./assets/icons/aws.svg" alt="AWS" width="40" height="40">&nbsp;
  <img src="./assets/icons/azure.svg" alt="Azure" width="40" height="40">&nbsp;
  <img src="./assets/icons/gcp.svg" alt="Google Cloud" width="40" height="40">&nbsp;
  <img src="./assets/icons/hetzner.svg" alt="Hetzner" width="40" height="40">&nbsp;
  <img src="./assets/icons/prometheus.svg" alt="Prometheus" width="40" height="40">&nbsp;
  <img src="./assets/icons/grafana.svg" alt="Grafana" width="40" height="40">&nbsp;
  <img src="./assets/icons/elasticsearch.svg" alt="ELK" width="40" height="40">&nbsp;
  <img src="./assets/icons/nginx.svg" alt="Nginx" width="40" height="40">&nbsp;
  <img src="./assets/icons/traefik.svg" alt="Traefik" width="40" height="40">&nbsp;
  <img src="./assets/icons/cloudflare.svg" alt="Cloudflare" width="40" height="40">&nbsp;
  <img src="./assets/icons/linux.svg" alt="Linux" width="40" height="40">&nbsp;
  <img src="./assets/icons/bash.svg" alt="Bash" width="40" height="40">
</p>

<sub>Jenkins and Ansible run most of my deploys, GitLab CI builds the mobile apps, Terraform covers AWS, Azure, GCP and Hetzner. For new Kubernetes environments I use Helm and Argo CD. Monitoring and security: Prometheus, Grafana, Zabbix, ELK and Wazuh. Icons from [skill-icons](https://github.com/tandpfun/skill-icons) (MIT) and [Simple Icons](https://simpleicons.org) (CC0).</sub>

---

<p align="center">
  <a href="https://www.linkedin.com/in/vadik-bkv">LinkedIn</a> ·
  <a href="mailto:vadim_bkv@yahoo.com">vadim_bkv@yahoo.com</a>
</p>
