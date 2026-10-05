Yes. If your current README is only going **up to the License section**, replace it with a proper project README that documents the actual implementation you built.

Based on your current project structure:

```text
clouddefend/
├── agent/
│   └── ssh_detector.py
├── rules/
│   └── ssh_rules.py
├── logs/
│   └── alerts.json
├── api.py
├── monitor.py
└── dashboard.html
```

use this as your **complete `README.md`**:

```markdown
# CloudDefend

### Cloud Security Monitoring & SSH Threat Detection Platform

CloudDefend is a lightweight cloud security monitoring and threat detection platform designed to detect suspicious SSH authentication activity on a cloud-hosted Linux virtual machine.

It continuously analyzes SSH authentication logs, identifies suspicious login behavior, applies detection rules, generates security alerts, and exposes the results through a REST API and web-based security dashboard.

---

## Features

- SSH authentication log monitoring
- Detection of failed SSH authentication attempts
- Detection of invalid SSH users
- Source IP-based event aggregation
- SSH brute-force detection
- Configurable time-window based detection rules
- High-severity security alerts
- REST API for security data
- Web-based security dashboard
- JSON-based alert storage
- Linux systemd service deployment
- Cloud VM deployment on Microsoft Azure

---

## Architecture

```text
                  ┌──────────────────────┐
                  │   Azure Linux VM     │
                  │                      │
                  │     SSH Service      │
                  └──────────┬───────────┘
                             │
                             │ Authentication Logs
                             ▼
                  ┌──────────────────────┐
                  │   SSH Log Detector   │
                  │  agent/              │
                  │  ssh_detector.py     │
                  └──────────┬───────────┘
                             │
                             │ Parsed Events
                             ▼
                  ┌──────────────────────┐
                  │    Detection Rules   │
                  │  rules/              │
                  │  ssh_rules.py        │
                  └──────────┬───────────┘
                             │
                             │ Security Alerts
                             ▼
                  ┌──────────────────────┐
                  │     Alert Store      │
                  │  logs/alerts.json    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     FastAPI API      │
                  │       api.py         │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Security Dashboard   │
                  │   dashboard.html     │
                  └──────────────────────┘
```

---

## How CloudDefend Works

CloudDefend follows a simple security monitoring pipeline:

```text
SSH Logs
   ↓
Log Collection
   ↓
Event Parsing
   ↓
Security Rule Evaluation
   ↓
Brute-Force Detection
   ↓
Alert Generation
   ↓
JSON Alert Storage
   ↓
REST API
   ↓
Security Dashboard
```

### 1. Log Collection

CloudDefend reads SSH authentication events from the Linux system logs.

The detector extracts relevant authentication information such as:

- Timestamp
- Source IP address
- Username
- Event type

Example:

```json
{
  "timestamp": "2026-10-05T18:47:32+00:00",
  "ip": "154.18.197.29",
  "username": "root",
  "type": "failed_auth"
}
```

---

### 2. Event Classification

SSH events are classified into security-relevant categories.

Examples include:

```text
failed_auth
invalid_user
```

This allows the detection engine to work with structured security events rather than raw log lines.

---

### 3. Brute-Force Detection

CloudDefend analyzes authentication events based on:

- Source IP
- Number of suspicious events
- Time window

The current detection rule identifies repeated SSH authentication activity within a defined time window.

Example alert:

```json
{
  "rule": "SSH_BRUTE_FORCE",
  "severity": "HIGH",
  "source_ip": "154.18.197.29",
  "event_count": 13,
  "window_minutes": 10
}
```

---

## Detection Rule

### SSH_BRUTE_FORCE

| Property | Value |
|---|---|
| Rule | `SSH_BRUTE_FORCE` |
| Severity | `HIGH` |
| Detection Type | SSH authentication abuse |
| Detection Basis | Repeated events from same source IP |
| Time Window | 10 minutes |

The rule is designed to identify repeated authentication attempts that may indicate SSH password spraying or brute-force activity.

---

## Example Detection

During testing, CloudDefend detected suspicious SSH activity from multiple external source IP addresses.

Example:

```text
Suspicious SSH events: 75

Events by source IP:

