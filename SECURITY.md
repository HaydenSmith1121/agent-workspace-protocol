# Security

## Never Commit Real Secrets

This project includes workspace templates. Do not put real credentials,
customer data, private endpoints, or private repository paths in:

- `README.md` or any documentation page;
- skill references;
- example configuration;
- issues, pull requests, or discussion comments.

If a secret is committed, rotate it first, then remove it from history.
Deleting the file in a later commit is not enough.

## Reporting a Problem

Open a private security advisory on the GitHub repository when available. If
that is not possible, contact the maintainer through the repository's listed
contact method. Do not publish exploit details or live credentials in a
public issue.
