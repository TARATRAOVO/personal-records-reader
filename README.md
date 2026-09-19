# Personal records: agent-readable mirror

Site: https://taratraovo.github.io/personal-records-reader/

This repository contains only exporter code and synthetic tests. The user has explicitly chosen to publish their records without a password. Actual record snapshots are fetched from the existing public read-only API during deployment; they are never committed to Git. Deployment artifacts are deleted after deployment (a one-day expiration also applies). Public readers and caches can still retain copies of public content.

The site has initial HTML, JSON and plain text, complete category pages, and pre-generated daily pages. No JavaScript or login is needed. Query parameters do not filter the static site. Read `llms.txt` for units, timestamps, provenance and missing-data limitations. Book progress is a current snapshot, not a historical series.

Refreshes are scheduled every 15 minutes, subject to GitHub Actions scheduling delays. Failed downloads or validation retain the previous published site. Always check `generatedAt` and source observation times. A monthly maintenance commit containing only the month keeps this public repository active so scheduled workflows are not disabled after inactivity.

Run `python3 -m unittest -v`, then `python3 export.py`. Generated `_site/` is ignored by Git. No server credentials are needed. Writes still go directly from the clients to the existing authenticated backend.
