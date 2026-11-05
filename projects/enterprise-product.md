# Enterprise product

<sub>Release builds, security checks and release testing on four database engines</sub>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/enterprise-build/dark-narrow.svg?v=3">
  <source media="(max-width: 600px)" srcset="../assets/enterprise-build/light-narrow.svg?v=3">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/enterprise-build/dark.svg?v=3">
  <img src="../assets/enterprise-build/light.svg?v=3" alt="Release build: checkout, three web front-ends, server tests cached per commit, server JAR with the bundles inside, Docker image, deploy with Ansible. Dependency audit: npm audit on four front-ends, a gate that fails on high severity, archived reports. Antivirus service: keep the previous image for rollback, build the ClamAV image, push, deploy with Ansible." width="100%">
</picture>

A Java server product with three web front-ends, which customers run on their own database: PostgreSQL, Oracle, MariaDB or MySQL.

## Release build

One Jenkins pipeline builds a release. The three front-ends (the admin UI, the SDK bundles and the embed script) are built with npm and stamped with the release version. The server is tested and then built into a JAR with those bundles inside, so one artifact carries the whole product. The JAR becomes a Docker image, and Ansible deploys it to the target you pick. Server tests are skipped when the same commit already passed them in the previous build.

## Dependency audit

A separate pipeline runs `npm audit` on all four front-end projects, archives the reports and fails if any of them has a high-severity finding.

## Antivirus service

The product runs its own ClamAV service. Its image has its own pipeline: the current image is tagged as `previous` first, so a rollback is one tag away, then the new image is built, pushed and deployed with Ansible.

## The release check on four databases

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/db-matrix/dark-narrow.svg?v=3">
  <source media="(max-width: 600px)" srcset="../assets/db-matrix/light-narrow.svg?v=3">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/db-matrix/dark.svg?v=3">
  <img src="../assets/db-matrix/light.svg?v=3" alt="A new release is checked on PostgreSQL, Oracle, MariaDB and MySQL one after another. For each engine: database up, build and tests, restore dump, migrate, server up. When all four pass, the release is OK." width="100%">
</picture>

A release that works on one engine can still break a migration on another. One parameterized Jenkins pipeline runs the same check on every engine, one after another:

1. **DB up.** Ansible starts a fresh database container for the engine.
2. **Build + tests.** The server is built with that engine's profile and its unit tests run against it.
3. **Restore dump.** A production-like dump is loaded, so the migration meets real data, not an empty schema.
4. **Migrate.** The new server image starts and migrates the schema.
5. **Server up.** The pipeline waits for the service info endpoint to answer.

Each engine can be switched off for a quick run, the Oracle volume can be recreated from scratch, the whole run has a time limit, and a failure sends an email with the link to the build.

## Around it

Acceptance tests run in their own pipeline, and a Helm chart covers Kubernetes installs. Deployments to each customer's environment go through Ansible.

**Tools:** Jenkins, Ansible, Docker, Maven, npm, ClamAV, PostgreSQL, Oracle, MariaDB, MySQL, Helm.

[Back to profile](../README.md)
