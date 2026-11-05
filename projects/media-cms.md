# Media CMS

<sub>Microservices behind a high-traffic media portal</sub>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/media-gitops/dark-narrow.svg?v=8">
  <source media="(max-width: 600px)" srcset="../assets/media-gitops/light-narrow.svg?v=8">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/media-gitops/dark.svg?v=8">
  <img src="../assets/media-gitops/light.svg?v=8" alt="Every branch of ten services is built into images, with no deploy from CI. A release tag is promoted to the production registry and pinned in Git. Argo CD, as an app of apps, syncs platform components, stateful services and the ten services into GKE Autopilot." width="100%">
</picture>

## The new platform

I'm moving the CMS to Kubernetes on GKE Autopilot, with GitOps from the start. Terraform creates the cluster and everything around it. Staging already runs there, and production is moving over.

## Build: CI never deploys

Each of the ten services has its own multibranch Jenkins pipeline. It builds the images for every branch with Ansible and pushes them to the development registry, and that's all it does. A release tag is promoted to the production registry by a script that also keeps image names consistent across services.

## Deploy: a commit

One Git repository describes the whole cluster. A root Argo CD application (app of apps) creates three ApplicationSets:

- **Platform:** Argo CD itself, External Secrets, the ingress on the Gateway API, a MongoDB operator and monitoring, one Helm release per folder.
- **Stateful:** Redis, TimescaleDB and a MongoDB replica set per environment.
- **Services:** the ten services, each a Helm chart with a values file per environment.

To deploy, you pin the image tag in the environment's values file and commit. Argo CD syncs with prune and self-heal, so the cluster always matches Git.

## One library chart for the boring parts

Every service chart depends on a shared library chart: secrets from the cloud secret manager through External Secrets, HTTP routes and health checks for the Gateway API, metrics scraping, the workload service account and vertical pod autoscaling. A new service gets all of that by adding one dependency. Database migrations ship inside the chart as a Kubernetes Job.

## Today

Until the switch, production runs as before: Jenkins with Ansible deploys the services in Docker behind Traefik, through dev, stage and prod, with a managed SQL database and a message queue from the same cloud.

**Tools:** Jenkins, Ansible, Docker, Traefik, Terraform, Google Cloud (GKE Autopilot, Artifact Registry, Secret Manager, Cloud SQL, Pub/Sub), Argo CD, Helm, External Secrets, Gateway API.

[Back to profile](../README.md)
