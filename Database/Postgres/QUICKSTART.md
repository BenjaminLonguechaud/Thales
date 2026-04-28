# Quick Start Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Configure Connection in database_config.json

## 3. Access PostgreSQL from Outside Kubernetes with Port-Forward**
```bash
kubectl port-forward svc/postgres 5432:5432 -n default
```

## 4. Test Connection
```bash
python app.py
```

## Files Overview

| File | Purpose |
|------|---------|
| `postgresql.py` | Main database module with CRUD operations |
| `config.py` | Configuration management |
| `app.py` | Demo application |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
