```markdown
# CloudDefend

CloudDefend is a lightweight **cloud security monitoring and threat detection platform** deployed on a Microsoft Azure Virtual Machine.

It monitors SSH authentication activity, identifies suspicious authentication behavior, detects SSH brute-force attacks using rule-based detection, generates security alerts, and exposes the results through a FastAPI REST API and web-based security dashboard.

---

## Overview

Publicly exposed cloud servers are continuously scanned by automated systems attempting to discover valid usernames and gain SSH access.

CloudDefend monitors these SSH authentication events and converts raw system logs into structured security events.

The current detection pipeline is:

```text
Azure Virtual Machine
        │
        ▼
   SSH / sshd logs
        │
        ▼
 SSH Log Detector
        │
        ▼
 Structured Security Events
        │
        ▼
 Detection Rules
        │
        ▼
 SSH Brute-Force Detection
        │
        ▼
 Security Alerts
        │
        ├───────────────┐
        ▼               ▼
   alerts.json       FastAPI
                         │
                         ▼
                  Security Dashboard
```

---

## Features

- SSH authentication log monitoring
- Failed authentication detection
- Invalid-user detection
- Source IP tracking
- SSH brute-force detection
- Time-window based detection rules
- Severity-based security alerts
- JSON alert storage
- REST API
- Security monitoring dashboard
- Linux systemd service
- Deployment on Microsoft Azure VM

---

## Detection Logic

CloudDefend currently uses a rule-based approach to identify SSH brute-force activity.

An alert is generated when repeated suspicious SSH authentication events from the same source IP occur within a configured time window.

Example:

```json
{
  "rule": "SSH_BRUTE_FORCE",
  "severity": "HIGH",
  "source_ip": "154.18.197.29",
  "event_count": 13,
  "window_minutes": 10
}
```

The system can identify events such as:

```text
failed_auth
invalid_user
```

Example SSH activity observed during testing:

```text
root authentication attempts
invalid user ubuntu
repeated authentication attempts
```

These events are converted into structured records containing:

- Timestamp
- Source IP
- Username
- Event type

---

## Example Detection Result

During testing, CloudDefend detected repeated SSH activity and generated alerts such as:

```text
Alerts generated: 2

SSH_BRUTE_FORCE
Severity: HIGH
Source: 5.172.178.253
Events: 6
Window: 10 minutes

SSH_BRUTE_FORCE
Severity: HIGH
Source: 154.18.197.29
Events: 13
Window: 10 minutes
```

---

## Architecture

### 1. Log Collection

CloudDefend reads SSH authentication events from the Linux system journal.

```text
journalctl → SSH Detector
```

### 2. Event Parsing

The SSH detector converts raw log entries into structured security events.

Example:

```json
{
  "timestamp": "2026-10-05T19:02:19+00:00",
  "ip": "154.18.197.29",
  "username": "root",
  "type": "failed_auth"
}
```

### 3. Detection Engine

The detection rules analyze events within a configurable time window.

The current rule detects repeated SSH authentication activity from the same source IP.

### 4. Alert Generation

Detected threats are converted into structured alerts containing:

- Detection rule
- Severity
- Source IP
- Event count
- Detection window
- First event
- Last event
- Detection timestamp

### 5. REST API

FastAPI exposes the monitoring data through API endpoints.

### 6. Dashboard

A lightweight HTML/JavaScript dashboard displays:

- System status
- Total alerts
- High-severity alerts
- Source IP
- Detection rule
- Event count
- Detection window

---

## API

### Health Check

```http
GET /
```

Example response:

```json
{
  "project": "CloudDefend",
  "status": "operational"
}
```

### Security Alerts

```http
GET /alerts
```

Returns detected security alerts.

Example:

```json
[
  {
    "rule": "SSH_BRUTE_FORCE",
    "severity": "HIGH",
    "source_ip": "154.18.197.29",
    "event_count": 13,
    "window_minutes": 10
  }
]
```

### Statistics

```http
GET /stats
```

Example:

```json
{
  "total_alerts": 2,
  "high_severity": 2
}
```

---

## Project Structure

```text
CloudDefend/
│
├── agent/
│   └── ssh_detector.py
│
├── rules/
│   └── ssh_rules.py
│
├── logs/
│   └── alerts.json
│
├── api.py
├── monitor.py
├── dashboard.html
├── README.md
└── .gitignore
```

### Components

| File | Purpose |
|---|---|
| `agent/ssh_detector.py` | Collects and parses SSH security events |
| `rules/ssh_rules.py` | Contains SSH threat-detection rules |
| `monitor.py` | Monitoring/detection execution |
| `api.py` | FastAPI REST API |
| `dashboard.html` | Web security dashboard |
| `logs/alerts.json` | Stores generated alerts |

---

## Azure Deployment

CloudDefend was deployed on a **Microsoft Azure Virtual Machine** running Linux.

The application runs using Uvicorn:

```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

