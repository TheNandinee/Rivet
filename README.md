# Rivet

<div align="center">

### A Distributed Edge Proxy Platform

*Inspired by modern CDN architectures for intelligent traffic routing, caching, rate limiting, failover, and observability.*

---

**Built by**

**Paridhi Sharma** • **Nandinee** • **Lakshay Yadav**

</div>

---

## Overview

Rivet is a distributed edge proxy platform that simulates the core infrastructure behind modern Content Delivery Networks (CDNs) and API Gateways.

Instead of allowing every client request to directly reach the backend, Rivet routes traffic through multiple edge nodes that intelligently cache responses, enforce rate limits, monitor traffic, and automatically recover from failures.

The project demonstrates fundamental distributed systems concepts including reverse proxying, edge caching, load balancing, failover, observability, and traffic protection using a modular microservices architecture.

---

## Key Features

### Reverse Proxy

* Multi-node edge architecture
* HTTP request forwarding
* Connection pooling
* Retry & timeout handling
* Reverse proxy routing

### Intelligent Caching

* In-memory LRU cache
* Configurable TTL
* Cache invalidation
* Cache hit/miss tracking
* Reduced backend latency

### Traffic Protection

* Token Bucket rate limiting
* Per-IP request throttling
* API Key based limits
* Basic bot detection

### Load Balancing & Failover

* Multiple edge nodes
* Health-aware routing
* Automatic failover
* Traffic redistribution

### Observability

* Prometheus metrics
* Grafana dashboards
* Request latency monitoring
* Cache analytics
* Node health monitoring

---

# Architecture

```
                     Clients
                         │
                         ▼
              ┌────────────────────┐
              │     Edge Nodes     │
              │ ────────────────   │
              │  Edge 1            │
              │  Edge 2            │
              │  Edge 3            │
              └─────────┬──────────┘
                        │
                        ▼
                 Control Plane
                        │
                        ▼
                  Origin Server

          ┌────────────────────────────┐
          │  Prometheus + Grafana      │
          │  Metrics & Dashboards      │
          └────────────────────────────┘
```

---

# Repository Structure

```
rivet/
│
├── services/
│   ├── edge/
│   ├── origin/
│   └── control-plane/
│
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── load-tests/
│
├── shared/
│
├── docs/
├── scripts/
├── tests/
│
├── docker-compose.yml
├── README.md
└── requirements-dev.txt
```

---

# Technology Stack

| Category         | Technology              |
| ---------------- | ----------------------- |
| Language         | Python 3.12             |
| Framework        | FastAPI                 |
| HTTP Client      | httpx                   |
| Monitoring       | Prometheus              |
| Dashboards       | Grafana                 |
| Containerization | Docker & Docker Compose |
| Load Testing     | k6 / wrk                |
| Configuration    | Pydantic Settings       |

---

# Team Responsibilities

## Paridhi Sharma

### Edge Infrastructure

* Reverse Proxy
* Request Forwarding
* HTTP Routing
* Caching Layer
* Load Balancing
* Health Checks
* Automatic Failover
* Performance Optimization

---

## Nandinee

### Security & Traffic Protection

* Origin Server
* Token Bucket Rate Limiter
* Bot Detection
* Request Validation
* Logging Infrastructure
* Abuse Simulation

---

## Lakshay Yadav

### Monitoring & Observability

* Prometheus Integration
* Grafana Dashboards
* Metrics Collection
* Load Testing
* Performance Reporting

---

# Services

| Service       | Purpose                                      |
| ------------- | -------------------------------------------- |
| Edge          | Reverse proxy, caching, routing              |
| Origin        | Backend application serving requests         |
| Control Plane | Configuration management & service discovery |
| Prometheus    | Metrics collection                           |
| Grafana       | Visualization & dashboards                   |

---

# Performance Goals

* Cache Hit Ratio ≥ **80%**
* **5×** reduction in cached request latency
* Automatic node failover within **10 seconds**
* Stable latency under burst traffic
* Real-time monitoring through Grafana
* One-command deployment using Docker Compose

---

# Getting Started

Clone the repository

```bash
git clone <repository-url>
cd rivet
```

Start the platform

```bash
docker compose up --build
```

Available Services

| Service       | URL                   |
| ------------- | --------------------- |
| Edge Node     | http://localhost:8000 |
| Origin Server | http://localhost:9000 |
| Prometheus    | http://localhost:9090 |
| Grafana       | http://localhost:3000 |

---

# Development Roadmap

### Phase 1

* Project setup
* Docker infrastructure
* Reverse proxy
* Origin server

### Phase 2

* LRU caching
* TTL support
* Cache invalidation
* Metrics integration

### Phase 3

* Rate limiting
* Traffic protection
* Control plane

### Phase 4

* Load balancing
* Automatic failover
* Dashboard completion
* Performance benchmarking

---

# Learning Outcomes

This project explores practical backend and distributed systems concepts including:

* Reverse Proxy Design
* Distributed Systems
* Edge Computing
* HTTP Networking
* Load Balancing
* Caching Strategies
* Rate Limiting Algorithms
* Fault Tolerance
* Observability
* Containerized Deployment
* Performance Engineering

---

# License

This project is developed for educational and learning purposes.
