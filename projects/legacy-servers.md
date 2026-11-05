# Legacy servers of a media portal

<sub>Incident response and security</sub>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/legacy-lockdown/dark-narrow.svg?v=10">
  <source media="(max-width: 600px)" srcset="../assets/legacy-lockdown/light-narrow.svg?v=10">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/legacy-lockdown/dark.svg?v=10">
  <img src="../assets/legacy-lockdown/light.svg?v=10" alt="Visitors reach the origin through the CDN, while bots and scanners hit it directly. Six steps close the direct path: report-only logging, a secret header from the CDN, the client IP set by the edge, DNS moved to the CDN, 403 for anything without the secret, and a cloud firewall that lets in only the CDN and uptime checks. Uptime stays at 100% the whole time." width="100%">
</picture>

The portal's old servers run an end-of-life PHP stack behind a CDN. These are the main pieces of work on them.

## Bots and an expensive image endpoint

Server load reached ~85. Almost all slow requests were on-the-fly image resizing, and crawlers walked the image catalog so that every unique URL missed the CDN cache and hit the server.

- A disk cache for the resize endpoint: a repeat request went from 0.57 s to 0.0005 s.
- Origin shielding on the CDN, plus blocks for scraper networks and bad user agents. Search engine bots stayed allowed.

Load dropped to 2 to 7, and it no longer depends on bots.

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="../assets/legacy-load/dark-narrow.svg?v=10">
  <source media="(max-width: 600px)" srcset="../assets/legacy-load/light-narrow.svg?v=10">
  <source media="(prefers-color-scheme: dark)" srcset="../assets/legacy-load/dark.svg?v=10">
  <img src="../assets/legacy-load/light.svg?v=10" alt="Server load during the bot incident: around 85 before the cache for the image resize endpoint, 2 to 7 after it. A repeat request went from 0.57 s to 0.0005 s. Illustrative curve." width="100%">
</picture>

## A critical bug with no patch

A remote code execution bug in the PHP runtime could be triggered without logging in. The PHP version in use had no patched build, so I contained it with temporary measures instead:

- runtime settings that break the attack chain,
- request body and multipart limits in front of PHP,
- the admin backend closed behind authentication, with exceptions only for the machines that need it,
- daily read-only checks of logs, processes and code checksums, with a guard section that prints `DRIFT` if any measure goes missing.

No signs of a successful attack were found.

## Origin only behind the CDN, with zero downtime

Anyone could reach the origin directly and bypass the CDN, and the client IP header could be faked. I closed this step by step:

1. report-only logging of everything that would be refused,
2. a secret header from the CDN to the origin, and a client IP the edge sets itself,
3. short DNS TTL, then the apex and wildcard records moved to the CDN,
4. the origin refusing anything without the secret,
5. a cloud firewall that lets in only the CDN and uptime checks,
6. a daily job that alerts if the CDN's IP ranges change.

## A daily outage caused by a backup

Around lunchtime the site hung for two minutes. A database dump locked a table while the CMS wrote to it. The dump now runs only at night, retention went to 10 days, and the backup disk went from 94% to 55% full.

## How I worked

Every change was a script: check the hostname, back up the "before" state, apply, self-test, roll back automatically on failure, write a log entry on the server. Investigation was done with separate read-only scripts first.

**Tools:** nginx, PHP-FPM, Fastly, Google Cloud, Bash, Jenkins.

[Back to profile](../README.md)
