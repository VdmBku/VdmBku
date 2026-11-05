# Media CMS

<sub>Microservices behind a high-traffic media portal</sub>

## Today

The CMS is eleven microservice repositories. Jenkins with Ansible builds and deploys each of them: images go to the cloud's artifact registry, services run in Docker behind Traefik, and every change moves through dev, stage and prod. The services use a managed SQL database and a message queue from the same cloud.

## Next

I'm building a second production environment next to the current one, fully described in code:

- Terraform creates the cluster on GKE Autopilot and everything around it,
- every service is packaged as a Helm chart,
- Argo CD keeps the cluster in sync with Git, so a deploy is a commit.

**Tools:** Jenkins, Ansible, Docker, Traefik, Google Cloud (Artifact Registry, Cloud SQL, Pub/Sub, GKE Autopilot), Terraform, Helm, Argo CD.

[Back to profile](../README.md)
