# Personal records: agent-readable mirror

Site: https://taratraovo.github.io/personal-records-reader/

This repository contains only exporter code and synthetic tests. The user has explicitly chosen to publish their records without a password. Actual record snapshots are fetched from the existing public read-only API during deployment; they are never committed to Git. Deployment artifacts are deleted after deployment (a one-day expiration also applies). Public readers and caches can still retain copies of public content.

The site has initial HTML, JSON and plain text, complete category pages, and pre-generated daily pages. No JavaScript or login is needed. Query parameters do not filter the static site. Read `llms.txt` for units, timestamps, provenance and missing-data limitations. Book progress is a current snapshot, not a historical series.

The source server checks public data every 10 seconds, batches changes for 20 seconds, and triggers at most once every 2 minutes. It pushes only `.refresh.json` (a request timestamp and generic reason) using a dedicated deploy key scoped to this repository. Measured-value changes and deletions trigger updates; sampling timestamp changes alone do not. Failed pushes retry and preserve pending changes across process restarts. No personal record content or account token is committed.

Refreshes also remain scheduled every 15 minutes as fallback, subject to GitHub Actions scheduling delays. Builds and CDN caching add delay: this is not a live API. Failed downloads or validation retain the previous published site. Always check `generatedAt` and source observation times. A monthly maintenance commit containing only the month keeps this public repository active so scheduled workflows are not disabled after inactivity.

Run `python3 -m unittest -v`, then `python3 export.py`. Generated `_site/` is ignored by Git. No server credentials are needed. Writes still go directly from the clients to the existing authenticated backend.
