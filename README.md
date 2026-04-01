🚀 sre-devops-gitops-lab

A complete SRE / DevOps / Platform Engineering lab to learn and practice:

GitOps with Flux CD
Kubernetes
Helm
Prometheus + Grafana
Alertmanager
Blackbox Exporter
Loki + Promtail (logging)
SOPS + age (secrets encryption)

🧠 What is this project?

This repository is a hands-on lab that builds a real-world SRE platform locally.

You will learn how to:

Deploy applications using GitOps
Monitor systems using metrics
Create and test alerts
Collect and explore logs
Debug failures like a real SRE

👉 This is not just setup — it’s a complete learning environment.

🏗 Architecture

                         +----------------------+
                         |      GitHub Repo     |
                         | sre-devops-gitops    |
                         +----------+-----------+
                                    |
                                    | GitOps Sync
                                    v
                           +-------------------+
                           |      Flux CD      |
                           +---------+---------+
                                     |
                                     v
        +--------------------------------------------------+
        |              Kubernetes Cluster                  |
        |--------------------------------------------------|
        |                                                  |
        |  apps namespace                                  |
        |   └── Caddy (web app)                           |
        |                                                  |
        |  monitoring namespace                            |
        |   ├── Prometheus (metrics)                      |
        |   ├── Grafana (dashboards)                      |
        |   ├── Alertmanager (alerts)                     |
        |   ├── Blackbox Exporter (HTTP probes)           |
        |   └── Node/K8s metrics                          |
        |                                                  |
        |  logging namespace                               |
        |   ├── Loki (log storage)                        |
        |   └── Promtail (log collector)                  |
        +--------------------------------------------------+

             Metrics        Logs         Alerts
           (Prometheus)   (Loki)    (Alertmanager)
                  \           |           /
                   \          |          /
                    \         ▼         /
                     +----------------+
                     |    Grafana     |
                     +----------------+

🎯 What you will build
✅ Health Checks

Cluster:

kubectl get nodes
kubectl get pods -A

Flux:

flux get sources git -A
flux get kustomizations -A
flux get helmreleases -A

Monitoring:

curl localhost:9090/-/ready

Logging:

curl localhost:3100/ready

Quick check:

kubectl get pods -A | grep -v Running
🧪 What is implemented
Kubernetes cluster
GitOps (Flux CD)
Caddy application
Prometheus monitoring
Grafana dashboards
Alertmanager alerts
Blackbox checks
Loki logging
Promtail log collection
SOPS encrypted secrets
🎓 What you learn
GitOps workflows
Kubernetes operations
Observability (metrics + logs)
Alerting
Debugging failures

🔮 Future Improvements
Ingress + domains
TLS
Slack / PagerDuty alerts
CI/CD pipeline
SLO dashboards
Distributed tracing

🛑 Troubleshooting

Port-forward issue:

kubectl port-forward --address 0.0.0.0 ...

Flux issues:

flux get kustomizations -A
kubectl -n flux-system logs deploy/kustomize-controller

⭐ Final Note

This lab simulates a real SRE environment.

You now have:

GitOps deployment
Monitoring
Alerting
Logging

👉 This is the core of modern DevOps & SRE platforms.
