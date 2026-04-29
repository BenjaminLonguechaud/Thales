# Quick Start Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Configure Connection
- Adjust the database configuration file database_config.template.json and rename database_config.json.
- Adjust the CipherTrust and CRDP configuration file CRDP/config.template.json and rename config.json.

## 3. Access PostgreSQL from Outside Kubernetes with Port-Forward**
```bash
kubectl port-forward svc/postgres 5432:5432 -n postgres-namespace
```

## 4. Test Connection
```bash
python app.py
```