154.18.197.29    42
5.172.178.253     25
62.60.130.201      3
45.148.10.157      3
45.148.10.152      1
45.148.10.151      1
```

The detection engine generated two high-severity alerts:

```text
SSH_BRUTE_FORCE
Source: 5.172.178.253
Events: 6
Window: 10 minutes
Severity: HIGH
```

```text
SSH_BRUTE_FORCE
Source: 154.18.197.29
Events: 13
Window: 10 minutes
Severity: HIGH
```

---

# REST API

CloudDefend exposes security information through a FastAPI backend.

## Health Check

```http
GET /
```

Example:

```bash
curl http://127.0.0.1:8000/
```

Response:

```json
{
  "project": "CloudDefend",
  "status": "operational"
}
```

---

## Get Alerts

```http
GET /alerts
```

Example:

```bash
curl http://127.0.0.1:8000/alerts
```

Example response:

```json
[
  {
    "rule": "SSH_BRUTE_FORCE",
    "severity": "HIGH",
    "source_ip": "5.172.178.253",
    "event_count": 6,
    "window_minutes": 10
  },
  {
    "rule": "SSH_BRUTE_FORCE",
    "severity": "HIGH",
    "source_ip": "154.18.197.29",
    "event_count": 13,
    "window_minutes": 10
  }
]
```

---

## Get Statistics

```http
GET /stats
```

Example:

```bash
curl http://127.0.0.1:8000/stats
```

Example response:

```json
{
  "total_alerts": 2,
  "high_severity": 2
}
```

---

# Security Dashboard

CloudDefend provides a browser-based dashboard for viewing detected security alerts.

The dashboard displays:

- System status
- Total alerts
- High-severity alerts
- Detection rule
- Source IP
- Number of suspicious events
- Detection time window

Example dashboard:

```text
┌─────────────────────────────────────────────────────┐
│                    CloudDefend                      │
│       Cloud Security Monitoring Platform             │
├──────────────────┬──────────────────┬───────────────┤
│ System Status    │ Total Alerts     │ High Severity │
│                  │                  │               │
│ OPERATIONAL      │       2          │       2       │
├──────────────────┴──────────────────┴───────────────┤
│ Severity │ Rule            │ Source IP    │ Events   │
├──────────┼─────────────────┼──────────────┼──────────┤
│ HIGH     │ SSH_BRUTE_FORCE │ 5.172.178.253│ 6        │
│ HIGH     │ SSH_BRUTE_FORCE │154.18.197.29 │ 13       │
└─────────────────────────────────────────────────────┘
```

---

# Project Structure

```text
clouddefend/
│
├── agent/
│   └── ssh_detector.py
│       └── Collects and parses SSH authentication logs
│
├── rules/
│   └── ssh_rules.py
│       └── Contains SSH brute-force detection logic
│
├── logs/
│   └── alerts.json
│       └── Stores generated security alerts
│
├── api.py
│   └── FastAPI REST API
│
├── monitor.py
│   └── Monitoring/alert processing entry point
│
└── dashboard.html
    └── Web-based security dashboard
```

---

# Technology Stack

### Backend

- Python 3
- FastAPI
- Uvicorn

### Security Monitoring

- Linux SSH authentication logs
- Python log parsing
- Rule-based threat detection
- IP-based event aggregation

### Frontend

- HTML
- CSS
- JavaScript
- Fetch API

### Infrastructure

- Microsoft Azure Virtual Machine
- Linux
- systemd

---

# Installation

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd clouddefend
```

---

## 2. Install Dependencies

Install FastAPI and Uvicorn:

```bash
pip3 install fastapi uvicorn
```

If your system requires it:

```bash
python3 -m pip install fastapi uvicorn
```

---

# Running CloudDefend

Start the API server:

```bash
cd ~/clouddefend

python3 -m uvicorn api:app \
    --host 0.0.0.0 \
    --port 8000
```

The API will be available at:

```text
http://<SERVER_IP>:8000
```

---

# Running the Detector

Run the SSH detector:

```bash
python3 ~/clouddefend/agent/ssh_detector.py
```

Example:

```text
Suspicious SSH events: 75

Events by source IP:
154.18.197.29  42
5.172.178.253   25
62.60.130.201    3
```

---

# Testing the Detection Engine

The detection engine can be tested directly:

