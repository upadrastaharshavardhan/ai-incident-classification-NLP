"""
Synthetic IT Incident / Ticket generator.
Produces realistic ITSM-style tickets with category and priority labels.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


CATEGORY_TEMPLATES: Dict[str, List[Dict[str, str]]] = {
    "Network": [
        {
            "title": "VPN connection failures for remote users",
            "description": "Multiple users unable to connect to corporate VPN since morning. Error: Connection timed out. Affects approximately 40% of remote workforce.",
        },
        {
            "title": "Intermittent packet loss on floor 3 switches",
            "description": "Network team reports intermittent connectivity issues on floor 3. Users experiencing high latency and dropped packets. Core switch logs show interface flaps.",
        },
        {
            "title": "DNS resolution failures for internal domains",
            "description": "Users cannot resolve internal.company.com. External sites work fine. Suspected DNS server issue or zone transfer problem.",
        },
        {
            "title": "Wi-Fi authentication failures in Building B",
            "description": "Employees in Building B cannot authenticate to corporate Wi-Fi. RADIUS server may be overloaded or misconfigured.",
        },
        {
            "title": "Firewall blocking legitimate traffic after rule change",
            "description": "After last night's firewall policy update, several production services cannot reach external payment gateway. Need urgent rule review.",
        },
    ],
    "Software": [
        {
            "title": "CRM application throwing 500 errors",
            "description": "Salesforce-integrated CRM module returns HTTP 500 for all create/update operations. Error logs show NullPointerException in OrderService.",
        },
        {
            "title": "Payroll system calculation incorrect for overtime",
            "description": "HR reports that overtime hours are being calculated at regular rate instead of 1.5x. Affects last pay cycle for ~120 employees.",
        },
        {
            "title": "Mobile app crashes on login for Android 14",
            "description": "Android users on version 14 report immediate crash after entering credentials. iOS users unaffected. Crashlytics shows native library error.",
        },
        {
            "title": "Batch job failed - inventory sync not completed",
            "description": "Nightly inventory synchronization job failed with exit code 1. Downstream reports and warehouse systems have stale data.",
        },
        {
            "title": "Email notification service not sending messages",
            "description": "Users report they are not receiving password reset and order confirmation emails. SMTP queue is backing up.",
        },
    ],
    "Hardware": [
        {
            "title": "Server disk failure on DB-PROD-03",
            "description": "Hardware monitoring alert: Disk failure predicted on DB-PROD-03 (RAID array degraded). Immediate replacement required to avoid data loss.",
        },
        {
            "title": "Laptop not powering on - executive user",
            "description": "CTO laptop does not power on. No LED indicators. Possible motherboard or power adapter failure. Loaner device requested.",
        },
        {
            "title": "Printer in Finance floor offline",
            "description": "Network printer FIN-PRN-02 is offline. Users cannot print invoices. Physical check shows paper jam and error code 49.",
        },
        {
            "title": "UPS battery failure in Server Room A",
            "description": "UPS unit reporting battery end-of-life. Runtime reduced to <5 minutes. Risk of unclean shutdown during power event.",
        },
        {
            "title": "Monitor flickering on multiple workstations",
            "description": "Several users on Floor 2 report monitor flickering. Suspected graphics driver or hardware issue with recent docking station model.",
        },
    ],
    "Security": [
        {
            "title": "Suspicious login attempts detected",
            "description": "SIEM alert: Multiple failed login attempts from unusual geolocations for privileged accounts. Possible brute-force or credential stuffing attack.",
        },
        {
            "title": "Phishing email campaign targeting Finance",
            "description": "Several employees received sophisticated phishing emails impersonating CFO. Two users reported clicking the link. Need immediate investigation.",
        },
        {
            "title": "Malware detection on endpoint",
            "description": "EDR solution quarantined suspicious executable on user workstation. File appears to be Trojan. Need full scan and user interview.",
        },
        {
            "title": "Unauthorized access to shared drive",
            "description": "Access logs show unusual download activity on confidential HR shared folder outside business hours. Possible insider threat or compromised account.",
        },
        {
            "title": "SSL certificate expiring in 3 days",
            "description": "Public-facing portal certificate expires in 72 hours. Renewal process stuck in approval. Risk of service disruption and security warnings.",
        },
    ],
    "Access": [
        {
            "title": "New employee cannot access email and Teams",
            "description": "Onboarding ticket: New hire started today but AD account not provisioned correctly. Cannot access Outlook or Microsoft Teams.",
        },
        {
            "title": "Password reset not working for contractor",
            "description": "External contractor unable to reset password via self-service portal. Error: Account locked or not found in directory.",
        },
        {
            "title": "Role change - need elevated permissions",
            "description": "Employee promoted to Team Lead. Requires additional access to project management and reporting tools. Current role insufficient.",
        },
        {
            "title": "Shared mailbox permissions missing",
            "description": "Finance team reports they can no longer send from invoices@company.com shared mailbox after weekend maintenance.",
        },
        {
            "title": "VPN certificate expired for user",
            "description": "User cannot connect to VPN. Error indicates client certificate has expired. Needs re-issuance from PKI team.",
        },
    ],
    "Database": [
        {
            "title": "Production database high CPU and slow queries",
            "description": "DBA alert: CPU on ORDERS-DB consistently above 90%. Several long-running queries identified. Application response times degraded.",
        },
        {
            "title": "Replication lag between primary and replica",
            "description": "PostgreSQL replication lag exceeded 30 seconds. Read replicas serving stale data. Risk of data inconsistency for reporting.",
        },
        {
            "title": "Deadlock detected in order processing",
            "description": "Application logs show frequent deadlocks in order and inventory tables. Transactions being rolled back. Customer orders failing.",
        },
        {
            "title": "Backup job failed for critical database",
            "description": "Nightly full backup of CUSTOMER-DB failed with space error. Last successful backup is 36 hours old. Compliance risk.",
        },
        {
            "title": "Table space almost full - urgent",
            "description": "Tablespace USERS_DATA at 97% capacity. Growth rate indicates full within 12 hours. Need emergency expansion.",
        },
    ],
    "CloudInfra": [
        {
            "title": "AWS EC2 instance unreachable",
            "description": "Production EC2 instance i-0abc123 became unreachable. Status checks failing. Possible host failure or network ACL issue.",
        },
        {
            "title": "Kubernetes pod crash looping",
            "description": "Payment service pods in crashloopbackoff. OOMKilled events in logs. Memory limit may be too low after recent traffic increase.",
        },
        {
            "title": "S3 bucket access denied after policy change",
            "description": "Application cannot read from s3://company-assets after IAM policy update. 403 Access Denied errors in logs.",
        },
        {
            "title": "Azure App Service high latency",
            "description": "West Europe App Service plan showing elevated response times. Possible noisy neighbor or scaling issue.",
        },
        {
            "title": "Terraform apply failed - state lock",
            "description": "Infrastructure pipeline blocked. Terraform state is locked by a previous failed run. Manual unlock required.",
        },
    ],
    "Performance": [
        {
            "title": "Website extremely slow for European users",
            "description": "Users in EU region report page load times >8 seconds. CDN cache hit ratio dropped. Origin response times also elevated.",
        },
        {
            "title": "API gateway timeout errors increasing",
            "description": "API Gateway 504 errors increased 300% in last hour. Backend services show elevated latency. Possible database or downstream bottleneck.",
        },
        {
            "title": "Report generation taking >10 minutes",
            "description": "Monthly sales report that normally completes in 90 seconds now takes over 10 minutes and sometimes times out.",
        },
        {
            "title": "Mobile app laggy after latest release",
            "description": "Users report significant UI lag and battery drain after v3.2.0 release. Profiling suggests main-thread blocking.",
        },
        {
            "title": "Search functionality very slow",
            "description": "Product search that previously returned in <200ms now takes 2-4 seconds. Elasticsearch cluster may need tuning or scaling.",
        },
    ],
    "Other": [
        {
            "title": "General inquiry about system status",
            "description": "User asking whether systems are currently experiencing any known issues. No specific error reported.",
        },
        {
            "title": "Request for documentation",
            "description": "New team member requests access to internal runbooks and architecture diagrams.",
        },
        {
            "title": "Feedback on recent change",
            "description": "User providing feedback on the new UI layout. Not an incident but logged in the system.",
        },
        {
            "title": "Training request for new tool",
            "description": "Team would like training session on the newly introduced monitoring dashboard.",
        },
        {
            "title": "Unclear error message - needs clarification",
            "description": "User received an error dialog with code E-9921 but no description. Needs help understanding next steps.",
        },
    ],
}

# Priority is influenced by category + urgency keywords + business impact language
PRIORITY_RULES = {
    "P1-Critical": {
        "keywords": ["production down", "outage", "data loss", "security breach", "ransomware", "complete failure", "all users", "revenue impact"],
        "categories_boost": ["Security", "Database", "Network", "CloudInfra"],
    },
    "P2-High": {
        "keywords": ["degraded", "multiple users", "urgent", "blocking", "cannot work", "sla risk", "executive", "customer facing"],
        "categories_boost": ["Software", "Network", "Performance", "Access"],
    },
    "P3-Medium": {
        "keywords": ["intermittent", "some users", "workaround available", "non-critical", "delayed"],
        "categories_boost": ["Hardware", "Software", "Access", "Performance"],
    },
    "P4-Low": {
        "keywords": ["request", "inquiry", "documentation", "training", "feedback", "low impact", "cosmetic"],
        "categories_boost": ["Other", "Access"],
    },
}


def _assign_priority(category: str, title: str, description: str) -> str:
    """Heuristic priority assignment based on keywords and category."""
    text = (title + " " + description).lower()
    scores = {p: 0 for p in PRIORITY_RULES}

    for prio, rules in PRIORITY_RULES.items():
        for kw in rules["keywords"]:
            if kw in text:
                scores[prio] += 2
        if category in rules["categories_boost"]:
            scores[prio] += 1

    # Soft random noise so distribution is not perfectly deterministic
    for p in scores:
        scores[p] += random.random() * 0.5

    # Ensure P1 is rarer
    scores["P1-Critical"] *= 0.7

    return max(scores, key=scores.get)


def generate_incident_dataset(
    n_samples: int = 4000,
    seed: int = 42,
    categories: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Generate a realistic IT incident dataset.

    Returns DataFrame with columns:
    incident_id, timestamp, title, description, full_text,
    category, priority, affected_users_estimate
    """
    random.seed(seed)
    np.random.seed(seed)

    if categories is None:
        categories = list(CATEGORY_TEMPLATES.keys())

    records = []
    for i in range(n_samples):
        category = random.choice(categories)
        template = random.choice(CATEGORY_TEMPLATES[category])

        title = template["title"]
        description = template["description"]

        # Light lexical variation
        if random.random() < 0.3:
            description += f" Ticket opened by user-{random.randint(1000, 9999)}."
        if random.random() < 0.2:
            description += f" Reference: INC{random.randint(100000, 999999)}."

        priority = _assign_priority(category, title, description)

        # Rough impact estimate
        impact_map = {"P1-Critical": (50, 500), "P2-High": (10, 80), "P3-Medium": (2, 15), "P4-Low": (1, 3)}
        low, high = impact_map.get(priority, (1, 5))
        affected = random.randint(low, high)

        full_text = f"Title: {title}\nDescription: {description}"

        records.append(
            {
                "incident_id": f"INC-{i+1:06d}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 3000)),
                "title": title,
                "description": description,
                "full_text": full_text,
                "category": category,
                "priority": priority,
                "affected_users_estimate": affected,
            }
        )

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_incident_dataset(200)
    print(df.head(3))
    print("\nCategory distribution:")
    print(df["category"].value_counts())
    print("\nPriority distribution:")
    print(df["priority"].value_counts())
