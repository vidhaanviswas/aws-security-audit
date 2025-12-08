# AWS Security Misconfiguration Audit  Gauntlet Assignment

Author: Vidhaan Viswas  
Role Applied: Python Developer & Testing Intern

---

## Overview

A small, read-only Python tool that scans an AWS account for common misconfigurations in:
- Amazon S3 (public buckets, logging, versioning)
- Amazon RDS (public instances, deletion protection, backups)
- EC2 Security Groups (SSH/MongoDB open to the world, IPv6 ::/0)

The checks use the `boto3` SDK and perform only read operations. Configure AWS credentials before running.

---

## Prerequisites

- Python 3.8+ installed
- AWS credentials configured (via `aws configure` or environment variables)

---

## Install

Windows PowerShell (recommended):

```powershell
# create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

Or (platform-agnostic):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

By default the script sets `AWS_REGION` at the top of `aws_security_audit.py`. You can edit that value or rely on your environment/AWS configuration.

Run the audit:

```bash
python aws_security_audit.py
```

Expected output is printed to stdout and indicates `OK` or `[MISCONFIG]` for each check.

---

## Running Tests

The project includes pytest-based tests that mock AWS clients. Run them with:

```bash
pytest -q
```

---

## Project Structure

```
aws_security_audit.py        # Main audit script
requirements.txt             # Dependencies (boto3, pytest)
README.md                    # This file
tests/                       # Unit tests (mock-based)
report/                      # Vulnerability report (PDF)
```

---

## Notes

- The tool uses a simple, heuristic-based approach to detect common misconfigurations. It is not exhaustive.
- Ensure credentials used have **read-only** permissions where possible.
- If you want the script to use a different region without editing the file, either set `AWS_DEFAULT_REGION` in the environment or modify the `AWS_REGION` variable in the script.

---

## Screenshots

You can include screenshots of the script output or test runs to make results easy to review.

- Suggested locations for screenshots (create the directories if needed):
  - `report/screenshots/scan_output.png`  screenshot of `python aws_security_audit.py` output
  - `report/screenshots/tests_output.png`  screenshot of `pytest -q` output

- Quick way to capture textual output if you prefer a plain file instead of an image:
  - Run the audit and save output to a text file:

```bash
python aws_security_audit.py > report/scan_output.txt
```

  - Run tests and save output:

```bash
pytest -q > report/tests_output.txt
```