```bash
python3 - <<'PY'
import sys

sys.path.insert(0, "/home/azureuser/clouddefend/agent")
sys.path.insert(0, "/home/azureuser/clouddefend/rules")

from ssh_detector import get_ssh_logs, parse_event
from ssh_rules import detect_ssh_bruteforce

events = []

for line in get_ssh_logs():
    event = parse_event(line)

    if event:
        events.append(event)

alerts = detect_ssh_bruteforce(events)

print(f"Alerts generated: {len(alerts)}")

for alert in alerts:
    print(alert)
PY
```

---

# Running as a Linux Service

CloudDefend can run as a systemd service so that the API starts automatically with the server.

Start the service:

```bash
sudo systemctl start clouddefend
```

Check its status:

```bash
sudo systemctl status clouddefend
```

Enable automatic startup:

```bash
sudo systemctl enable clouddefend
```

Example:

```text
● clouddefend.service
   Loaded: loaded
   Active: active (running)

   └─ python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

This allows CloudDefend to continue running without manually starting Uvicorn after every VM reboot.

---

# Azure Deployment

CloudDefend was deployed on a Microsoft Azure Linux Virtual Machine.

The deployment consists of:

```text
Internet
    │
    ▼
Azure VM
    │
    ├── SSH
    │
    ├── CloudDefend Monitor
    │
    ├── FastAPI
    │
    └── Security Dashboard
```

The API listens on:

```text
0.0.0.0:8000
```

For remote browser access, TCP port `8000` must be permitted through the Azure VM's networking/security configuration.

---

# Security Considerations

CloudDefend is intended for defensive security monitoring.

The system:

- Monitors authentication activity
- Detects repeated SSH authentication attempts
- Identifies suspicious source IP addresses
- Generates security alerts
- Provides visibility through a dashboard

The project does **not** attempt to exploit or compromise the detected source systems.

---

# Current Capabilities

The current implementation supports:

- [x] SSH log collection
- [x] SSH event parsing
- [x] Failed authentication detection
- [x] Invalid-user detection
- [x] Source IP tracking
- [x] Brute-force detection
- [x] High-severity alert generation
- [x] JSON alert storage
- [x] REST API
- [x] Security dashboard
- [x] Azure VM deployment
- [x] systemd service
- [x] Remote dashboard access

---

# Future Improvements

Possible future enhancements include:

### Detection

- Multiple SSH detection rules
- Password spraying detection
- Distributed brute-force detection
- Successful login after repeated failures
- Privilege escalation detection
- Suspicious command execution detection

### Threat Intelligence

- IP reputation lookup
- AbuseIPDB integration
- VirusTotal integration
- GeoIP enrichment
- ASN/ISP information
- Known malicious IP detection

### Alerting

- Email notifications
- Telegram notifications
- Slack notifications
- Webhook integrations

### Platform

- PostgreSQL/SQLite alert database
- Authentication and RBAC
- HTTPS/TLS
- Docker deployment
- Kubernetes deployment
- Centralized logging
- SIEM integration

### Dashboard

- Alert filtering
- Search
- IP reputation information
- Time-series attack graphs
- Attack source map
- Alert details page
- Real-time event updates

---

# Limitations

The current version is intentionally lightweight.

It primarily focuses on SSH authentication monitoring and rule-based brute-force detection.

It should not be considered a complete enterprise SIEM or EDR solution.

The current implementation also uses JSON-based alert storage rather than a production-grade database.

---

# Use Cases

CloudDefend can be used for:

- Cloud security learning
- SOC analyst training
- Linux security monitoring
- SSH brute-force detection
- Cybersecurity demonstrations
- Security engineering projects
- Azure security labs
- Threat detection research

---

# Learning Objectives

This project demonstrates practical knowledge of:

- Linux authentication logs
- SSH security
- Log parsing
- Event normalization
- Rule-based detection
- Security alert generation
- REST API development
- FastAPI
- Cloud VM deployment
- Azure networking
- Linux systemd
- Basic SOC/SIEM concepts
- Security dashboard development

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Author

**Aryan Singh Shaktawat**

B.Tech Computer Science & Engineering  
Cyber Security & Forensics

---

## Project Summary

CloudDefend is a lightweight cloud security monitoring platform that demonstrates how raw Linux SSH authentication logs can be transformed into structured security events, analyzed using detection rules, converted into actionable alerts, and presented through a web-based security dashboard.

```text
Raw Logs
   ↓
Detection
   ↓
Rules
   ↓
Alerts
   ↓
API
   ↓
Dashboard
```

**CloudDefend — Monitor. Detect. Respond.**
```
