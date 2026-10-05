
# CloudDefend

> Cloud Security Monitoring & Threat Detection Platform

CloudDefend is a lightweight security monitoring platform designed to detect and visualize suspicious SSH authentication activity on a Linux cloud server.

It analyzes SSH logs, identifies suspicious authentication events, applies detection rules for brute-force behavior, and exposes the results through a REST API and web dashboard.

---

## Features

- SSH authentication log monitoring
- Failed SSH authentication detection
- Invalid SSH user detection
- Source IP tracking
- SSH brute-force detection
- Time-window based detection rules
- Severity classification
- REST API for security alerts
- Web-based security dashboard
- Persistent alert storage
- Linux systemd service
- Azure Virtual Machine deployment

---

## Architecture

```text
                    ┌─────────────────────┐
                    │    Linux SSH Logs   │
                    │     journald        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SSH Detector     │
                    │  Log Collection &   │
                    │      Parsing        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Detection Rules   │
                    │                     │
                    │ SSH_BRUTE_FORCE     │
                    │ Time-window checks  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Alert Generation  │
                    │                     │
                    │ Severity            │
                    │ Source IP           │
                    │ Event Count         │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │   FastAPI REST   │        │  Alert Storage   │
       │       API        │        │   alerts.json    │
       └────────┬─────────┘        └──────────────────┘
                │
                ▼
       ┌──────────────────┐
       │ Web Dashboard    │
       │                  │
       │ System Status    │
       │ Total Alerts     │
       │ High Severity    │
       │ Source IPs       │
       └──────────────────┘
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

---

## Detection Pipeline

CloudDefend follows this security monitoring workflow:

```text
SSH Logs
   │
   ▼
Log Collection
   │
   ▼
Event Parsing
   │
   ▼
Event Normalization
   │
   ▼
Detection Rules
   │
   ▼
Threat Detection
   │
   ▼
Alert Generation
   │
   ├── Source IP
   ├── Username
   ├── Event Count
   ├── Detection Window
   └── Severity
   │
   ▼
REST API
   │
   ▼
Security Dashboard
```

---

## Components

### SSH Detector

`agent/ssh_detector.py`

The SSH detector collects SSH authentication events from the Linux system logs and converts them into structured security events.

Example:

```json
{
  "timestamp": "2026-10-05T18:44:33+00:00",
  "ip": "5.172.178.253",
  "username": "ubuntu",
  "type": "invalid_user"
}
```

Supported event types include:

- `failed_auth`
- `invalid_user`

---

### Detection Rules

`rules/ssh_rules.py`

The detection engine analyzes normalized SSH events and applies security rules.

The current detection rule is:

```text
SSH_BRUTE_FORCE
```

The rule identifies repeated SSH authentication activity from the same source IP within a configured time window.

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

### Alert Storage

Detected alerts are stored in:

```text
logs/alerts.json
```

This provides persistent storage for the generated security alerts.

---

### FastAPI Backend

`api.py`

CloudDefend provides a REST API using FastAPI.

### Available Endpoints

| Endpoint | Description |
|---|---|
| `/` | Security dashboard |
| `/alerts` | Returns detected alerts |
| `/stats` | Returns alert statistics |

Example:

```bash
curl http://127.0.0.1:8000/stats
```

Response:

```json
{
  "total_alerts": 2,
  "high_severity": 2
}
```

Get alerts:

```bash
curl http://127.0.0.1:8000/alerts
```

---

## Security Dashboard

The CloudDefend dashboard provides a simple security monitoring interface.

It displays:

- System status
- Total alerts
- High-severity alerts
- Detection rule
- Source IP
- Event count
- Detection window

The dashboard communicates with the FastAPI backend to retrieve the latest security information.

---

## Example Detection

During testing, the system detected repeated SSH authentication attempts against the publicly accessible cloud VM.

Example alerts included:

```text
Rule: SSH_BRUTE_FORCE
Severity: HIGH
Source IP: 5.172.178.253
Events: 6
Window: 10 minutes
```

and:

```text
Rule: SSH_BRUTE_FORCE
Severity: HIGH
Source IP: 154.18.197.29
Events: 13
Window: 10 minutes
```

The system successfully converted raw SSH authentication logs into structured security alerts.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core application |
| FastAPI | REST API |
| Uvicorn | ASGI server |
| OpenSSH | SSH service |
| systemd-journald | Log collection |
| journalctl | Log retrieval |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Dashboard functionality |
| JSON | Alert storage |
| systemd | Service management |
| Microsoft Azure | Cloud deployment |

---

## Deployment

CloudDefend was deployed on an Ubuntu-based Microsoft Azure Virtual Machine.

### Install Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

Install Python dependencies:

```bash
pip3 install fastapi uvicorn
```

### Start the API

```bash
cd ~/clouddefend
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

