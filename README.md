<div align="center">

# RIVET

### Distributed Edge Proxy Platform

A high-performance, distributed reverse proxy platform inspired by modern CDN architectures, featuring intelligent edge caching, configurable rate limiting, automatic failover, and real-time observability.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800)

---

**Built by**

**Paridhi Sharma--** 
**Nandinee--**
**Lakshay Yadav**

</div>

---

# Overview

Rivet is a distributed edge proxy platform that simulates how modern Content Delivery Networks (CDNs) accelerate, protect, and monitor web traffic.

Instead of sending every client request directly to the backend server, Rivet routes traffic through multiple intelligent edge nodes capable of:

- Reverse proxying requests
- Response caching
- Rate limiting
- Traffic monitoring
- Automatic failover
- Load balancing
- Real-time metrics collection

The project demonstrates core distributed systems concepts used by infrastructure companies such as Cloudflare, Fastly, Akamai, and large-scale cloud platforms.

---

# Features

### Reverse Proxy

- Multi-node edge architecture
- HTTP request forwarding
- Connection pooling
- Retry handling
- Timeout management

---

### Intelligent Caching

- In-memory LRU cache
- Configurable TTL
- Cache invalidation
- Cache hit/miss tracking
- Reduced backend latency

---

### Rate Limiting

- Token Bucket algorithm
- Per-IP throttling
- Per API Key limits
- Burst traffic protection

---

### Load Balancing

- Multiple edge nodes
- Health-aware routing
- Automatic failover
- Traffic redistribution

---

### Observability

- Prometheus metrics
- Grafana dashboards
- Request latency
- Cache statistics
- Node health
- Traffic analytics

---

# Architecture

```
                Clients
                    │
                    ▼
          ┌───────────────────┐
          │   Edge Node 1     │
          ├───────────────────┤
          │   Edge Node 2     │
          ├───────────────────┤
          │   Edge Node 3     │
          └───────────────────┘
                    │
                    ▼
             Control Plane
                    │
                    ▼
             Origin Server

         Prometheus + Grafana
```

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Backend | FastAPI |
| Language | Python |
| HTTP Client | httpx |
| Monitoring | Prometheus |
| Dashboards | Grafana |
| Containerization | Docker |
| Load Testing | k6 / wrk |
| Caching | Custom LRU Cache |

---

# Repository Structure

```
Rivet/

│
├── edge/
│   ├── proxy.py
│   ├── cache.py
│   └── metrics.py
│
├── origin/
│   └── server.py
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana_dashboard.json
│
├── tests/
│
├── docker-compose.yml
│
└── README.md
```

---

# Team Responsibilities

## Paridhi Sharma

### Networking & Proxy Layer

- Reverse Proxy
- Request Forwarding
- HTTP Routing
- Caching Layer
- Load Balancing
- Failover
- Health Checks
- Performance Optimization

---

## Nandinee

### Security & Traffic Protection

- Origin Server
- Token Bucket Rate Limiter
- Bot Detection
- Request Fingerprinting
- Abuse Simulation
- Logging Infrastructure

---

## Lakshay Yadav

### Observability

- Prometheus Integration
- Grafana Dashboards
- Metrics Collection
- Load Testing
- Reporting

---

# Performance Goals

- Cache Hit Ratio ≥ 80%
- 5× reduction in response latency
- Automatic failover within 10 seconds
- Real-time monitoring
- Dockerized deployment
- One-command startup

---

# Getting Started

Clone the repository

```bash
git clone <repository-url>
cd Rivet
```

Start the platform

```bash
docker compose up --build
```

Access the services

| Service | URL |
|----------|-----|
| Edge Node | localhost:8000 |
| Origin Server | localhost:9000 |
| Prometheus | localhost:9090 |
| Grafana | localhost:3000 |

---

# Future Enhancements

- Distributed cache using Redis
- TLS termination
- OpenTelemetry tracing
- Adaptive rate limiting
- WebSocket proxying
- Geo-aware routing
- Service discovery
- Kubernetes deployment

---

# Learning Outcomes

This project explores practical distributed systems concepts including:

- Reverse Proxy Design
- HTTP Networking
- Distributed Caching
- Rate Limiting Algorithms
- Fault Tolerance
- Load Balancing
- Observability
- Containerized Deployment
- Performance Engineering

---

# License

This project is intended for educational purposes.
