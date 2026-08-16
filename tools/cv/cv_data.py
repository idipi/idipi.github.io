# -*- coding: utf-8 -*-
"""
Layout/styling lives in build_cv.py - do not put formatting here.
"""

NAME = "Jevgeni Diede"
LOCATION = "Uusimaa, Finland"
EMAIL = "jevgeni.diede.work@outlook.com"
EMAIL_LINK = "mailto:jevgeni.diede.work@outlook.com"
SITE = "idipi.github.io"
SITE_LINK = "https://idipi.github.io"
# LinkedIn intentionally omitted - see README.

SUMMARY = (
    "Site Reliability Engineer with 3+ years of production operations experience across heterogeneous "
    "Kubernetes-based environments. Managed reliability for 8\u201310 independent production systems on AWS and "
    "Azure under 24/7 support with contractual SLA obligations (99.9%). Track record in incident response, "
    "SLO/SLI management, observability, and operational automation. Based in Finland (EU), open to hybrid "
    "roles in Finland or fully remote."
)

EXPERIENCE = [
    {
        "title": "Site Reliability Engineer \u2013 Operational Lead",
        "company": "Corewide LLP, London, UK (remote)",
        "dates": "Apr 2024 \u2013 Nov 2025",
        "bullets": [
            "Owned operational reliability for multiple independent production environments across AWS and Azure, "
            "supporting applications including asynchronous video interviewing platforms, large-scale video "
            "hosting, and EKS-based fintech systems (Helm, Terraform).",

            "Primary on-call escalation point for all production incidents under 24/7 support. Designed a "
            "structured escalation chain that eliminated recurring escalation failures \u2013 acknowledged by "
            "leadership as eliminating a persistent operational gap.",

            "Coordinated daily operations across an SRE team of 5\u20138 engineers: work allocation, on-call "
            "scheduling, and incident ownership.",

            "Facilitated blameless postmortems and established a unified documentation standard for incident "
            "follow-ups, improving knowledge retention and reducing repeat incidents.",

            "Developed internal Python tooling for engineer onboarding/offboarding workflows and automated "
            "operational reporting. Led SRE workstream during company-wide ticketing system migration.",

            "Tracked and reported SLO/SLI metrics tied directly to contractual client discount structures "
            "triggered by SLA breaches.",

            "Mentored junior and mid-level engineers; participated in technical hiring interviews.",
        ],
    },
    {
        "title": "Site Reliability Engineer",
        "company": "Corewide LLP, London, UK (remote)",
        "dates": "Dec 2022 \u2013 Apr 2024",
        "bullets": [
            "Provided 24/7 on-call support for ~5 production Kubernetes clusters (with separate prod/staging/dev "
            "environments) hosting distinct application architectures.",

            "Performed production backup and recovery for MySQL/PostgreSQL databases and RAID storage arrays, "
            "including real incident-driven restores.",

            "Built Grafana dashboards, developed custom Prometheus exporters in Python, and provisioned blackbox "
            "monitoring across services.",

            "Reviewed and tuned alerting rules on an ongoing basis \u2013 investigated whether noisy alerts "
            "indicated architectural issues or required threshold adjustment, reducing on-call alert fatigue.",

            "Managed Kubernetes and Docker workloads on AWS/Azure. Used Terraform and Ansible for infrastructure "
            "and observability provisioning. Maintained CI/CD pipelines in GitLab CI and GitHub Actions.",
        ],
    },
    {
        "title": "IT Infrastructure Engineer",
        "company": "PrivatBank, Dnipro, Ukraine",
        "dates": "Dec 2021 \u2013 Nov 2022",
        "bullets": [
            "Monitored and maintained infrastructure at scale \u2013 thousands of endpoints across all bank "
            "branches and offices \u2013 using Zabbix.",

            "Managed DNS, DHCP, SSL/TLS certificates, and configuration management systems.",

            "Built Node-RED automation workflows for ticket routing, data aggregation, and operational statistics, "
            "reducing manual triage and improving team response allocation.",
        ],
    },
]

SKILLS = [
    ("Cloud", "AWS, Azure"),
    ("Containers", "Kubernetes, Helm, Docker"),
    ("Observability", "Prometheus (incl. custom exporters), Grafana, Loki, Zabbix, blackbox monitoring"),
    ("IaC", "Terraform, Ansible"),
    ("CI/CD", "GitLab CI, GitHub Actions"),
    ("Scripting", "Python, Bash"),
    ("SRE Practices", "SLO/SLI tracking, incident management, blameless postmortems, escalation design"),
]

EDUCATION_SCHOOL = "Oles Honchar Dnipro National University"
EDUCATION_DEGREE = " \u2013 Bachelor\u2019s Degree (2018\u20132022)"

LANGUAGES = [
    "Ukrainian (Native)",
    "Russian (Native)",
    "English (Professional)",
    "Finnish (Elementary)",
]

PDF_TITLE = "SRE who actually answers pages at 3 AM"
PDF_SUBJECT = "Site Reliability Engineer CV"
PDF_AUTHOR = "Jevgeni Diede"
