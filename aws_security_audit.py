import boto3

# You can change this if needed
AWS_REGION = "eu-north-1"

session = boto3.Session(region_name=AWS_REGION)
s3 = session.client("s3")
rds = session.client("rds")
ec2 = session.client("ec2")


def check_s3_buckets():
    print("\n=== S3 Bucket Checks ===")
    response = s3.list_buckets()
    buckets = response.get("Buckets", [])

    if not buckets:
        print("No S3 buckets found.")
        return

    for bucket in buckets:
        name = bucket["Name"]
        print(f"\nBucket: {name}")

        # 1. Check public access (simple ACL-based check)
        is_public = False
        try:
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl.get("Grants", []):
                grantee = grant.get("Grantee", {})
                uri = grantee.get("URI", "")
                # 'AllUsers' or 'AuthenticatedUsers' means wide access
                if "AllUsers" in uri or "AuthenticatedUsers" in uri:
                    is_public = True
                    break
        except Exception as e:
            print(f"  [!] Could not get ACL: {e}")

        # 2. Check logging
        logging_enabled = False
        try:
            logging = s3.get_bucket_logging(Bucket=name)
            if logging.get("LoggingEnabled"):
                logging_enabled = True
        except Exception as e:
            print(f"  [!] Could not get logging info: {e}")

        # 3. Check versioning
        versioning_enabled = False
        try:
            versioning = s3.get_bucket_versioning(Bucket=name)
            if versioning.get("Status") == "Enabled":
                versioning_enabled = True
        except Exception as e:
            print(f"  [!] Could not get versioning info: {e}")

        # Report
        if is_public:
            print("  [MISCONFIG] Bucket is publicly accessible")
        else:
            print("  [OK] Bucket is not publicly accessible")

        if not logging_enabled:
            print("  [MISCONFIG] Logging is DISABLED")
        else:
            print("  [OK] Logging is enabled")

        if not versioning_enabled:
            print("  [MISCONFIG] Versioning is DISABLED")
        else:
            print("  [OK] Versioning is enabled")


def check_rds_instances():
    print("\n=== RDS Instance Checks ===")

    try:
        response = rds.describe_db_instances()
    except Exception as e:
        print(f"Error describing DB instances: {e}")
        return

    instances = response.get("DBInstances", [])
    if not instances:
        print("No RDS DB instances found.")
        return

    for db in instances:
        identifier = db["DBInstanceIdentifier"]
        publicly_accessible = db.get("PubliclyAccessible", False)
        deletion_protection = db.get("DeletionProtection", False)
        backup_retention = db.get("BackupRetentionPeriod", 0)

        print(f"\nDB Instance: {identifier}")

        if publicly_accessible:
            print("  [MISCONFIG] DB is publicly accessible")
        else:
            print("  [OK] Not publicly accessible")

        if not deletion_protection:
            print("  [MISCONFIG] Delete protection is DISABLED")
        else:
            print("  [OK] Delete protection is enabled")

        if backup_retention == 0:
            print("  [MISCONFIG] Backups are DISABLED (RetentionPeriod = 0)")
        else:
            print(f"  [OK] Backups enabled (RetentionPeriod = {backup_retention} days)")


def check_security_groups():
    print("\n=== Security Group Checks ===")

    try:
        response = ec2.describe_security_groups()
    except Exception as e:
        print(f"Error describing security groups: {e}")
        return

    sgs = response.get("SecurityGroups", [])
    if not sgs:
        print("No Security Groups found.")
        return

    for sg in sgs:
        sg_id = sg["GroupId"]
        sg_name = sg.get("GroupName", "")
        print(f"\nSecurity Group: {sg_name} ({sg_id})")

        inbound_rules = sg.get("IpPermissions", [])
        found_issue = False

        for perm in inbound_rules:
            from_port = perm.get("FromPort")
            to_port = perm.get("ToPort")
            ip_ranges = perm.get("IpRanges", [])
            ipv6_ranges = perm.get("Ipv6Ranges", [])

            # Some rules are "all ports" (from_port/to_port may be None)
            # So we guard with "is not None"
            # SSH port
            if from_port is not None and to_port is not None:
                # Check SSH (22)
                if from_port <= 22 <= to_port:
                    if any(r.get("CidrIp") == "0.0.0.0/0" for r in ip_ranges):
                        print("  [MISCONFIG] SSH (22) is open to the world (0.0.0.0/0)")
                        found_issue = True

                # Check MongoDB (27017)
                if from_port <= 27017 <= to_port:
                    if any(r.get("CidrIp") == "0.0.0.0/0" for r in ip_ranges):
                        print("  [MISCONFIG] MongoDB (27017) is open to the world (0.0.0.0/0)")
                        found_issue = True

            # Also check IPv6 "anywhere" (:::0/0)
            if any(r.get("CidrIpv6") == "::/0" for r in ipv6_ranges):
                print("  [MISCONFIG] Rule allows all IPv6 addresses (::/0)")
                found_issue = True

        if not found_issue:
            print("  [OK] No obvious SSH/MongoDB public access issues found.")


def main():
    print("Starting AWS security misconfiguration scan...")
    check_s3_buckets()
    check_rds_instances()
    check_security_groups()
    print("\nScan complete.")


if __name__ == "__main__":
    main()