The API listens on:

```text
0.0.0.0:8000
```

---

## Systemd Deployment

CloudDefend can run as a Linux systemd service.

Start the service:

```bash
sudo systemctl start clouddefend
```

Enable automatic startup:

```bash
sudo systemctl enable clouddefend
```

Check service status:

```bash
sudo systemctl status clouddefend
```

Expected status:

```text
Active: active (running)
```

This allows CloudDefend to continue running independently of the SSH terminal session and automatically start when the VM boots.

---

## Firewall Configuration

The Azure VM was configured with UFW.

Current firewall policy:

```text
Default: deny (incoming)
Default: allow (outgoing)
```

SSH access:

```text
22/tcp ALLOW IN
```

SSH was configured to use key-based authentication.

Relevant SSH configuration:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

This prevents direct root login and password-based SSH authentication.

---

## Security Monitoring Example

During testing, the VM received repeated automated SSH authentication attempts.

The detector identified activity such as:

```text
Invalid user ubuntu
```

and:

```text
Connection reset by authenticating user root
```

CloudDefend normalized these events and grouped them by source IP.

This allowed the detection engine to identify repeated authentication attempts as potential brute-force activity.

---

## Current Capabilities

- [x] SSH log collection
- [x] SSH event parsing
- [x] Failed authentication detection
- [x] Invalid user detection
- [x] Source IP extraction
- [x] Brute-force detection
- [x] Time-window analysis
- [x] Severity classification
- [x] Alert generation
- [x] JSON alert storage
- [x] FastAPI REST API
- [x] Security dashboard
- [x] systemd service
- [x] Azure VM deployment

---

## Future Improvements

- Automatic malicious IP blocking
- Fail2ban integration
- GeoIP enrichment
- IP reputation analysis
- Threat intelligence integration
- Email/Telegram/Slack notifications
- Real-time log streaming
- PostgreSQL database
- Role-based dashboard access
- HTTPS/TLS
- Docker deployment
- SIEM integration
- MITRE ATT&CK mapping
- Additional Linux security detections
- Authentication anomaly detection

---

## Limitations

CloudDefend currently focuses primarily on SSH authentication activity.

It is a lightweight security monitoring and threat detection prototype and is not intended to replace a full SIEM, EDR, IDS, or cloud-native security platform.

Detection is currently rule-based and depends on configured thresholds and time windows.

---

## Security Considerations

When deploying CloudDefend on a public cloud VM:

- Use SSH keys instead of passwords.
- Disable direct root login.
- Keep the operating system updated.
- Restrict exposed ports using Azure NSGs and UFW.
- Avoid exposing administrative services unnecessarily.
- Use HTTPS/TLS for production deployments.
- Never commit private keys, passwords, API tokens, or other secrets to GitHub.

---

## Project Status

**Functional Prototype**

CloudDefend successfully demonstrates an end-to-end security monitoring workflow:

```text
Log Collection
      ↓
Event Parsing
      ↓
Detection Rules
      ↓
Threat Detection
      ↓
Alert Generation
      ↓
REST API
      ↓
Security Dashboard
```

---

## Author

**Aryan Singh Shaktawat**

B.Tech Computer Science & Engineering  
Cyber Security & Forensics

GitHub:  
https://github.com/aryansinghshaktawat

---

## License

This project is licensed under the MIT License.
```
