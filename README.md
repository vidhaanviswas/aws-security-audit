# AWS Security Misconfiguration Audit  Gauntlet Assignment

## Author: Vidhaan Viswas
## Role Applied: Python Developer & Testing Intern

---

##  Overview

This project is a Python-based AWS security audit tool built using the `boto3` SDK.  
It checks for misconfigurations in:

- Amazon S3
- Amazon RDS
- EC2 Security Groups

The script performs **read-only** operations and requires valid AWS credentials configured via `aws configure`.

---

##  Features Implemented

### S3 Audit
- Detect publicly accessible buckets
- Detect buckets with logging disabled
- Detect buckets with versioning disabled

### RDS Audit
- Detect public RDS instances
- Detect missing delete protection
- Detect backups disabled

### Security Group Audit
- Detect SSH (22) open to world
- Detect MongoDB (27017) open to world

---

##  How to Run

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure AWS credentials:
```bash
aws configure
```

### 3. Run the audit:
```bash
python aws_security_audit.py
```

🧪 Running Tests (pytest)
```bash
pytest
```

📝 Optional Report
### A sample vulnerability report is included under:

- report/vulnerability_report.pdf
