# 🛡️ AWS Security Misconfiguration Audit – Gauntlet Assignment

> **Author:** Vidhaan Viswas  
> **Role Applied:** Python Developer & Testing Intern  

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
![Status](https://img.shields.io/badge/Status-Read--Only%20Audit-success)
![AWS](https://img.shields.io/badge/AWS-boto3-orange?logo=amazonaws)
![Tests](https://img.shields.io/badge/Tests-pytest-informational?logo=pytest)


## 📌 Overview

This repository contains a **small, read-only Python tool** that scans an AWS account for common security misconfigurations in:

- **Amazon S3**
  - Publicly accessible buckets  
  - Buckets without logging  
  - Buckets without versioning  

- **Amazon RDS**
  - Publicly accessible DB instances  
  - Instances without deletion protection  
  - Instances without automated backups  

- **EC2 Security Groups**
  - SSH (`22`) open to the world  
  - MongoDB (`27017`) open to the world 

All checks are implemented using the **`boto3`** SDK and perform **only read operations**.

---

## 🧰 Tech Stack

- **Language:** Python 3.8+
- **AWS SDK:** `boto3`
- **Testing:** `pytest`
- **Environment:** Any system with Python & AWS credentials configured

---

## ✅ What the Tool Checks

| AWS Service     | Check                                      | Flagged as `[MISCONFIG]` when…                          |
|-----------------|--------------------------------------------|--------------------------------------------------------|
| **S3**          | Public access                              | Bucket is publicly accessible                          |
|                 | Logging                                    | Logging is **disabled**                                |
|                 | Versioning                                 | Versioning is **disabled**                             |
| **RDS**         | Public accessibility                       | Instance is publicly accessible                        |
|                 | Deletion protection                        | Deletion protection is **disabled**                    |
|                 | Automated backups                          | Backups are **disabled** or retention is too low       |
| **Security Groups** | SSH exposure (`22/tcp`)                | Rule allows `0.0.0.0/0` or `::/0`                       |
|                 | MongoDB exposure (`27017/tcp`)             | Rule allows `0.0.0.0/0` or `::/0`                       |

The script prints `[MISCONFIG]` for each of these checks.

---

## 🔑 Prerequisites

- **Python**: `3.8+`
- **AWS account** with **read-only credentials**
- AWS credentials configured via one of:
  - `aws configure`
  - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, optionally `AWS_DEFAULT_REGION`)
  - Any other standard AWS credential provider supported by `boto3`

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
Expected output is printed to stdout and indicates `[MISCONFIG]` for each check.
![Scan Output](report/screenshots/scan_output.png)

---

## Running Tests

The project includes pytest-based tests that mock AWS clients. Run them with:

```bash
pytest -q
```
![Tests Output](report/screenshots/pytest.png)

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


