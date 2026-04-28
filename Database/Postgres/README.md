# PostgreSQL Kubernetes Database Application

A simple Python application to connect to and interact with a PostgreSQL database deployed in a Kubernetes cluster.

## Overview

This application provides:
- Connection pooling for efficient database access
- CRUD operations (Create, Read, Update, Delete)
- Table management utilities
- Configuration via config file
- Comprehensive error handling and logging

## Prerequisites

- Python 3.7+
- `pip` package manager
- Access to a PostgreSQL database in Kubernetes (or via port-forward)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the environment in database_config.json:**

## Accessing PostgreSQL in Kubernetes Using kubectl port-forward (Recommended)

```bash
# Forward local port 5432 to the Kubernetes service
kubectl port-forward svc/postgres 5432:5432 -n postgres-namespace
```

## Running the Demo
```bash
python app.py
```

This demo will:
1. Show how to access PostgreSQL from outside the cluster
2. Create a sample table
3. Insert, select, update, and delete records
4. Display table structure
5. Clean up

## File Structure

```
PostgresApp/
├── postgresql.py          # Main database module
├── config.py              # Configuration management
├── app.py                 # Demo application with examples
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── QUICKSTART.md          # Quick start guide
```

## License

[Add license here]

## References
- [Setting up our PostgreSQL environment by "That DevOps Guy"](https://github.com/marcel-dempers/docker-development-youtube-series/blob/master/storage/databases/postgresql/4-k8s-basic/README.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/)
- [Kubernetes StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Docker PostgreSQL](https://hub.docker.com/_/postgres)
