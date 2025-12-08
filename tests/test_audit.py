import os
import sys
import pytest

# Add project root (folder containing aws_security_audit.py) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import aws_security_audit as audit

# ---------- S3 TESTS ----------

def test_s3_audit_detects_public_bucket(monkeypatch, capsys):
    """
    Ensure that a public bucket is reported correctly and that
    logging/versioning disabled are also flagged.
    """

    class MockS3Client:
        def list_buckets(self):
            return {
                "Buckets": [
                    {"Name": "aws-test-bucket-vidhaan"}
                ]
            }

        def get_bucket_acl(self, Bucket):
            # Simulate public ACL (AllUsers)
            return {
                "Grants": [
                    {
                        "Grantee": {
                            "URI": "http://acs.amazonaws.com/groups/global/AllUsers"
                        }
                    }
                ]
            }

        def get_bucket_logging(self, Bucket):
            # No LoggingEnabled key => logging disabled
            return {}

        def get_bucket_versioning(self, Bucket):
            # Status not "Enabled" => versioning disabled
            return {"Status": "Suspended"}

    # Patch the global s3 client in the script
    monkeypatch.setattr(audit, "s3", MockS3Client())

    audit.check_s3_buckets()
    captured = capsys.readouterr().out

    # Check expected strings in the output
    assert "aws-test-bucket-vidhaan" in captured
    assert "Publicly accessible" in captured or "[MISCONFIG]" in captured
    assert "logging disabled" in captured or "Logging is DISABLED" in captured
    assert "versioning disabled" in captured or "Versioning is DISABLED" in captured


# ---------- RDS TESTS ----------

def test_rds_audit_detects_public_rds(monkeypatch, capsys):
    """
    Ensure that a publicly accessible RDS instance with no backups
    and no delete protection is reported correctly.
    """

    class MockRDSClient:
        def describe_db_instances(self):
            return {
                "DBInstances": [
                    {
                        "DBInstanceIdentifier": "test-rds-vidhaan",
                        "PubliclyAccessible": True,
                        "DeletionProtection": False,
                        "BackupRetentionPeriod": 0,
                    }
                ]
            }

    monkeypatch.setattr(audit, "rds", MockRDSClient())

    audit.check_rds_instances()
    captured = capsys.readouterr().out

    assert "test-rds-vidhaan" in captured
    # any of these variants depending on how you print
    assert "publicly accessible" in captured.lower()
    assert "delete protection" in captured.lower()
    assert "backup" in captured.lower()


# ---------- SECURITY GROUP TESTS ----------

def test_sg_audit_detects_public_ssh_and_mongo(monkeypatch, capsys):
    """
    Ensure that a security group with SSH (22) and MongoDB (27017)
    open to 0.0.0.0/0 is flagged.
    """

    class MockEC2Client:
        def describe_security_groups(self):
            return {
                "SecurityGroups": [
                    {
                        "GroupId": "sg-0284e10343c655497",
                        "GroupName": "insecure-sg-vidhaan",
                        "IpPermissions": [
                            {
                                "FromPort": 22,
                                "ToPort": 22,
                                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                                "Ipv6Ranges": []
                            },
                            {
                                "FromPort": 27017,
                                "ToPort": 27017,
                                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                                "Ipv6Ranges": []
                            }
                        ]
                    }
                ]
            }

    monkeypatch.setattr(audit, "ec2", MockEC2Client())

    audit.check_security_groups()
    captured = capsys.readouterr().out

    # depending on your exact print format, adjust text:
    assert "insecure-sg-vidhaan" in captured
    assert "22" in captured
    assert "27017" in captured
    # if you use labels like these in your output:
    assert "public SSH" in captured or "SSH (22) is open" in captured
    assert "MongoDB" in captured or "27017" in captured


# ---------- INTEGRATION STYLE TEST (OPTIONAL) ----------

def test_full_scan_runs_without_error(monkeypatch, capsys):
    """
    Optional: sanity test that the main scan can run with mocked clients
    without raising exceptions.
    """

    class MockS3Client:
        def list_buckets(self):
            return {"Buckets": []}

        def get_bucket_acl(self, Bucket):
            return {"Grants": []}

        def get_bucket_logging(self, Bucket):
            return {}

        def get_bucket_versioning(self, Bucket):
            return {}

    class MockRDSClient:
        def describe_db_instances(self):
            return {"DBInstances": []}

    class MockEC2Client:
        def describe_security_groups(self):
            return {"SecurityGroups": []}

    monkeypatch.setattr(audit, "s3", MockS3Client())
    monkeypatch.setattr(audit, "rds", MockRDSClient())
    monkeypatch.setattr(audit, "ec2", MockEC2Client())

    # If you have a `main()` function that calls all checks, use that.
    # Otherwise just call the three functions.
    if hasattr(audit, "main"):
        audit.main()
    else:
        audit.check_s3_buckets()
        audit.check_rds_instances()
        audit.check_security_groups()

    captured = capsys.readouterr().out
    assert "S3" in captured or "Bucket" in captured
    assert "RDS" in captured or "DB Instance" in captured
    assert "Security Group" in captured
