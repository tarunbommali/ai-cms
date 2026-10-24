# Artificial Intelligent Cloud Monitoring System — Quick Start

This is the setup for the application currently in this repository. The supported path is the development Compose stack on one host, with Prometheus scraping Node Exporter on monitored EC2 instances.

## 1. Requirements

- Ubuntu 22.04/24.04 for the host, or Docker Desktop on Windows/macOS
- Docker with the Compose plugin (`docker compose`)
- One or more monitored Linux EC2 instances
- TCP access from the monitoring host to each monitored instance on port `9100`

For an AWS monitoring host, allow in its security group:

- `22` from your IP for SSH
- `3000` from your IP for the dashboard while testing
- `8000` from your IP for the API while testing
- `3001`, `9090`, and `9093` only from trusted IPs if you need their UIs

On each monitored EC2 security group, allow TCP `9100` from the monitoring host’s security group.

## 2. Install Docker on Ubuntu

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
```

Log out and reconnect, then verify:

```bash
docker --version
docker compose version
```

## 3. Download and configure

```bash
git clone https://github.com/tarunbommali/ai-cms.git
cd ai-cms
cp backend/.env.example backend/.env
openssl rand -hex 32
```

Put the generated value in `backend/.env`:

```env
SECRET_KEY=replace_with_the_generated_value
```

The Compose file sets the backend’s database and service URLs to the Compose service names. Keep the `DATABASE_URL` in `backend/.env` for direct, non-Docker runs; it is overridden by the Compose environment.

Email alerts are disabled until `SMTP_USER` and `SMTP_PASSWORD` are configured in `backend/.env`.

## 4. Make the frontend reach the backend

For local access on the same computer, no extra setting is needed. For an EC2 host accessed from another computer, create `frontend/.env` before building:

```env
VITE_API_URL=http://MONITORING_SERVER_IP:8000/api
```

Replace `MONITORING_SERVER_IP` with the monitoring EC2 private or public IP that your browser can reach. `VITE_API_URL` is compiled into the frontend image, so rebuild after changing it.

## 5. Configure monitored EC2 instances

The current Prometheus file contains one existing target. Replace that target with the private IP and port of each monitored instance in `monitoring/prometheus/prometheus.yml`:

```yaml
  - job_name: "node-exporter"
    static_configs:
      - targets:
          - "10.0.1.100:9100"
```

Install Node Exporter on every monitored Linux instance:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin --user-group node_exporter
cd /tmp
curl -LO https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
tar xzf node_exporter-1.8.2.linux-amd64.tar.gz
sudo cp node_exporter-1.8.2.linux-amd64/node_exporter /usr/local/bin/

sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<'EOF'
[Unit]
Description=Prometheus Node Exporter
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now node_exporter
curl http://localhost:9100/metrics
```

The repository’s Compose file also starts a Node Exporter container on the monitoring host at port `9100`. That container is separate from Node Exporter installed on monitored EC2 instances.

## 6. Start the platform

From the project root:

```bash
docker compose up -d --build
docker compose ps
```

Useful commands:

```bash
docker compose logs -f
docker compose down
docker compose restart
```

## 7. Use the application

Replace `SERVER_IP` with the monitoring host address:

- Dashboard: `http://SERVER_IP:3000`
- API docs: `http://SERVER_IP:8000/api/docs`
- Prometheus targets: `http://SERVER_IP:9090/targets`
- Grafana: `http://SERVER_IP:3001`
- Alertmanager: `http://SERVER_IP:9093`

1. Register at `/register`.
2. Log in at `/login`.
3. Open **Instances** and add each monitored instance using its private IP and port `9100`.
4. Open **Dashboard**, **Metrics**, or **Alerts**.

The current Compose file uses Grafana credentials `admin` / `admin`. Change them in `docker-compose.yml` before exposing Grafana to an untrusted network.

ML features use metrics snapshots. Snapshots are saved when the application requests `/api/metrics/all/{instance_id}`; training endpoints require at least 10 recent snapshots. Until then, some ML endpoints return an insufficient-data response.

## Troubleshooting

```bash
# Check all containers
docker compose ps

# Check the backend
curl http://localhost:8000/api/health

# Check a target from the monitoring host
curl http://TARGET_PRIVATE_IP:9100/metrics

# Inspect service logs
docker compose logs backend
docker compose logs prometheus
```

If a Prometheus target is down, check the target’s Node Exporter service, private IP, routing, and security-group rule for port `9100`.

If the dashboard loads but login fails on EC2, check `frontend/.env`, confirm `VITE_API_URL` points to the monitoring host’s API, and rebuild with `docker compose up -d --build`.
