# sre-devops-gitops-lab
# sre-devops-gitops-lab

A hands-on **SRE / DevOps / Platform Engineering lab** built to learn and practice:

- **GitOps** with Flux CD
- **Kubernetes**
- **Helm**
- **Prometheus**
- **Grafana**
- **Alertmanager**
- **Blackbox Exporter**
- **Loki**
- **Promtail**
- **Secrets management** with SOPS + age
- and later: **Ansible**, **Ingress**, **SLOs**, **Tracing**, and more

This project is designed as a **step-by-step lab** for people who want practical experience with the tools and workflows often used in real SRE / DevOps roles.

---

## Table of Contents

- [1. What is this lab?](#1-what-is-this-lab)
- [2. Who is this for?](#2-who-is-this-for)
- [3. Learning goals](#3-learning-goals)
- [4. Final architecture](#4-final-architecture)
- [5. What you will build](#5-what-you-will-build)
- [6. Supported host systems](#6-supported-host-systems)
- [7. Prerequisites](#7-prerequisites)
- [8. High-level setup flow](#8-high-level-setup-flow)
- [9. Repository structure](#9-repository-structure)
- [10. Step-by-step roadmap](#10-step-by-step-roadmap)
- [11. Accessing the services](#11-accessing-the-services)
- [12. Health checks](#12-health-checks)
- [13. What is already implemented](#13-what-is-already-implemented)
- [14. Future improvements](#14-future-improvements)
- [15. Troubleshooting notes](#15-troubleshooting-notes)

---

## 1. What is this lab?

This repository is a **practical SRE/DevOps training environment**.

It starts from a local virtual machine and builds up a small but realistic platform using Kubernetes and GitOps. The idea is not only to deploy tools, but to understand how they work together:

- applications
- monitoring
- alerting
- logging
- secrets
- GitOps workflows

This is meant to be a **learning playground**, not a production deployment.

---

## 2. Who is this for?

This lab is useful for:

- people preparing for **SRE roles**
- junior or mid-level **DevOps engineers**
- platform engineers learning **GitOps**
- anyone wanting a home lab for:
  - Kubernetes
  - observability
  - alerts
  - logs
  - troubleshooting

---

## 3. Learning goals

By working through this lab, you will learn how to:

- create and operate a Kubernetes lab
- structure a GitOps repository
- deploy workloads using **Flux CD**
- install applications using **Helm**
- expose and test a sample service
- collect and visualize **metrics**
- define and test **alerts**
- collect and query **logs**
- store secrets safely in Git using **SOPS**
- debug failures end-to-end

---

## 4. Final architecture

```text
                         +----------------------+
                         |      GitHub Repo     |
                         |  sre-devops-gitops   |
                         +----------+-----------+
                                    |
                                    | GitOps sync
                                    v
                           +-------------------+
                           |      Flux CD      |
                           | GitRepository     |
                           | Kustomizations    |
                           | HelmReleases      |
                           +---------+---------+
                                     |
                                     v
                     +-----------------------------------+
                     |        Kubernetes Cluster         |
                     |                                   |
                     |  apps namespace                   |
                     |   - Caddy                         |
                     |                                   |
                     |  monitoring namespace             |
                     |   - Prometheus                    |
                     |   - Grafana                       |
                     |   - Alertmanager                  |
                     |   - Blackbox Exporter             |
                     |   - kube-state-metrics            |
                     |   - node-exporter                 |
                     |                                   |
                     |  logging namespace                |
                     |   - Loki                          |
                     |   - Promtail                      |
                     +-----------------------------------+