The application was configured as a Linux `systemd` service:

```text
clouddefend.service
```

The service is configured to start automatically with the system.

Check service status:

```bash
sudo systemctl status clouddefend
```

Start the service:

```bash
sudo systemctl start clouddefend
```

Stop the service:

```bash
sudo systemctl stop clouddefend
```

Restart the service:

```bash
sudo systemctl restart clouddefend
```

---

## Security Configuration

The Azure VM was configured with basic SSH hardening.

### Firewall

UFW was enabled with incoming traffic denied by default.

SSH access was explicitly allowed:

```text
22/tcp ALLOW IN
```

Configuration:

```text
Default: deny (incoming)
Default: allow (outgoing)
```

### SSH Hardening

The SSH configuration was verified to use:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

This prevents direct root SSH login and password-based SSH authentication while allowing public-key authentication.

---

## Technologies

### Cloud

- Microsoft Azure
- Azure Virtual Machine

### Backend

- Python
- FastAPI
- Uvicorn

### Security

- OpenSSH
- Linux system logs
- SSH authentication monitoring
- Rule-based threat detection
- UFW

### Frontend

- HTML
- CSS
- JavaScript

### Infrastructure

- Linux
- systemd
- Git
- GitHub

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/aryansinghshaktawat/CloudDefend.git
cd CloudDefend
```

Install the required Python dependencies:

```bash
pip install fastapi uvicorn
```

Start the API:

```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/
```

Test alerts:

```bash
curl http://127.0.0.1:8000/alerts
```

Test statistics:

```bash
curl http://127.0.0.1:8000/stats
```

---

## Security Considerations

CloudDefend is currently a monitoring and detection platform intended for educational and development purposes.

For a production deployment, additional security controls should be implemented, including:

- HTTPS/TLS
- API authentication
- Role-based access control
- Secure secret management
- Network-level access restrictions
- Database-backed alert storage
- Centralized logging
- Alert notification mechanisms
- IP reputation enrichment
- Rate limiting
- Audit logging

The dashboard should not be exposed publicly without appropriate authentication and transport security.

---

## Future Improvements

Planned improvements include:

- Real-time log streaming
- Automated IP reputation lookup
- GeoIP enrichment
- Automated malicious IP blocking
- Email/Telegram/Slack notifications
- Authentication and RBAC
- HTTPS/TLS
- Database-backed alert storage
- Additional detection rules
- Docker deployment
- SIEM integration
- Cloud security telemetry
- MITRE ATT&CK technique mapping
- Risk scoring
- Historical attack analytics

---

## Learning Outcomes

This project provided practical experience with:

- Linux server administration
- Azure cloud infrastructure
- SSH security
- Authentication monitoring
- Security log analysis
- Threat detection
- Rule-based detection engines
- REST API development
- FastAPI
- Linux systemd
- Firewall configuration
- Cloud security monitoring
- Git and GitHub deployment

---

## License

MIT License
```

### One important change before you push

Your current project has:

```text
logs/alerts.json
```


