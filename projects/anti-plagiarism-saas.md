# Anti-plagiarism SaaS

<sub>Demo environments on request</sub>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/demo-flow/dark-narrow.svg?v=8">
  <source media="(max-width: 600px)" srcset="../assets/demo-flow/light-narrow.svg?v=8">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/demo-flow/dark.svg?v=8">
  <img src="../assets/demo-flow/light.svg?v=8" alt="Request a demo, then seven automated steps: approve, pipeline, server and DNS, hardening, proxy and TLS, six service releases one by one, ready with access sent." width="100%">
</picture>

## From a button to a running environment

A prospect fills in name, email and company and clicks "Request a demo" on the landing page. The form starts a parameterized Jenkins job remotely. After a quick manual approval, one pipeline builds a complete environment for them from scratch:

1. **Pipeline.** Checks out the infrastructure code and the release branch of each service.
2. **Server + DNS.** Terraform creates a server on Hetzner Cloud in the project of the chosen environment, sized by a parameter, with its DNS records. The plan and outputs are archived with the build.
3. **Hardening.** The Ansible inventory is built from the Terraform output. The server gets an SSH baseline, a host intrusion detection agent, a monitoring agent, a separate data volume and a technical user with least privilege.
4. **Proxy + TLS.** Traefik in front of everything, with certificates issued automatically.
5. **6 service releases.** Each service is released on its own, one after another: API gateway, web app, the anti-plagiarism engine, chat detector, search integration and text extractor. Each one is built from its own release branch and deployed in its own container.
6. **Ready.** The team gets a build card in Microsoft Teams, and the prospect gets access.

A dry-run mode validates the pipeline after changes, and a separate pipeline tears an environment down.

**Tools:** Jenkins, Terraform, Hetzner Cloud, Ansible, Docker, Traefik, Wazuh, Zabbix, Microsoft Teams.

[Back to profile](../README.md)
