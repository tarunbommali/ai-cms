# Artificial Intelligent Cloud Monitoring System

This repository contains the Artificial Intelligent Cloud Monitoring System: a React dashboard, FastAPI API, PostgreSQL database, Prometheus metrics collection, Grafana dashboards, Alertmanager, and ML analysis for monitored instances.

## Features in the current application

- JWT registration and login
- User profile lookup and update
- Admin and owner-based instance access
- CPU, memory, disk, network, load-average, uptime, and combined metrics
- Threshold alerts for CPU, memory, and disk
- Prometheus and Node Exporter integration
- Anomaly detection, forecasts, health scoring, failure prediction, root-cause analysis, capacity planning, and autoscaling recommendations
- Dashboard, metrics, instances, alerts, and how-it-works pages

## Start with Docker Compose

The supported Compose file is [`docker-compose.yml`](docker-compose.yml). It starts:

- PostgreSQL on `5432`
- Prometheus on `9090`
- Grafana on `3001`
- Alertmanager on `9093`
- FastAPI on `8000`
- React/Nginx frontend on `3000`
- A Node Exporter container on `9100`

For local use:

```bash
cp backend/.env.example backend/.env
# Set a unique SECRET_KEY in backend/.env.
docker compose up -d
```

Open:

- Dashboard: `http://localhost:3000`
- API docs: `http://localhost:8000/api/docs`
- API ReDoc: `http://localhost:8000/api/redoc`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`
- Alertmanager: `http://localhost:9093`

For EC2 deployment, follow [`QUICKSTART.md`](QUICKSTART.md). It includes the frontend API URL requirement, security-group rules, and remote Node Exporter setup.

## API routes

The complete request and response schemas are available in the running Swagger UI at `/api/docs`. The implemented route groups are:

| Group | Routes |
|---|---|
| Health | `GET /api/health/`, `GET /api/health/services` |
| Authentication | `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, `PUT /api/auth/me` |
| Instances | `GET/POST /api/instances/`, `GET/PUT/DELETE /api/instances/{instance_id}`, `GET /api/instances/{instance_id}/alerts` |
| Metrics | `GET /api/metrics/cpu/{instance_id}`, `/memory/`, `/disk/`, `/network/`, `/load/`, `/all/`, and `/dashboard/summary` |
| ML | `POST /api/ml/anomaly/train/{id}`, `GET /api/ml/anomaly/detect/{id}`, `POST /api/ml/cpu/train/{id}`, `GET /api/ml/cpu/predict/{id}`, `POST /api/ml/memory/train/{id}`, `GET /api/ml/memory/predict/{id}`, `GET /api/ml/memory/leak-detection/{id}`, `GET /api/ml/health-score/{id}`, `GET /api/ml/failure/predict/{id}`, `GET /api/ml/autoscale/recommend/{id}`, `GET /api/ml/capacity/plan/{id}`, `GET /api/ml/root-cause/analyze/{id}`, and `GET /api/ml/dashboard/ml-summary/{id}` |

`/api/auth/register`, `/api/auth/login`, and both health routes are public. Listing, creating, updating, and deleting instances requires the bearer token returned by `/api/auth/login`. The individual-instance, metrics, dashboard-summary, and ML routes currently accept optional authentication; owner checks apply when a user is authenticated. Instance and ML routes use the application’s numeric instance ID, not the AWS EC2 ID alone.

## Local development without Docker

The backend uses SQLite by default when run directly:

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Run the frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend expects `VITE_API_URL` and otherwise calls `http://127.0.0.1:8000/api`.

## Important behavior

- Metrics snapshots are written when `/api/metrics/all/{instance_id}` is requested. ML endpoints that need history return an insufficient-data error until at least 10 snapshots exist.
- The development Compose file supplies PostgreSQL and service URLs through container environment variables. It is not the same configuration as running the backend directly with SQLite.
- The production Compose file requires `nginx/nginx.conf` and `nginx/ssl/`; those files are not included in this repository, so use `docker-compose.yml` unless you provide them.

## Main directories

| Directory | Purpose |
|---|---|
| `backend/` | FastAPI routes, database models, services, and ML code |
| `frontend/` | React dashboard |
| `monitoring/` | Prometheus, Grafana, and Alertmanager configuration |

## License

MIT. See [LICENSE](LICENSE).
